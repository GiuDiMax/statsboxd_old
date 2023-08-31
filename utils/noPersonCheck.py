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
    npCheck([1116586, 2791228, 351940, 886225, 1989996, 1463691, 443811, 1117534, 1116587, 1187723, 1463686, 801410, 629260, 1116586, 875154, 1367043])
    #2791228