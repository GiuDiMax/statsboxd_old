from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb, fillMongodbmembers, fillMongodbratings
import time
from setLists import updateLists
from setPeople import mainSetNames
from setCollections import mainSetCollection2
from setThemes import all
from cleanUsers import cleanUsers


def refresh(i):
    datex = datetime.today()
    #datex = datex - timedelta(days=10)
    datex = datex - timedelta(hours=24)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - 2}}},
        {'$match': {"updateDate": {'$lt': datex}}},
        {'$sort': {'updateDate': 1}},
        {'$limit': 1000},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    print('analyizing data' + str(len(uris) + i*1000))
    fillMongodb(uris)


def addMembers(i):
    a = db.Film.aggregate([
        {'$sort': {'updateMembers': 1}},
        {'$limit': 1000},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    print('analyzing members ' + str(len(uris) + i*1000))
    fillMongodbmembers(uris)


def addRatings(i):
    a = db.Film.aggregate([
        {'$sort': {'updateRating': 1}},
        {'$limit': 1000},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    print('analyizing ratings ' + str(len(uris) + i*1000))
    fillMongodbratings(uris)


def refreshata(i, k):
    try:
        if k == 0:
            refresh(i)
        elif k == 1:
            addMembers(i)
        elif k == 2:
            addRatings(i)
    except:
        time.sleep(10)
        refreshata(i, k)


if __name__ == '__main__':
    for k in range(1, 3):
        for i in range(78):
            start = time.time()
            refreshata(i, k)
            print('Done in ' + str(time.time() - start))

    exit()
    all()
    updateLists()
    mainSetNames()
    mainSetCollection2()
    cleanUsers()
    print("FINE")
