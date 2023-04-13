from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb, fillMongodbmembers, fillMongodbratings
import time
from setLists import updateLists
from setPeople import mainSetNames
from setCollections import mainSetCollection2
from setThemes import all
from cleanUsers import cleanUsers

limitx = 100
hx = 24 #ore


def refresh(i, nn):
    b = False
    datex = datetime.today()
    datex = datex - timedelta(hours=24)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - nn}}},
        {'$match': {"updateDate": {'$lt': datex}}},
        {'$sort': {'updateDate': 1}},
        {'$limit': limitx},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    if len(uris)<limitx:
        b = True
    print('analyizing data ' + str(len(uris) + i*limitx))
    fillMongodb(uris)
    return b


def addMembers(i, nn):
    b = False
    datex = datetime.today()
    datex = datex - timedelta(hours=24)
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
    if len(uris)<limitx:
        b = True
    print('analyzing members ' + str(len(uris) + i*limitx))
    fillMongodbmembers(uris)
    return b


def addRatings(i, nn):
    b = False
    datex = datetime.today()
    datex = datex - timedelta(hours=24)
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
    nn = 1 #last x years
    for k in range(3):
        for i in range(int(80000/limitx)+1):
            #start = time.time()
            b = refreshata(i, k, nn)
            if b: break
            #print('Done in ' + str(time.time() - start))

    #exit()
    all()
    updateLists()
    mainSetNames()
    mainSetCollection2()
    cleanUsers()
    print("FINE")
