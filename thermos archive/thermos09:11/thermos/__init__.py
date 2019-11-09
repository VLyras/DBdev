import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Message, Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
mail = Mail()

app.config['SECRET_KEY'] = '\xd3\x869\x06\xb9\xe7~\xde\xc55l\x19l\xc2\xdc\r\x01i:\x9dvA\x98\xbc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = False
db = SQLAlchemy(app)

# Configuring contact mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'driftbee.info@gmail.com'
app.config["MAIL_PASSWORD"] = 'driftbee888'
mail.init_app(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# Enable debugtoolbar
toolbar = DebugToolbarExtension(app)

# for displaying timestamps
moment = Moment(app)

import models
import views
