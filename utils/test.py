from mongodb import db
from time import time


def test():
    start = time()
    obj = list(db.Users.aggregate([
        {'$project': {'_id': 1, 'update': 1, 'fullUpdate': 1}},
        {'$sort': {'update': -1}}
    ]))
    print(obj)
    print(time() - start)


if __name__ == '__main__':
    test()
