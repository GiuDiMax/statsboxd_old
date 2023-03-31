from mongodb import db
from time import time

def test():
    start = time()
    visti = []
    obj = db.Users.aggregate([
        {'$match': {'_id': 'giudimax'}},
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
        {'$limit': 47}
    ])
    for x in obj:
        print(x)
    print(time()-start)


if __name__ == '__main__':
    test()