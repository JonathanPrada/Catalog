from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Category, Items, Users

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# all the imports an application uses get called name
app = Flask(__name__)
# required for flash messaging
app.secret_key = 'some_secret'

# connect to our database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session
    # in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    login_session.clear()
    # return "you have been logged out"
    return redirect(url_for('catalog'))


# User Helper Functions
def createUser(login_session):
    newUser = Users(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/catalog/JSON')
def catalogJSON():
    category = session.query(Category).all()
    return jsonify(category=[r.serialize for r in category])


@app.route('/items/JSON')
def itemsJSON():
    allitemsjson = session.query(Items).all()
    return jsonify(allitemsjson=[r.serialize for r in allitemsjson])


# catalog page
@app.route('/')
def catalog():
    categories = session.query(Category).all()
    allitems = session.query(Items).all()
    if 'username' not in login_session:
        return render_template('publiccatalog.html', categories=categories, allitems=allitems)
    else:
        loggedinas = login_session['username']
        return render_template('catalog.html', categories=categories, allitems=allitems, logged=loggedinas)


# login page
@app.route('/')
def login():
    return render_template('login.html')


# items page
@app.route('/catalog/<int:category_id>/items')
def items(category_id):
    categories = session.query(Category).all()
    categoryselected = session.query(Category).filter_by(id=category_id).one()
    allitems = session.query(Items).filter_by(category_id=category_id).all()
    return render_template('items.html', categories=categories, items=allitems, categoryselected=categoryselected)


# item page
@app.route('/catalog/category/<int:id>')
def item(id):
    categories = session.query(Category).all()
    singleitem = session.query(Items).filter_by(id=id).one()
    if 'username' not in login_session:
        return render_template('publicitem.html', categories=categories, item=singleitem)
    else:
        return render_template('item.html', categories=categories, item=singleitem)


# add item page
@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if 'username' not in login_session:
        return redirect(url_for('catalog'))
    else:
        if request.method == 'POST':
            newitem = Items(
                name=request.form['name'],
                description=request.form['description'],
                creator_email=login_session['email'],
                category_id=request.form['cat'])
            session.add(newitem)
            session.commit()
            return redirect(url_for('catalog'))
        else:
            return render_template('additem.html')


# edit item page
@app.route('/catalog/<string:edit_item>/edit', methods=['GET', 'POST'])
def edititem(edit_item):
    itemtoedit = session.query(Items).filter_by(name=edit_item).one()
    if 'username' not in login_session:
        return redirect(url_for('catalog'))
    else:
        if login_session['email'] == itemtoedit.creator_email:
            if request.method == 'POST':
                # if login_session['email'] == itemtoedit.creator_email:
                itemtoedit.name = request.form['name']
                itemtoedit.description = request.form['description']
                itemtoedit.category_id = request.form['cat']
                return redirect(url_for('catalog'))
            # else:
                # error = "You cannot edit this"
                # return render_template('edititem.html', item=itemtoedit, error=error)
            else:
                return render_template('edititem.html', item=itemtoedit)
        else:
            error = "You do not have permission to edit this item"
            return render_template('edititem.html', item=itemtoedit, error=error)

# delete item page
@app.route('/catalog/<string:delete_item>/delete', methods=['GET', 'POST'])
def deleteitem(delete_item):
    itemtodelete = session.query(Items).filter_by(name=delete_item).one()
    if 'username' not in login_session:
        return redirect(url_for('catalog'))
    else:
        if login_session['email'] == itemtodelete.creator_email:
            if request.method == 'POST':
                session.delete(itemtodelete)
                session.commit()
                return redirect(url_for('catalog'))
            else:
                return render_template('deleteitem.html')
        else:
            error = "You do not have permission to delete this item"
            return render_template('deleteitem.html', error=error)

# run only if script executed from python interpreter and not imported as a module
if __name__ == '__main__':
    # reload the server every time code changes
    app.debug = True
    # run on the local server host machine
    app.run(host='0.0.0.0', port=5000)
