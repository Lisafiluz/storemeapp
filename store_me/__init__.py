import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY'] or '2a6352e066e2360e8169b91e4d3e8a5f'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] or 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signIn'
login_manager.login_message_category = 'info'


from . import routes
# from store_me import routes
# from StoreMeApp.store_me.create_db import Create_DB
# Create_DB(db)
