import time
from mongodb import db
from config import *
from stats import getStats, getLists
from username import getFromusername
from operations import fillMongodb
from setPeople import mainSetNames2
from username import get_watched


def fullCreation(username):
    watched_list = get_watched(username, False)
    diary_list = get_watched(username, True)
    db.Users.insert_one({'username': username, 'watched': watched_list, 'diary': diary_list})
    fullUpdate(username)


def fullUpdate(username):
    start_time = time.time()
    username_object = getFromusername(username)
    watched = username_object['watched']
    ids = []
    uris = []
    for movie in watched:
        ids.append(movie['id'])
        uris.append(movie['uri'])

    db.tmpUris.delete_many({})
    db.tmpUris.insert_many(username_object['watched'])

    while True:
        obj1 = db.Film.find({"_id": {"$in": ids}})
        uris2 = list(set(uris) - set(obj1.distinct('uri')))
        print(len(uris2))
        if len(uris2) > 0:
            try:
                fillMongodb(uris2)
            except:
                pass
        else:
            break

    print('names')
    #mainSetNames2()
    json3 = getStats(username)
    for x in json3:
        y = x

    min = y['totalyear'][0]['_id']
    max = y['totalyear'][-1]['_id']


    y2 = []
    for i in range(min, max + 1):
        check = False
        for a in y['totalyear']:
            if a['_id'] == i:
                y2.append(a)
                check = True
                break
        if not check:
            y2.append({'_id': i, 'average': 0, 'sum': 0})
    y['totalyear'] = y2

    x = []
    json4 = getLists()
    for i in json4:
        x.append(i)
    y = y | {'lists': x}
    db.Users.update_one({'username': username}, {'$set': {'stats': y}})
    print(time.time() - start_time)
