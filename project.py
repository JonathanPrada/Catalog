from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Category, Items, Users


# all the imports an application uses get called name
app = Flask(__name__)


# connect to our database
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# catalog page
@app.route('/')
def catalog():
    categories = session.query(Category).all()
    return render_template('catalog.html', categories=categories)


# login page
@app.route('/')
def login():
    return render_template('login.html')


# items page
@app.route('/catalog/<int:category_id>/items')
def items(category_id):
    allitems = session.query(Items).all()
    return render_template('items.html', items=allitems)


# items page
@app.route('/catalog/category/item')
def item():
    return render_template('item.html')


# add item page
@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if request.method == 'POST':
        newitem = Items(
            name=request.form['name'],
            description=request.form['description'])
        session.add(newitem)
        session.commit()
        return redirect(url_for('catalog'))
    else:
        return render_template('additem.html')


# edit item page
@app.route('/catalog/category/item/edit')
def edititem():
    return render_template('edititem.html')


# delete item page
@app.route('/catalog/category/item/delete')
def deleteitem():
    return render_template('deleteitem.html')


# run only if script executed from python interpreter and not imported as a module
if __name__ == '__main__':
    # reload the server every time code changes
    app.debug = True
    # run on the local server host machine
    app.run(host='0.0.0.0', port=5000)
