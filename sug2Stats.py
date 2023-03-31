from mongodb import db
#from time import time

json_operations = {}
json_operations['sug2'] = [
    {'$match': {'count': {'$gt': 1}}},
    {'$sort': {'avg': -1}},
    {'$limit': 50},
    {'$lookup': {
        'from': 'Film',
        'localField': '_id',
        'foreignField': '_id',
        'as': 'info'}
    },
    {'$unwind': '$info'},
    {'$project': {'_id': 1, 'perc': {'$toInt': {'$multiply': ['$avg', 10]}}, 'uri': '$info.uri', 'poster': '$info.images.poster'}}
]
"""
json_operations['sug3'] = [
    {'$lookup': {
        'from': 'Users',
        'localField': 'user',
        'foreignField': '_id',
        'let': {'movie_id': "$_id"},
        'pipeline': [{'$unwind': '$sug_list'},
                     {'$project': {'_id': '$sug_list._id', 'perc': '$sug_list.perc'}},
                     {'$match': {'_id': '$$movie_id'}}
                     ],
        'as': 'sugx'}},
    #{'$match': {'sugx': {'$ne': []}}}
]
"""

def sug2statsx(username):
    visti = []
    obj = db.Users.aggregate([
        {'$match': {'_id': username}},
        {'$unwind': '$watched'},
        {'$match': {'watched.rating': {'$gt': 0}}},
        {'$project': {'_id': '$watched.id'}},
        {'$group': {'_id': None, 'visti': {'$push': '$_id'}}}
    ])
    for x in obj:
        visti = x['visti']
        break
    if len(visti) == 0:
        return
    obj = db.Users.aggregate([
        {'$match': {'_id': 'giudimax'}},
        {'$unwind': '$watched'},
        {'$match': {'watched.rating': {'$gt': 0}}},
        {'$project': {'_id': '$watched.id', 'rate': '$watched.rating', 'user': '$_id'}},
        {'$lookup': {
            'from': 'Film',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}
        },
        {'$project': {'_id': 1, 'rate': 1, 'similar': '$info.related', 'user': 1}},
        {'$unwind': '$similar'},
        {'$unwind': '$similar'},
        {'$match': {'similar': {'$nin': visti}}},
        {'$group': {'_id': '$similar', 'avg': {'$avg': '$rate'}, 'count': {'$sum': 1}, 'user': {'$first': '$user'}}},
        {'$facet': json_operations},
    ])
    a = None
    for x in obj:
        a = x
        break
    if a is not None:
        db.Users.update_one({'_id': username}, {'$set': {'sug2': a['sug2']}})


if __name__ == '__main__':
    sug2statsx('giudimax')
