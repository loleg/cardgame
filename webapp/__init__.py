# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from pymongo import MongoClient

DB_NAME = 'cardgame'
app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': DB_NAME}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

pymongo_client = MongoClient()


def register_blueprints(app):
    # Prevents circular imports
    from webapp.views import cards_blueprint

    app.register_blueprint(cards_blueprint)


if __name__ == '__main__':
    app.run()

register_blueprints(app)
