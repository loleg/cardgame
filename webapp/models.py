# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'
import datetime
from flask import url_for
from webapp import db


class Card(db.Document):
    meta = {'collection': '1940 gestorben'}


