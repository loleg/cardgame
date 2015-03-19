# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'
from flask import Blueprint, jsonify, render_template
from flask.views import MethodView, View
from bson.json_util import dumps, ObjectId, json

from webapp import pymongo_client, DB_NAME
from webapp.models import Author

cards_blueprint = Blueprint('cards', __name__, template_folder='templates')
exclude_collections = ['system.indexes']

mongo_to_json = lambda objects: list(map(dumps, objects))


def get_collection(collection):
    _db = pymongo_client.cardgame
    results = None
    collections = filter(lambda x: x not in exclude_collections, _db.collection_names())
    if collection is None or collection == 'all':
        results = {}
        for _collection in collections:
            results[_collection] = _db[_collection].find({}, dict(_id=False))
    elif collection in collections:
        results = _db[collection].find({}, dict(_id=False))  # TODO remove projection later
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
        periods = list(periods)
        return dumps(dict(timeperiod=periods)), status


class AbstractView(View):
    def __init__(self, template):
        self.template = template

    def get_template_name(self):
        return self.template

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    def get_objects(self):
        return None


class TimePeriodView(AbstractView):
    def get_objects(self):
        schema_fields = Author()._db_field_map.values()
        Author._fields_ordered

        # return ['Format','Name', 'Gestorben in']

        return schema_fields

    def dispatch_request(self):
        context = {'titles': self.get_objects()}
        return self.render_template(context)


period_api = TimePeriodAPI.as_view('timeperiod')
author_api = AuthorAPI.as_view('author')
cards_blueprint.add_url_rule('/', view_func=TimePeriodView.as_view('index', template='index.html'))
cards_blueprint.add_url_rule('/timeperiod/<period>/', view_func=period_api)
cards_blueprint.add_url_rule('/author/<timeperiod>/<id>/', view_func=author_api)