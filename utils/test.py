from mongodb import db
from time import time


def test():
    start = time()
    obj = list(db.Users.aggregate([
        {'$match': {'_id': 'giudimax'}},
        {'$project': {'watched': 1}},
        {'$unwind': '$watched'},
        {'$project': {'_id': '$watched.id'}},
        {'$lookup': {'from': 'Film',
                     'localField': '_id',
                     'foreignField': '_id',
                     'as': 'info'}},
        {'$project': {'_id': 1, 'uri': '$info.uri', 'studio': '$info.studio', 'r': '$info.rating.average'}},
        {'$unwind': '$uri'},
        {'$unwind': '$studio'},
        {'$match': {'studio': 'warner-bros-pictures-1'}},
        {'$sort': {'r': -1}},
        {'$project': {'_id': '$uri'}}
    ]))
    print(obj)
    print(len(obj))
    print(time() - start)


if __name__ == '__main__':
    test()
