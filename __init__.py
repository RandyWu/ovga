from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required
from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

#   Setting up path of Config file
app.config.from_object('config.Conf')

#   TODO: 404 page
# @app.errorhandler(404)
# def page_not_fount(error):
#     pass

#   Init Model
db = SQLAlchemy(app)
db.create_all()


#   Loading Model Classes and Controller Classes
# from app.model import models
# from app.controller import *