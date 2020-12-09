from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '2a6352e066e2360e8169b91e4d3e8a5f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://mxpgrlxlxcnfwg:dc13c53fa5d3742a094ecf2e607494270d87ebaadfc5f0c5a23d2c9977c8bb5f@ec2-54-237-155-151.compute-1.amazonaws.com:5432/d3nlt1fikgsico'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signIn'
login_manager.login_message_category = 'info'

from store_me import routes
# from store_me.create_db import Create_DB
# Create_DB(db)
