from mongodb import db
from config import *
from jsonoOpAllTime import json_operations

def getStats(username):
    # db.Users.update_one({'username': username}, {'$set': {'a': 'b'}})

    ob3 = db.Users.aggregate([
        {'$match': {"username": username}},
        {'$unwind': '$watched'},
        {'$lookup': {
            'from': 'Film',
            'localField': 'watched.id',
            'foreignField': '_id',
            'as': 'info'}},
        {'$unwind': '$info'},
        {'$facet': json_operations},
    ])
    return ob3
