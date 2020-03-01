from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

#   Setting up path of Config file
app.config.from_object('config.Conf')

#   Init Model
db = SQLAlchemy(app)
db.create_all()

#   Loading Model Classes and Controller Classes
from app.controllers import *