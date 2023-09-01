from mongodb import db
from config import *


def npCheck(uris):
    a = []
    for field in field2:
        x = list(db.Film.aggregate([
            {'$match': {field: {'$in': uris}}},
            {'$project': {'_id': '$uri'}}
        ]))
        for y in x:
            if y['_id'] not in a:
                a.append(y['_id'])
    print(a)


if __name__ == '__main__':
    npCheck([1116586, 2791228, ])
    #2791228