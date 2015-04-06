# -*- coding:utf-8 -*-
__author__ = u'Joël Vogt'

cimport cython

from pymongo.collection import Collection
from pymongo.database import Database

from webapp import pymongo_client, DB_NAME


cdef list exclude_collections = ['system.indexes']

def mongo_to_dict(dict object):
    cdef str _id = '_id'
    if _id in object:
        object['_id'] = str(object['_id'])
    return object

def get_collection_names():
    _db = pymongo_client[DB_NAME]
    cdef:
        list collection_names = _db.collection_names()
        str collection
        list result = []
    for collection in collection_names:
        if collection not in exclude_collections:
            result.append(collection)

    return result

def get_collection(str collection, dict projection=None):
    _db = pymongo_client[DB_NAME]
    cdef:
        list collections = get_collection_names()
        tuple find_args
        str _collection
        list results = []
        dict result = {}
        dict db_object
    if projection:
        find_args = (projection)
    else:
        find_args = ()
    if collection is None or collection == 'all':

        for _collection in collections:
            result[_collection] = _db[_collection].find(*find_args)
    elif collection in collections:
        for db_object in _db[collection].find(*find_args):
            results.append(db_object)
    return results