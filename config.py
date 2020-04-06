import os

class Conf(object):
    DEBUG = True
    DEVELOPMENT = True
    SITE_NAME = "OVGA Scoring"  #   It will affect the whole website
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "mysql://admin:Vancouver2010@15.222.176.252:23306/PublicDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False