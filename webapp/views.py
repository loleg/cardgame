# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'
from flask import Blueprint, request, redirect, render_template, url_for, jsonify, make_response
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from webapp.models import Card
from flask_restful import Resource, fields, marshal
from webapp import pymongo_client, DB_NAME
from bson.json_util import dumps, ObjectId

cards_blueprint = Blueprint('cards', __name__, template_folder='templates')
exclude_collections = ['system.indexes']

mongo_to_json = lambda objects: list(map(dumps, objects))


def get_collection(collection):
    _db = pymongo_client.cardgame
    results = {}

    collections = filter(lambda x: x not in exclude_collections, _db.collection_names())
    if collection is None or collection == 'all':
        for _collection in collections:
            results[_collection] = mongo_to_json(_db[_collection].find())
    elif collection in collections:
        print(_db['1941 gestorben'])
        results[collection] = mongo_to_json(_db[collection].find())
    return results


class AuthorAPI(MethodView):
    def get(self, timeperiod, id):
        collection = pymongo_client[DB_NAME][timeperiod]
        _id = ObjectId(id)
        author = collection.find_one(dict(_id=_id))
        return dumps(author)

    def post(self, period):
        pass


class TimePeriodAPI(MethodView):
    def get(self, period):
        print(period)
        periods = get_collection(period)
        print(periods)
        if periods:
            status = 200
        else:
            status = 404
        return make_response(jsonify(periods), status)


period_api = TimePeriodAPI.as_view('timeperiod')
author_api = AuthorAPI.as_view('author')
cards_blueprint.add_url_rule('/timeperiod/<period>', view_func=period_api)
cards_blueprint.add_url_rule('/author/<timeperiod>/<id>', view_func=author_api)