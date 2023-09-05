json_operations = {}
from config import *

for field in field2 + field3:
    op_role = []
    if field == 'genres.theme':
        op_role.append({'$project': {'themesunion': {'$concatArrays': [{'$ifNull': ['$info.genres.mini-theme', []]}, {'$ifNull': ['$info.genres.theme', []]}]}}})
        op_role.append({'$unwind': '$themesunion'})
        op_role.append({'$group': {'_id': '$themesunion',
                                   'sum': {'$sum': 1}}})
    else:
        op_role.append({'$unwind': '$info.' + field})
        op_role.append({'$group': {'_id': '$info.' + field,
                                   'run': {'$sum': '$info.runtime'},
                                   #'avg': {'$avg': '$watched.rating'},
                                   'sum': {'$sum': 1}}})
    if field == 'actors':
        op_role.append({'$match': {"_id": {'$nin': exclude_people}}})
    if field == 'language' or field == 'country':
        op_role.append({'$match': {"sum": {'$gt': 0}}})
        op_role.append({'$sort': {'sum': -1, 'run': -1}})
        op_role.append({'$limit': 10})
    #elif field != 'studio':
    #    op_role.append({'$match': {"sum": {'$gt': 2}}})
    #    op_role.append({'$sort': {'sum': -1, 'run': -1}})
    #    op_role.append({'$limit': 10})
    else:
        op_role.append({'$match': {"sum": {'$gt': 3}}})
        op_role.append({'$sort': {'sum': -1, 'run': -1}})
        op_role.append({'$limit': 20})
    #op_role.append({'$limit': 20})
    if (field in field2):
        op_role.append({'$lookup': {
            'from': 'People',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}})
        op_role.append({'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'sum': 1,
                                     'name': {'$first': '$info.name'}, 'img': {'$first': '$info.tmdbImg'}}})
        #if field == "studio":
        #    op_role.append({'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'sum': 1, 'name': {'$first': '$info.name'}, 'img': {'$first': '$info.img'}}})
        #else:
        #    op_role.append({'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'sum': 1, 'name': {'$first': '$info.name'}, 'img': {'$first': '$info.tmdbImg'}}})
        #    op_role.append({'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, {'$first': '$info._id'}]}, 'sum': 1, 'name': {'$first': '$info.name'}, 'img': {'$first': '$info.tmdbImg'}}})
    elif field == 'studio':
        op_role.append({'$lookup': {
            'from': 'Studios',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}})
        op_role.append({'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'sum': 1,
                                     'name': {'$first': '$info.name'}}})
    elif field in ['genres.theme', 'genres.nanogenre']:
        op_role.append({'$lookup': {
            'from': 'Themes',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}})
        op_role.append({'$unwind': '$info'})
        op_role.append({'$project': {'_id': 1, 'sum': 1, 'name': '$info.name', 'uri': '$info.uri', 'type': '$info.type'}})
    json_operations['mostWatched' + field.replace('.', '_')] = op_role
    if (field in field2) or (field == 'studio'):
        op_role = []
        op_role.append({'$unwind': '$info.' + field})
        op_role.append({'$match': {'watched.rating': {'$gt': 0}}})
        op_role.append({'$group': {'_id': '$info.' + field,
                                   'avg': {'$avg': '$watched.rating'},
                                   'sum': {'$sum': 1}}})
        if field == 'actors':
            op_role.append({'$match': {"sum": {'$gt': 3}}})
            op_role.append({'$match': {"_id": {'$nin': exclude_people}}})
        else:
            op_role.append({'$match': {"sum": {'$gt': 1}}})
        op_role.append({'$sort': {'avg': -1, 'sum': -1, 'info.rating.average': -1}})
        op_role.append({'$limit': 20})
        if field == 'studio':
            op_role.append({'$lookup': {
                'from': 'Studios',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
            op_role.append(
                {'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'avg': {'$round': ['$avg', 2]},
                              'name': {'$first': '$info.name'}}})
        else:
            op_role.append({'$lookup': {
                'from': 'People',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
            op_role.append(
                {'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'avg': {'$round': ['$avg', 2]}, 'name': {'$first': '$info.name'}, 'img': {'$first': '$info.tmdbImg'}}})
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
            'foreignField': 'index',
            'as': 'info'}})
        op_role.append({'$project': {'_id': {'$first': '$info._id'}, 'uri': '$_id', 'sum': 1}})
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
                           'uri': {'$first': '$info.uri'},
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
                           'uri': {'$first': '$info.uri'},
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
op_role.append({'$match': {'diff': {'$lt': 3}}})
op_role.append({'$project': {'_id': '$_id', 'name': '$info.name', 'list': '$list', 'numRat': '$info.numRat',
                             'perc': {'$divide': ['$num', '$info.num']},
                             'complete': {'$cond': {'if': {'$eq': [{'$divide': ['$num', '$info.num']}, 1]}, 'then': 'complete', 'else': 'almost'}},
                             'num': {'$concat': [{'$toString': '$num'}, '/', {'$toString': '$info.num'}]},
                             'posters': '$info.posters'}})
op_role.append({'$match': {"posters": {'$exists': True}}})
#op_role.append({'$match': {"posters": {'$ne': []}}})
op_role.append({'$match': {'perc': {'$gt': 0.65}}})
op_role.append({'$sort': {'numRat': -1, 'perc': -1}})
op_role.append({'$project': {'_id': 1, 'name': 1, 'num': 1, 'posters': 1, 'complete': 1}})
op_role.append({'$group': {'_id': '$complete', 'collections': {'$push': '$$ROOT'}}})
op_role.append({'$unset': ['collections.complete']})
op_role.append({'$sort': {'_id': -1}})
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
def test():
    from mongodb import db
    op_role = []
    op_role.append({'$match': {"_id": 'giudimax'}})
    op_role.append({'$unwind': '$sug'})
    op_role.append({'$project': {'_id': 0, 'uri': '$sug.uri', 'perc': '$sug.perc'}})
    op_role.append({'$lookup': {
        'from': 'Film',
        'localField': 'uri',
        'foreignField': 'uri',
        'as': 'info'}})
    op_role.append({'$unwind': '$info'})
    op_role.append({'$unwind': '$info.related'})
    op_role.append({'$project': {'_id': '$info.related', 'perc': ''}})
    op_role.append({'$limit': 1})
    ob3 = db.Users.aggregate(op_role)
    for x in ob3:
        print(x)


if __name__ == '__main__':
    test()
    #print(y['mostWatchedlanguage'])
