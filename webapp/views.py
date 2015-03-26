# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'
from flask import Blueprint, jsonify, render_template, redirect, request
from flask.views import MethodView, View
from bson.json_util import dumps, ObjectId, json
from flask.ext.mongoengine.wtf import model_form

from webapp import pymongo_client, DB_NAME
from webapp.models import Author

cards_blueprint = Blueprint('cards', __name__, template_folder='templates')
exclude_collections = ['system.indexes']


def mongo_to_dict(object):
    if '_id' in object:
        object['_id'] = str(object['_id'])
    return object


def get_collection_names():
    _db = pymongo_client.cardgame
    return list(filter(lambda x: x not in exclude_collections, _db.collection_names()))


def get_collection(collection, projection=None):
    _db = pymongo_client.cardgame
    results = None
    collections = get_collection_names()
    if projection:
        find_args = (projection)
    else:
        find_args = ()
    if collection is None or collection == 'all':
        results = {}
        for _collection in collections:
            results[_collection] = _db[_collection].find(*find_args)
    elif collection in collections:
        results = _db[collection].find(*find_args)
    return results


class AuthorAPI(MethodView):
    def get(self, timeperiod, id):
        collection = pymongo_client[DB_NAME][timeperiod]
        _id = ObjectId(id)
        author = collection.find_one(dict(_id=_id), dict(_id=False))
        return dumps(author)

    def post(self, period):
        pass


class TimePeriodAPI(MethodView):
    def get(self, period):
        periods = get_collection(period)
        if periods:
            status = 200
        else:
            status = 404
        return dumps(dict(timeperiod=map(mongo_to_dict, periods))), status


class AbstractView(View):
    def __init__(self, template):
        self.template = template

    def get_template_name(self):
        return self.template

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get_objects(self):
        return None


class FormView(MethodView):
    def __init__(self, template, Model):
        self.template = template
        self.Model = Model

    def post(self):
        print(request.get_data())
        form = model_form(self.Model)
        return render_template(self.template, **dict(form=form(request.form)))


class TimePeriodView(AbstractView):
    def get_objects(self):
        schema_fields = Author()._db_field_map.values()
        return schema_fields

    def dispatch_request(self):
        collections = get_collection_names()
        context = dict(titles=self.get_objects(), timeperiods=json.dumps(collections), init=collections[0])
        return self.render_template(context)


period_api = TimePeriodAPI.as_view('timeperiod')
author_api = AuthorAPI.as_view('author')

cards_blueprint.add_url_rule('/author_form',
                             view_func=FormView.as_view('form', template='author_form.html', Model=Author))
cards_blueprint.add_url_rule('/', view_func=TimePeriodView.as_view('index', template='index.html'))
cards_blueprint.add_url_rule('/timeperiod/<period>/', view_func=period_api)
cards_blueprint.add_url_rule('/author/<timeperiod>/<id>/', view_func=author_api)
