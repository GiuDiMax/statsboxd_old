from mongodb import db
from config import *

def getStats(username):
    # db.Users.update_one({'username': username}, {'$set': {'a': 'b'}})

    json_operations = {}

    for field in field2+field3:
        op_role = []
        op_role.append({'$unwind': '$info.'+field})
        op_role.append({'$group': {'_id': '$info.'+field,
                                   'average': {'$avg': '$watched.rating'},
                                   'sum': {'$sum': 1}}})
        op_role.append({'$sort': {'sum': -1}})
        op_role.append({'$limit': 20})
        if field in field2:
            op_role.append({'$lookup': {
                'from': 'People',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
        json_operations['mostWatched'+field.replace('.', '_')] = op_role
        if field in field2 or field == 'studio':
            op_role = []
            op_role.append({'$unwind': '$info.'+field})
            op_role.append({'$group': {'_id': '$info.'+field,
                                       'average': {'$avg': '$watched.rating'},
                                       'sum': {'$sum': 1}}})
            op_role.append({'$match': {"sum": {'$gt': 2}}})
            op_role.append({'$sort': {'average': -1}})
            op_role.append({'$limit': 20})
            if field in field2:
                op_role.append({'$lookup': {
                    'from': 'People',
                    'localField': '_id',
                    'foreignField': '_id',
                    'as': 'info'}})
            json_operations['topRated'+field.replace('.', '_')] = op_role

    for field in field4:
        op_role = []
        op_role.append({'$unwind': '$info.'+field})
        op_role.append({'$group': {'_id': '$info.'+field,
                                   'average': {'$avg': '$watched.rating'},
                                   'sum': {'$sum': 1}}})
        if field == 'country':
            op_role.append({'$lookup': {
                'from': 'Countries',
                'localField': '_id',
                'foreignField': 'uri',
                'as': 'info'}})
            op_role.append({'$unwind': '$info'})
        op_role.append({'$sort': {'_id': 1}})
        json_operations['total'+field.rsplit(".", 1)[0]] = op_role


    op_role = []
    op_role.append({'$group': {'_id': '$_id',
                               'movies': {'$sum': 1},
                               'runtime': {'$sum': '$info.runtime'}}})
    json_operations['total'] = op_role

    op_role = []
    op_role.append({'$group': {'_id': '$watched.id',
                               'uri': {'$first': '$watched.uri'},
                               'poster': {'$first': '$info.images.poster'},
                               'media': {'$first': '$info.rating.average'},
                               'rating': {'$first': '$watched.rating'}}})
    op_role.append({'$match': {"rating": {'$gt': 0}}})
    op_role.append({'$match': {"media": {'$gt': 0}}})
    op_role.append({'$addFields': {'rispettoMedia': {'$subtract': [{'$divide': ['$rating', 2]}, '$media']}}})
    op_role.append({'$sort': {'rispettoMedia': -1}})
    op_role.append({'$limit': 12})
    json_operations['topToAverage'] = op_role

    op_role = []
    op_role.append({'$group': {'_id': '$watched.id',
                               'uri': {'$first': '$watched.uri'},
                               'poster': {'$first': '$info.images.poster'},
                               'media': {'$first': '$info.rating.average'},
                               'rating': {'$first': '$watched.rating'}}})
    op_role.append({'$match': {"rating": {'$gt': 0}}})
    op_role.append({'$match': {"media": {'$gt': 0}}})
    op_role.append({'$addFields': {'rispettoMedia': {'$subtract': [{'$divide': ['$rating', 2]}, '$media']}}})
    op_role.append({'$sort': {'rispettoMedia': 1}})
    op_role.append({'$limit': 12})
    json_operations['flopToAverage'] = op_role

    op_role = []
    op_role.append({'$group': {'_id': '$watched.id',
                               'year': {'$first': '$info.year'},
                               'poster': {'$first': '$info.images.poster'},
                               'rating': {'$first': '$watched.rating'}}})
    op_role.append({'$sort': {'rating': -1}})
    op_role.append({'$addFields': {'decade': {'$substr': [{'$toString': '$year'}, 0, 3]}}}),
    op_role.append({'$group': {'_id': '$decade',
                               'average': {'$avg': '$rating'},
                               'posters': {'$push': "$poster"},
                               'sum': {'$sum': 1}}})
    op_role.append({'$match': {"sum": {'$gt': 10}}})
    op_role.append({'$sort': {'average': -1}})
    op_role.append({'$limit': 3})
    op_role.append({'$project': {'_id': 1, 'average': 1, 'posters': {'$slice': ['$posters', 20]}}})
    json_operations['topDecade'] = op_role

    op_role = []
    op_role.append({'$group': {'_id': '$info.collection', 'num': {'$sum': 1}}})
    op_role.append({'$match': {"num": {'$gt': 1}}})
    op_role.append({'$lookup': {
        'from': 'Collections',
        'localField': '_id',
        'foreignField': '_id',
        'as': 'info'}})
    op_role.append({'$unwind': '$info'})
    op_role.append({'$match': {"info.num": {'$gt': 2}}})
    op_role.append({'$addFields': {"diff": {'$subtract': ['$info.num', '$num']}}})
    op_role.append({'$match': {'diff': {'$lt': 2}}})
    op_role.append({'$project': {'_id': '$_id', 'name': '$info.name', 'list': '$list',
                                 'perc': {'$divide': ['$num', '$info.num']},
                                 'num': {'$concat': [{'$toString': '$num'}, '/', {'$toString': '$info.num'}]}}})
    json_operations['collections'] = op_role

    op_role = []
    op_role.append({'$unwind': '$info.statsLists'})
    op_role.append({'$group': {'_id': '$info.statsLists', 'num': {'$sum': 1}}})
    op_role.append({'$lookup': {
        'from': 'Lists',
        'localField': '_id',
        'foreignField': '_id',
        'as': 'info'}})
    op_role.append({'$project': {'_id': '$_id', 'name': {'$first': '$info.name'},
                                 'watched': '$num', 'num': {'$first': '$info.num'}}})
    op_role.append({'$addFields': {"perc": {'$divide': ['$watched', '$num']}}}),
    json_operations['statsLists'] = op_role

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

#OBSOLETO
def getLists():
    return(db.Lists.aggregate([
        {'$match': {"isStats": True}},
        {'$unwind': '$uris'},
        {'$lookup': {
            'from': 'tmpUris',
            'localField': 'uris',
            'foreignField': 'uri',
            'as': 'info'}},
        {'$match': {"info": {'$not': {'$size': 0}}}},
        {'$group': {'_id': '$_id', 'name': {'$first': '$name'}, 'num': {'$first': '$num'}, 'numWatch': {'$sum': 1}}},
        {'$addFields': {"perc": {'$multiply': [{'$divide': ['$numWatch', '$num']}, 100]}}}
    ]))
