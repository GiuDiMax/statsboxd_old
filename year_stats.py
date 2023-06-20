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


json_operations_extra = {}
json_operations_extra['streak'] = [
                {'$project': {'sett': {'$sum': [{'$week': '$diary.date'}, {'$multiply': [{'$year': '$diary.date'}, 53]}]}}},
                {'$group': {'_id': '$sett'}},
                #{'$project': {'s': {'$week': '$diary.date'}, 'y': {'$year': '$diary.date'}}},
                #{'$group': {'sett': '$sett', 'year': '$year'}},
                #{'$sort': {'y': 1, 's': 1}}
                {'$sort': {'_id': 1}}
                ]

json_operations_extra['2+filmdays'] = [
            {'$group': {'_id': '$diary.date', 'count': {'$count': {}}}},
            {'$match': {'count': {'$gt': 1}}},
            {'$group': {'_id': None, 'count': {'$count': {}}}},
            {'$project': {'_id': 0, 'count': '$count'}}
            ]


def getYears(username):
    global json_operations4
    ob3 = db.Users.aggregate([
        {'$match': {"_id": username}},
        {'$unwind': '$diary'},
        {'$project': {'diary': '$diary', 'year': {'$year': '$diary.date'}}},
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
    miles = []
    z = int(len(y['milestones'])/50)
    for i in range(z):
        miles.append(y['milestones'][((i+1)*50)-1])
    y['milestones'] = miles
    #print(y['totalcountry'])
    db.Users.update_one({'_id': username}, {'$set': {'stats_'+str(year): y}})


def year_stats(username, fastUpdate=False):
    k = {}
    k['years'] = []
    a = getYears(username)
    threads = []
    years = []
    for y in a:
        k = y
    aa = list(k['years'])
    aa.reverse()
    bb = []
    for y in aa:
        if len(bb) == 0:
            bb.append(y)
        else:
            while True:
                if y['_id'] == bb[-1]['_id'] + 1:
                    bb.append(y)
                    break
                else:
                    bb.append({'_id': bb[-1]['_id']+1, 'sum': 0})

    db.Users.update_one({'_id': username}, {'$set': {'extra_stats.diaryperyear': bb}})
    if fastUpdate:
        singleYear(datetime.now().year, username)
    else:
        db.Users.update_one({'_id': username}, {'$set': {'mostWatched': k['mostWatched']}})
        for x in k['years']:
            if x['sum'] >= 25:
                years.append(x['_id'])
                t = Thread(target=singleYear, args=(x['_id'], username))
                threads.append(t)
        for x in threads:
            x.start()
        for x in threads:
            x.join()

        db.Users.update_one({'_id': username}, {'$set': {'years': years}})

    #STREAK E 2PERDAYS
    json_op1 = [{'$match': {"_id": username}},
                {'$unwind': '$diary'},
                {'$facet': json_operations_extra}]
    ob3 = db.Users.aggregate(json_op1)
    for x in ob3:
        y = x
    max = 0
    currentd = 0
    current = 0
    maxdatmin = 0
    mmdm = 0
    for x in y['streak']:
        #print(x['_id'])
        year = (int(x['_id'] / 53))
        month = (x['_id'] % 53) / 4
        #print(year)
        #print(month)
        #print("-------")
        if x['_id'] == currentd + 1:
            current = current + 1
        else:
            if current > max:
                max = current
                mmdm = maxdatmin
            maxdatmin = x['_id']
            current = 0
        currentd = x['_id']
    if current > max:
        max = current
        mmdm = maxdatmin
    #print(mmdm)
    year = (int(mmdm / 53))
    month = (mmdm % 53) / 4
    #print(year)
    #print(month)
    if month % 1 > 0:
        month = int(month)
    else:
        month = int(month) - 1
    if month > 13:
        month = 1
        year = year + 1
    y['streak'] = {'max': max, 'year': year, 'month': month}
    #print(y['streak'])
    db.Users.update_one({'_id': username}, {'$set': {'extra_stats.streak': y['streak'], 'extra_stats.2+filmdays': y['2+filmdays'][0]}})


if __name__ == '__main__':
    year_stats('orekkyy', False)
    pass
