from mongodb import db
from config import *
from jsonoOpAllTime import json_operations


def getStats(username):
    # db.Users.update_one({'username': username}, {'$set': {'a': 'b'}})

    json_op1 = [{'$match': {"_id": username}},
                {'$unwind': '$watched'},
                {'$lookup': {
                    'from': 'Film',
                    'localField': 'watched.id',
                    'foreignField': '_id',
                    'as': 'info'}},
                {'$unwind': '$info'},
                {'$facet': json_operations}]


    ob3 = db.Users.aggregate(json_op1)

    y = None
    for x in ob3:
        y = x
    if __name__ == '__main__':
        print(y['test'])

    if y != None:
        min = y['totalyear'][0]['_id']
        max = y['totalyear'][-1]['_id']

        y2 = []
        for i in range(min, max + 1):
            check = False
            for a in y['totalyear']:
                if a['_id'] == i:
                    y2.append(a)
                    check = True
                    break
            if not check:
                y2.append({'_id': i, 'average': 0, 'sum': 0})
        y['totalyear'] = y2
        db.Users.update_one({'_id': username}, {'$set': {'stats': y}})


if __name__ == '__main__':
    getStats('giudimax')
