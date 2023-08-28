from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb, fillMongodbmembers, fillMongodbratings
import time
from setLists import updateLists
from setPeople import mainSetNames, mainSetNames2, mainSetNamesExt
from setCollections import mainSetCollection2
from setThemes import all
from cleanUsers import cleanUsers
import random

limitx = 100
hx = 5 #ore


def refresh(i, nn):
    b = False
    datex = datetime.today()
    datex = datex - timedelta(hours=hx)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {'$or':[{"year": {'$gt': current_year - nn}}, {'year': {'$exists': False}}]}},
        {'$match': {"updateDate": {'$lt': datex}}},
        {'$sort': {'updateDate': 1}},
        {'$limit': limitx},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        #print(x)
        uris.append(x['uri'])
    random.shuffle(uris)
    #print(len(uris))
    #exit()
    if len(uris)<limitx:
        b = True
    print('analyizing data ' + str(len(uris) + i*limitx))
    fillMongodb(uris)
    return b


def addMembers(i, nn):
    b = False
    datex = datetime.today()
    datex = datex - timedelta(hours=hx)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - nn}}},
        {'$match': {'$or': [{"updateMembers": {'$lt': datex}}, {'updateMembers': {'$exists': False}}]}},
        #{'$match': {'members': {'$exists': False}}},
        {'$sort': {'updateMembers': 1}},
        {'$limit': limitx},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    #print(len(uris))
    if len(uris)<limitx:
        b = True
    print('analyzing members ' + str(len(uris) + i*limitx))
    fillMongodbmembers(uris)
    return b


def addRatings(i, nn):
    b = False
    datex = datetime.today()
    datex = datex - timedelta(hours=hx)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - nn}}},
        {'$match': {'$or': [{"updateRating": {'$lt': datex}}, {'updateRating': {'$exists': False}}]}},
        #{'$match': {'ratings': {'$exists': False}}},
        {'$sort': {'updateRating': 1}},
        {'$limit': limitx},
        {'$project': {'uri': 1}}
    ])
    uris = []
    for x in a:
        uris.append(x['uri'])
    #print(len(uris))
    #exit()
    if len(uris)<limitx:
        b = True
    print('analyizing ratings ' + str(len(uris) + i*limitx))
    fillMongodbratings(uris)
    return b


def refreshata(i, k, nn):
    b = False
    try:
        if k == 0:
            b = refresh(i, nn)
        elif k == 1:
            b = addMembers(i, nn)
        elif k == 2:
            b = addRatings(i, nn)
    except:
        time.sleep(15)
        b = refreshata(i, k, nn)
    return b


if __name__ == '__main__':
    nn = 999 #last x years
    for k in range(0, 3):
        for i in range(int(90000/limitx)+1):
            b = refreshata(i, k, nn)
            if b: break
    x = db.Film.delete_many({'modifiedDate': {'$exists': False}})
    print("deleted: " + str(x.deleted_count))
    all()
    updateLists()
    mainSetNames2()
    mainSetNamesExt()
    mainSetCollection2()
    cleanUsers()
    print("FINE")
