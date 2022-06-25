json_operations = {}
from config import *

for field in field2 + field3:
    op_role = []
    op_role.append({'$unwind': '$info.' + field})
    op_role.append({'$group': {'_id': '$info.' + field,
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
    json_operations['mostWatched' + field.replace('.', '_')] = op_role
    if field in field2 or field == 'studio':
        op_role = []
        op_role.append({'$unwind': '$info.' + field})
        op_role.append({'$match': {'watched.rating': {'$gt': 0}}})
        op_role.append({'$group': {'_id': '$info.' + field,
                                   'average': {'$avg': '$watched.rating'},
                                   'sum': {'$sum': 1}}})
        if field == 'actors':
            op_role.append({'$match': {"sum": {'$gt': 3}}})
        else:
            op_role.append({'$match': {"sum": {'$gt': 1}}})
        op_role.append({'$sort': {'average': -1}})
        op_role.append({'$limit': 20})
        if field in field2:
            op_role.append({'$lookup': {
                'from': 'People',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
        json_operations['topRated' + field.replace('.', '_')] = op_role

for field in field4:
    op_role = []
    op_role.append({'$unwind': '$info.' + field})
    op_role.append({'$group': {'_id': '$info.' + field,
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
    json_operations['total' + field.rsplit(".", 1)[0]] = op_role

op_role = []
op_role.append({'$group': {'_id': '$_id',
                           'movies': {'$sum': 1},
                           'runtime': {'$sum': '$info.runtime'}}})
json_operations['total'] = op_role

op_role = []
op_role.append({'$unwind': '$info.crew.director'})
op_role.append({'$group': {'_id': '$info.crew.director'}})
op_role.append({'$group': {'_id': None, 'count': {"$sum": 1}}})
json_operations['totalDirectors'] = op_role

op_role = []
op_role.append({'$unwind': '$info.country'})
op_role.append({'$group': {'_id': '$info.country'}})
op_role.append({'$group': {'_id': None, 'count': {"$sum": 1}}})
json_operations['totalCountry'] = op_role

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
                           'uri': {'$first': '$info.uri'},
                           'poster': {'$first': '$info.images.poster'},
                           'rating': {'$first': '$watched.rating'}}})
op_role.append({'$match': {'rating': {'$gt': 0}}})
op_role.append({'$sort': {'rating': -1}})
op_role.append({'$addFields': {'decade': {'$substr': [{'$toString': '$year'}, 0, 3]}}}),
op_role.append({'$group': {'_id': '$decade',
                           'average': {'$avg': '$rating'},
                           'posters': {'$push': {'img': "$poster", 'uri': '$uri'}},
                           'sum': {'$sum': 1}}})
op_role.append({'$match': {"sum": {'$gt': 9}}})
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
op_role.append({'$project': {'_id': '$_id', 'name': {'$first': '$info.name'}, 'order': {'$first': '$info.order'},
                             'watched': '$num', 'num': {'$first': '$info.num'}}})
op_role.append({'$addFields': {"perc": {'$divide': ['$watched', '$num']}}}),
op_role.append({'$sort': {'order': 1}})
json_operations['statsLists'] = op_role

# ZONA TEST

json_operations2 = {}

op_role = []
op_role.append({'$unwind': '$info.actors'})
op_role.append({'$group': {'_id': '$info.actors',
                           'average': {'$avg': '$watched.rating'},
                           'sum': {'$sum': 1},
                           'list': {'$push': '$info.uri'}}})
op_role.append({'$sort': {'sum': -1}})
op_role.append({'$limit': 10})
json_operations2['test'] = op_role


