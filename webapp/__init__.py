# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from pymongo import MongoClient
import os

DB_NAME = 'publicdomaingame'
HOST = 'mongodb://pdg:003dJFNsPbMiqkH@ds039211.mongolab.com:39211/publicdomaingame'  # os.environ['PROD_MONGODB']

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'host': HOST}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

pymongo_client = MongoClient(host=HOST)


def register_blueprints(app):
    # Prevents circular imports
    from webapp.views import cards_blueprint

    app.register_blueprint(cards_blueprint)


if __name__ == '__main__':
    app.run()

register_blueprints(app)
