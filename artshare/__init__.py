from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_folder='static')

# Secret key for the forms for security such as CSRF attacks, also required for the seesion
app.config['SECRET_KEY'] = 'soen287-assignment3'
# App config to hold the path to the local sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from artshare import routes
