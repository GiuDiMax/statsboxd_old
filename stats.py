from mongodb import db
from jsonoOpAllTime import json_operations
from datetime import datetime
from time import time


def getStats(username):
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
        #print(y)
        db.Users.update_one({'_id': username}, {'$set': {'stats': y, 'update': datetime.today()}})


if __name__ == '__main__':
    start = time()
    #getStats('giudimax')
    print(time()-start)
