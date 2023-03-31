from mongodb import db
from time import time


def sug2statsx(username):
    start = time()
    visti = []
    obj = db.Users.aggregate([
        {'$match': {'_id': username}},
        {'$unwind': '$watched'},
        {'$match': {'watched.rating': {'$gt': 0}}},
        {'$project': {'_id': '$watched.id'}},
        {'$group': {'_id': None, 'visti': {'$push': '$_id'}}}
    ])
    for x in obj:
        visti = x['visti']
        break
    if len(visti) == 0:
        return
    obj = db.Users.aggregate([
        {'$match': {'_id': 'giudimax'}},
        {'$unwind': '$watched'},
        {'$match': {'watched.rating': {'$gt': 0}}},
        {'$project': {'_id': '$watched.id', 'rate': '$watched.rating'}},
        {'$lookup': {
            'from': 'Film',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}
        },
        {'$project': {'_id': 1, 'rate': 1, 'similar': '$info.related'}},
        {'$unwind': '$similar'},
        {'$unwind': '$similar'},
        {'$match': {'similar': {'$nin': visti}}},
        {'$group': {'_id': '$similar', 'avg': {'$avg': '$rate'}, 'count': {'$sum': 1}}},
        {'$match': {'count': {'$gt': 1}}},
        {'$sort': {'avg': -1}},
        {'$limit': 50},
        {'$lookup': {
            'from': 'Film',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}
        },
        {'$unwind': '$info'},
        {'$project': {'_id': 1, 'perc': {'$toInt': {'$multiply': ['$avg', 10]}}, 'uri': '$info.uri', 'poster': '$info.images.poster'}}
    ])
    y = []
    for x in obj:
        y.append(x)
    db.Users.update_one({'_id': username}, {'$set': {'sug2': y}})


if __name__ == '__main__':
    sug2statsx('giudimax')
