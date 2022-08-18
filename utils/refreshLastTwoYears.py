from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb
import time


def refresh():
    datex = datetime.today()
    datex = datex - timedelta(days=10)
    #datex = datex - timedelta(days=1)

    current_year = date.today().year
    a = db.Film.aggregate([
        #{'$match': {"year": {'$gt': current_year - 2}}},
        {'$match': {"updateDate": {'$lt': datex}}},
        {'$sort': {'updateDate': 1}},
        {'$limit': 1000},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    #print(uris)
    print(len(uris))
    fillMongodb(uris)


def refreshata():
    try:
        refresh()
    except:
        time.sleep(100)
        refreshata()


if __name__ == '__main__':
    for i in range(50):
        start = time.time()
        refreshata()
        #refresh()
        print('Done in ' + str(time.time() - start))
