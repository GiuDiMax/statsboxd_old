from mongodb import db
from time import time


def test():
    start = time()
    obj = list(db.Film.aggregate([
        {'$match': {'year': 2022}},
        {'$project': {'_id': 1}}
    ]))
    print(len(obj))
    print(time() - start)


if __name__ == '__main__':
    test()
