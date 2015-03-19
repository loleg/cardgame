#!/usr/local/bin/python3
import pandas as pd
import numpy as np
from pymongo import MongoClient

timeperiods = pd.ExcelFile('NEU Werke von Autoren gestorben 1940-45.xlsx')
collection = None
client = MongoClient()
db = client.cardgame
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
