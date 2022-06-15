from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb

def refresh():
    a = db.Film.aggregate([
        {'$match': {'runtime': {'$exists': False}}},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])

    print(len(uris))
    fillMongodb(uris)


if __name__ == '__main__':
    refresh()
