import os

from flask import Flask, render_template, request, redirect  # etc.
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Create and name Flask app
app = Flask("FlaskLoginApp")

# database connection
app.config['MONGODB_SETTINGS'] = {
	'db': 'swe2017',
	'host': 'mongodb://localhost/swe2017',
	'port': 12345
}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.debug = os.environ.get('DEBUG',False)

db = MongoEngine(app) # connect MongoEngine with Flask App
app.session_interface = MongoEngineSessionInterface(db) # sessions w/ mongoengine

# Flask BCrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)

# Associate Flask-Login manager with current app
login_manager = LoginManager()
login_manager.init_app(app)
