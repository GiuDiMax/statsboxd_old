from mongodb import db
from time import time


def test():
    start = time()
    obj = list(db.Users.aggregate([
        {'$match': {'_id': 'giudimax'}},
        {'$unwind': '$watched'},
        {'$group': {'_id': '$watched.id'}},
        {'$lookup': {'from': 'Film', 'localField': '_id', 'foreignField': '_id', 'as': 'info'}},
        {'$project': {'_id': 0, 'uri': '$info.uri', 'ad': '$info.actors'}},
        {'$unwind': '$uri'},
        {'$unwind': '$ad'},
        {'$unwind': '$ad'},
        {'$group': {'_id': '$ad', 'sum': {'$sum': 1}, 'list': {'$push': '$uri'}}},
        {'$sort': {'sum': -1}},
        {'$limit': 10}
    ]))
    print(obj)
    print(time()-start)


if __name__ == '__main__':
    test()
