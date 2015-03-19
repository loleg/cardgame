# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'
import datetime
from flask import url_for
from webapp import db


class Author(db.Document):
    format = db.URLField(db_field='Format')
    archive = db.URLField(db_field='Archiv')
    category_author = db.StringField(db_field='Kategorie Autor')
    name = db.StringField(db_field='Name')
    died = db.StringField(db_field='Todesdatum')
    died_in = db.StringField(db_field='Gestorben in')
    description = db.StringField(db_field='Beschreibung')
    category_work = db.StringField(db_field='Kategorie Werk')
    uri = db.URLField(db_field='URI')
    work = db.StringField(db_field='Werk')


