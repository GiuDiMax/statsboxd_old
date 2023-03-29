from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb, fillMongodbmembers
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
    print('analyizing ' + str(len(uris) + i*1000))
    fillMongodb(uris)


def refreshata(i):
    try:
        refresh(i)
    except:
        time.sleep(10)
        refreshata(i)


def addMembers(i):
    datex = datetime.today()
    #datex = datex - timedelta(days=10)
    datex = datex - timedelta(hours=24)
    current_year = date.today().year

    a = db.Film.aggregate([
        {'$match': {"members": {'$exists': 0}}},
        {'$sort': {'updateDate': 1}},
        {'$limit': 1000},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    print('analyizing ' + str(len(uris) + i*1000))
    fillMongodbmembers(uris)


def refreshata2(i):
    try:
        addMembers(i)
    except:
        time.sleep(10)
        refreshata2(i)


if __name__ == '__main__':
    for i in range(78):
        start = time.time()
        refreshata(i)
        print('Done in ' + str(time.time() - start))

    for i in range(50):
        start = time.time()
        refreshata2(i)
        print('Done in ' + str(time.time() - start))

    all()
    updateLists()
    mainSetNames()
    mainSetCollection2()
    cleanUsers()
    print("FINE")
