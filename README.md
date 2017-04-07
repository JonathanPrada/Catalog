# Catalog
A project done in Bootstrap, Python, Flask and JavaScript.

Here we utilise jsonify, GET/POST, Routing, SqlAlchemy, Templating, Dynamic URLs & Facebook third party Authentication.

## FILES

Static: Holds the custom css.
Templates: Holds the Flask templates for the front end.
Root folder: Main scripts, Database Models and Facebook API.

## INSTALLATION

Download or git clone.
You need a personal Facebook App API key for this project to work.
You can get one here: https://developers.facebook.com/
With your personal API key, edit the login.html & fb_client_secrets.json.

## CONFIGURATION

catalog/static <br>
catalog/templates <br>
data.py<br>
database.py<br>
fb_client_secrets.json<br>
project.py<br>

## RUNNING

To run this project, you need vagrant and virtual box.

1. Navigate to the vagrant environment with this project already included

2. Run vagrant up and then vagrant ssh

3. Inside the project folder, run database.py to create the database using python database.py

4. Populate the database with categories by running data.py

5. Run project.py and navigate to localhost:5000 in your browser

## TODO

Further improve the front-end as the focus was the functionality.

## DEMO

Live demo:Coming Soon
