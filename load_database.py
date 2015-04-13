#!/usr/local/bin/python3
import pandas as pd
import numpy as np
from pymongo import MongoClient

timeperiods = pd.ExcelFile('/Users/joelvogt/Documents/NEU Werke von Autoren gestorben 1940-45.xlsx')
database_name = 'publicdomaingame'

print('\n\nlogin to %s \n' % database_name)
user = input('> user: ')
password = input('> password: ')

client = MongoClient(host='mongodb://%(user)s:%(password)s@ds039211.mongolab.com:39211/%(database)s' %
                          dict(database=database_name,
                               user=user,
                               password=password))

db = client[database_name]
for timeperiod_name in timeperiods.sheet_names:
    collection = db[timeperiod_name]
    timeperiod = timeperiods.parse(timeperiod_name)
    timeperiod = timeperiod[list(filter(lambda x: 'Unnamed' not in x, timeperiod.columns))]
    valid_entries = filter(lambda x: not (all(pd.isnull(x))), timeperiod.get_values())

    for entry in map(lambda artifact: dict(zip(timeperiod.columns, artifact.tolist())), valid_entries):
        for prop in entry:
            if pd.isnull(entry[prop]):
                entry[prop] = None
        print(entry)
        collection.insert(entry)
