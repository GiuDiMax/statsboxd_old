from mongodb import db
from datetime import date, timedelta, datetime

def refresh():
    datex = datetime.today()
    datex = datex - timedelta(days=7)

    current_year = date.today().year
    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - 2}}},
        {'$match': {"updateDate": {'$lt': datex}}},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])

    print(len(uris))
    fillMongodb(uris)


if __name__ == '__main__':
    refresh()