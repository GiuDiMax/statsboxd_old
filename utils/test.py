from mongodb import db
from time import time


def test():
    start = time()
    obj = list(db.Film.aggregate([
        {'$match': {'runtime': {'$exists': False}}},
        {'$project': {'_id': '$uri'}}
    ]))
    print(obj)
    print(time() - start)


if __name__ == '__main__':
    test()
