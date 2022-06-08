from mongodb import db
from config import *
from datetime import datetime, timedelta
from threading import Thread
import time
from jsonOpYear import json_operations


def getYears(username):
    ob3 = db.Users.aggregate([
        {'$match': {"_id": username}},
        #{'$project': {'_id': None, 'diary': '$diary'}},
        {'$unwind': '$diary'},
        #{'$unwind': '$info'},
        {'$project': {'diary': '$diary', 'year': {'$year': '$diary.date'}}},
        {'$group': {'_id': '$year', 'sum': {'$sum': 1}}},
        #{'$unwind': '$list.diary.info.actors'},
        #{'$group': {'_id': '$list.info.actors', 'sum': {'$sum': 1}}},
        #{'$facet': json_operations},
    ])
    return ob3


def singleYear(year, username):
    ob3 = db.Users.aggregate([
        {'$match': {"_id": username}},
        {'$unwind': '$diary'},
        {'$project': {'diary': '$diary', 'year': {'$year': '$diary.date'}}},
        {'$match': {"year": {'$eq': year}}},
        {'$lookup': {
            'from': 'Film',
            'localField': 'diary.id',
            'foreignField': '_id',
            'as': 'info'}},
        {'$unwind': '$info'},
        {'$facet': json_operations},
    ])
    y = {}
    for x in ob3:
        y = x
        break
    db.Users.update_one({'_id': username}, {'$set': {'stats_'+str(year): y}})


def year_stats(username):
    a = getYears(username)
    #y = {}
    threads = []
    #for x in a:
    #    y = a
    #    break
    for x in a:
        if x['sum'] > 10:
            t = Thread(target=singleYear, args=(x['_id'], username))
            threads.append(t)
    for x in threads:
        x.start()
    for x in threads:
        x.join()
