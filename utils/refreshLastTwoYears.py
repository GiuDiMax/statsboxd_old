from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb


def refresh():
    datex = datetime.today()
    datex = datex - timedelta(days=7)

    current_year = date.today().year
    a = db.Film.aggregate([
        #{'$match': {"year": {'$gt': current_year - 2}}},
        # {'$match': {"updateDate": {'$lt': datex}}},

        {'$sort': {'updateDate': 1}},
        {'$limit': 1000},

        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])

    fillMongodb(uris)


def refreshata():
    try:
        refresh()
    except:
        refreshata()


if __name__ == '__main__':
    for i in range(25):
        refreshata()
        print('1000 done')
