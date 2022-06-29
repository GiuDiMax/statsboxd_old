from mongodb import db
from config import *
from jsonoOpAllTime import json_operations

def getStats():
    # db.Users.update_one({'username': username}, {'$set': {'a': 'b'}})

    json_op1 = [
                {'$match': {"_id": '$$username'}},
                {'$unwind': '$watched'},
                {'$lookup': {
                    'from': 'Film',
                    'localField': 'watched.id',
                    'foreignField': '_id',
                    'as': 'info'}},
                {'$unwind': '$info'},
                {'$facet': json_operations},
    ]

    json_op2 = [{'$map': {'input': ['giudimax','ale_ich'], 'as': 'username', 'in': json_op1}}]


    db.command({
        "create": "alltimestats",
        "viewOn": "Users",
        "pipeline": json_op1
    })


    #ob3 = db.Users.aggregate(json_op2)

    #for x in ob3:
    #    print(x)


'''
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
'''

        #db.Users.update_one({'username': username}, {'$set': {'stats': y}})

getStats()
