from mongodb import db
from datetime import date, timedelta, datetime
from operations import fillMongodb


def refresh():
    a = db.Users.aggregate([
        {'$match': {"_id": 'alexmod1'}},
        {'$unwind': '$watched'},
        {'$lookup': {
            'from': 'Film',
            'localField': 'watched.id',
            'foreignField': '_id',
            'as': 'info'}},
        {'$unwind': '$info'},
        {'$match': {'info.runtime': {'$exists': False}}},
        {'$group': {'_id': '$_id',
                    'movies': {'$sum': 1},
                    'runtime': {'$sum': '$info.runtime'}}}
    ])

    for x in a:
        print(x)


if __name__ == '__main__':
    refresh()
