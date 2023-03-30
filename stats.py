from mongodb import db
#from config import *
from jsonoOpAllTime import json_operations
from datetime import datetime
from time import time


def getStats(username, fastUpdate=False):
    # db.Users.update_one({'username': username}, {'$set': {'a': 'b'}})
    jop = json_operations
    if fastUpdate:
        del jop['sug2']
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
        pass
        #print(y)
        #print(y['test'])
        #print(y['mostWatchedlanguage'])

    #y['2+filmdays'] = y['2+filmdays'][0]

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

        db.Users.update_one({'_id': username}, {'$set': {'stats': y, 'update': datetime.today()}})
        #print(y['mostWatchedgenres_nanogenre'])


if __name__ == '__main__':
    start = time()
    getStats('giudimax', True)
    print(time()-start)
