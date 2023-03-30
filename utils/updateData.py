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


def refresh(i, nn):
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
    print('analyizing data' + str(len(uris) + i*limitx))
    fillMongodb(uris)


def addMembers(i, nn):
    datex = datetime.today()
    datex = datex - timedelta(hours=24)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - nn}}},
        {'$match': {'$or': [{"updateMembers": {'$lt': datex}}, {'updateMembers': {'$exists': False}}]}},
        {'$sort': {'updateMembers': 1}},
        {'$limit': limitx},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    print('analyzing members ' + str(len(uris) + i*limitx))
    fillMongodbmembers(uris)


def addRatings(i, nn):
    datex = datetime.today()
    datex = datex - timedelta(hours=24)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - nn}}},
        {'$match': {'$or': [{"updateRating": {'$lt': datex}}, {'updateRating': {'$exists': False}}]}},
        {'$sort': {'updateRating': 1}},
        {'$limit': limitx},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    print('analyizing ratings ' + str(len(uris) + i*limitx))
    fillMongodbratings(uris)


def refreshata(i, k, nn):
    try:
        if k == 0:
            refresh(i, nn)
        elif k == 1:
            addMembers(i, nn)
        elif k == 2:
            addRatings(i, nn)
    except:
        time.sleep(15)
        refreshata(i, k, nn)


if __name__ == '__main__':
    nn = 99 #last x years
    for k in range(1, 3):
        for i in range(int(80000/limitx)+1):
            #start = time.time()
            refreshata(i, k, nn)
            #print('Done in ' + str(time.time() - start))

    exit()
    all()
    updateLists()
    mainSetNames()
    mainSetCollection2()
    cleanUsers()
    print("FINE")
