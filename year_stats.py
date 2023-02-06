from mongodb import db
from config import *
from datetime import datetime, timedelta
from threading import Thread
import time
from jsonOpYear import json_operations

global json_operations4

json_operations4 = {}
op_role = []
op_role.append({'$group': {'_id': '$diary.id', 'num': {'$sum': 1}}})
op_role.append({'$match': {"num": {'$gt': 1}}})
op_role.append({'$sort': {'num': -1}})
op_role.append({'$limit': 50})
op_role.append({'$lookup': {
                'from': 'Film',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
op_role.append({'$unwind': '$info'})
op_role.append({'$sort': {'info.rating.num': -1}})
op_role.append({'$sort': {'num': -1}})
op_role.append({'$limit': 18})
op_role.append({'$project': {'_id': '$_id', 'uri': '$info.uri', 'sum': '$num', 'poster': '$info.images.poster'}})
json_operations4['mostWatched'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$year', 'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': -1}})
json_operations4['years'] = op_role


def getYears(username):
    global json_operations4
    ob3 = db.Users.aggregate([
        {'$match': {"_id": username}},
        #{'$project': {'_id': None, 'diary': '$diary'}},
        {'$unwind': '$diary'},
        #{'$unwind': '$info'},
        {'$project': {'diary': '$diary', 'year': {'$year': '$diary.date'}}},
        #{'$unwind': '$list.diary.info.actors'},
        #{'$group': {'_id': '$list.info.actors', 'sum': {'$sum': 1}}},
        {'$facet': json_operations4},
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


def year_stats(username, fastUpdate):
    a = getYears(username)
    #y = {}
    threads = []
    #for x in a:
    #    y = a
    #    break
    years = []
    for y in a:
        k = y
    if fastUpdate:
        singleYear(datetime.now().year, username)
        #if datetime.now().month == 1:
        #    singleYear(datetime.now().year - 1, username)
    else:
        db.Users.update_one({'_id': username}, {'$set': {'mostWatched': k['mostWatched']}})
        for x in k['years']:
            if x['sum'] >= 50:
                years.append(x['_id'])
                t = Thread(target=singleYear, args=(x['_id'], username))
                threads.append(t)
        for x in threads:
            x.start()
        for x in threads:
            x.join()
    #years.sort(reverse=True)
        db.Users.update_one({'_id': username}, {'$set': {'years': years}})

#singleYear(2022, 'giudimax')
#year_stats('giudimax')