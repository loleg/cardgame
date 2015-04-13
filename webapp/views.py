# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'

import pyximport;

pyximport.install()
from webapp.helpers.dblib import mongo_to_dict, get_collection_names, get_collection

from flask import Blueprint, render_template, request
from flask.views import MethodView, View
from bson.json_util import dumps, ObjectId, json
from flask.ext.mongoengine.wtf import model_form

from webapp import pymongo_client, DB_NAME
from webapp.models import Author

cards_blueprint = Blueprint('cards', __name__, template_folder='templates')


class AuthorAPI(MethodView):
    def get(self, timeperiod, id):
        collection = pymongo_client[DB_NAME][timeperiod]
        _id = ObjectId(id)
        author = collection.find_one(dict(_id=_id), dict(_id=False))
        return dumps(author)

    def put(self, timeperiod, id):
        property_value = request.get_data()
        property, value = json.loads(property_value.decode())
        collection = pymongo_client[DB_NAME][timeperiod]
        _id = ObjectId(id)
        author = collection.find_one(dict(_id=_id))
        author[property] = value
        collection.update({u'_id': _id}, {"$set": author}, upsert=False)
        return dumps(author)

    def post(self, timeperiod):
        _db = pymongo_client[DB_NAME]
        collection = _db[timeperiod]
        new_entry = json.loads(request.get_data().decode())
        entry = collection.find_one(new_entry)
        if entry:
            return 'author already exists {0}'.format(entry), 401
        else:
            return 'Inserted new Author with id {0} to collection {1}'.format(collection.insert_one(), timeperiod), 200




class TimePeriodAPI(MethodView):
    def get(self, period):
        periods = get_collection(period)
        if periods:
            status = 200
        else:
            status = 404
        properties = Author()._db_field_map.values()
        return dumps(dict(timeperiod=map(mongo_to_dict, periods), properties=list(properties))), status


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
    def __init__(self, template):
        self.template = template

    def get(self):
        form = model_form(Author)
        return render_template(self.template, **dict(form=form(request.form)))


class TimePeriodView(AbstractView):
    def get_objects(self):
        schema_fields = Author()._db_field_map.values()
        collections = get_collection_names()
        return list(schema_fields), collections

    def dispatch_request(self):
        titles, collections = self.get_objects()
        context = dict(titles=titles, timeperiods=json.dumps(collections), init=collections[0])
        return self.render_template(context)


period_api = TimePeriodAPI.as_view('timeperiod')
author_api = AuthorAPI.as_view('author')

cards_blueprint.add_url_rule('/author_form/', view_func=FormView.as_view('form', template='author_form.html'))
cards_blueprint.add_url_rule('/', view_func=TimePeriodView.as_view('index', template='index.html'))
cards_blueprint.add_url_rule('/timeperiod/<period>/', view_func=period_api)
cards_blueprint.add_url_rule('/<timeperiod>/<id>/', view_func=author_api)
cards_blueprint.add_url_rule('/author/<timeperiod>/', view_func=author_api)
