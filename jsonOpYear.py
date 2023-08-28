json_operations = {}
from config import *

for field in field2 + field3:
    op_role = []
    op_role.append({'$group': {'_id': '$diary.id',
                               'info': {'$first': '$info'},
                               'rat': {'$avg': '$diary.dRating'}
                               }})
    if field == 'genres.theme':
        op_role.append({'$project': {'themesunion': {'$concatArrays': [{'$ifNull': ['$info.genres.mini-theme', []]}, {'$ifNull': ['$info.genres.theme', []]}]}}})
        op_role.append({'$unwind': '$themesunion'})
        op_role.append({'$group': {'_id': '$themesunion',
                                   #'list': {'$push': '$uri'},
                                   'sum': {'$sum': 1}}})
    else:
        op_role.append({'$unwind': '$info.' + field})
        op_role.append({'$group': {'_id': '$info.' + field,
                                   'avg': {'$avg': '$rat'},
                                   'sum': {'$sum': 1}}})
    if field == 'actors':
        op_role.append({'$match': {"_id": {'$nin': exclude_people}}})
    if field == 'language' or field == 'country' or field == 'country':
        op_role.append({'$match': {"sum": {'$gt': 0}}})
        op_role.append({'$sort': {'sum': -1, 'avg': -1}})
        op_role.append({'$limit': 20})
    elif field != 'studio':
        op_role.append({'$match': {"sum": {'$gt': 1}}})
        op_role.append({'$sort': {'sum': -1, 'avg': -1}})
        op_role.append({'$limit': 20})
    else:
        op_role.append({'$match': {"sum": {'$gt': 2}}})
        op_role.append({'$sort': {'sum': -1, 'avg': -1}})
        op_role.append({'$limit': 50})
    if (field in field2) or (field == 'studio'):
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
        op_role.append({'$match': {'diary.dRating': {'$gt': 0}}})
        op_role.append({'$unwind': '$info.' + field})
        op_role.append({'$group': {'_id': '$info.' + field,
                                   'avg': {'$avg': '$diary.dRating'},
                                   'sum': {'$sum': 1}}})
        if field == 'actors':
            op_role.append({'$match': {"sum": {'$gt': 1}}})
            op_role.append({'$match': {"_id": {'$nin': exclude_people}}})
        op_role.append({'$sort': {'avg': -1, 'sum': -1, 'info.rating.average': -1}})
        op_role.append({'$limit': 20})
        if field == 'studio':
            op_role.append({'$lookup': {
                'from': 'Studios',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
            op_role.append(
                {'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'avg': {'$round': ['$avg', 2]}, 'name': {'$first': '$info.name'}}})
        else:
            op_role.append({'$lookup': {
                'from': 'People',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'info'}})
            op_role.append(
                {'$project': {'_id': {'$ifNull': [{'$first': '$info.uri'}, '$_id']}, 'avg': {'$round': ['$avg', 2]}, 'name': {'$first': '$info.name'}, 'img': {'$first': '$info.tmdbImg'}}})
        json_operations['topRated' + field.replace('.', '_')] = op_role

op_role = []
op_role.append({'$group': {'_id': '$_id',
                           'movies': {'$sum': 1},
                           'runtime': {'$sum': '$info.runtime'}}})
json_operations['total'] = op_role

op_role = []
op_role.append({'$match': {'$expr': {'$eq': ["$year", '$info.year']}}})
op_role.append({'$match': {'diary.dRating': {'$gt': 0}}})
op_role.append({'$group': {'_id': '$diary.id',
                           'rated': {'$max': '$diary.dRating'},
                           'uri': {'$first': '$info.uri'},
                           'rating': {'$first': '$diary.dRating'},
                           'poster': {'$first': '$info.images.poster'},
                           'average': {'$first': '$info.rating.average'}}})
op_role.append({'$sort': {'rated': -1, 'average': -1}})
op_role.append({'$limit': 8})
json_operations['topRatedCurrentYear'] = op_role

op_role = []
op_role.append({'$match': {'$expr': {'$ne': ["$year", '$info.year']}}})
op_role.append({'$group': {'_id': '$diary.id',
                           'rated': {'$max': '$diary.dRating'},
                           'uri': {'$first': '$diary.uri'},
                           'rating': {'$first': '$diary.dRating'},
                           'poster': {'$first': '$info.images.poster'},
                           'average': {'$first': '$info.rating.average'}}})
op_role.append({'$sort': {'rated': -1, 'average': -1}})
op_role.append({'$limit': 16})
json_operations['topRatedOtherYears'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.id',
                           'sum': {'$sum': 1},
                           'uri': {'$first': '$info.uri'},
                           'poster': {'$first': '$info.images.poster'}}})
op_role.append({'$match': {"sum": {'$gt': 1}}})
op_role.append({'$sort': {'sum': -1}})
op_role.append({'$limit': 5})
json_operations['mostWatched'] = op_role

op_role = []
op_role.append({'$project': {'dayWeek': {'$dayOfWeek': '$diary.date'}}})
op_role.append({'$group': {'_id': '$dayWeek',
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': 1}})
json_operations['dayOfWeek'] = op_role

op_role = []
op_role.append({'$project': {'week': {'$trunc': [{'$divide': [{'$subtract': [{'$dayOfYear': '$diary.date'}, 1]}, 7]}, 0]}}})
op_role.append({'$group': {'_id': {'$toInt': {'$add': ['$week', 1]}},
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': 1}})
json_operations['week'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.dRating',
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': 1}})
json_operations['rating'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.dLike',
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': -1}})
json_operations['liked'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.rewatch',
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': 1}})
json_operations['rewatch'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.review',
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': -1}})
json_operations['review'] = op_role

op_role = []
op_role.append({'$group': {'_id': {'$eq': ['$info.year', '$year']},
                           'sum': {'$sum': 1}}})
op_role.append({'$sort': {'_id': -1}})
json_operations['currentYear'] = op_role

op_role = []
op_role.append({'$sort': {'info.rating.average': -1}})
op_role.append({'$limit': 1})
op_role.append({'$project': {'uri': '$info.uri', 'avg': '$info.rating.average', 'poster': '$info.images.poster'}})
json_operations['bestMovie'] = op_role

op_role = []
op_role.append({'$match': {"info.rating.average": {"$exists": True}}})
op_role.append({'$sort': {'info.rating.average': 1}})
op_role.append({'$limit': 1})
op_role.append({'$project': {'uri': '$info.uri', 'avg': '$info.rating.average', 'poster': '$info.images.poster'}})
json_operations['worstMovie'] = op_role

op_role = []
#op_role.append({'$sort': {'info.rating.num': -1}})
op_role.append({'$match': {"info.members": {"$exists": True}}})
op_role.append({'$sort': {'info.members': -1}})
op_role.append({'$limit': 1})
op_role.append({'$project': {'uri': '$info.uri', 'avg': '$info.rating.average', 'poster': '$info.images.poster'}})
json_operations['mostPopularMovie'] = op_role

op_role = []
#op_role.append({'$match': {"info.rating.average": {"$exists": True}}})
#op_role.append({'$sort': {'info.rating.num': 1}})
op_role.append({'$match': {"info.members": {"$exists": True}}})
op_role.append({'$match': {"info.members": {"$gt": 0}}})
op_role.append({'$sort': {'info.members': 1}})
op_role.append({'$limit': 1})
op_role.append({'$project': {'uri': '$info.uri', 'avg': '$info.rating.average', 'poster': '$info.images.poster'}})
json_operations['lessPopularMovie'] = op_role

op_role = []
op_role.append({'$sort': {'diary.date': 1}})
op_role.append({'$limit': 1})
op_role.append({'$project': {'uri': '$info.uri', 'date': '$diary.date', 'poster': '$info.images.poster'}})
json_operations['firstMovie'] = op_role

op_role = []
op_role.append({'$sort': {'diary.date': -1}})
op_role.append({'$limit': 1})
op_role.append({'$project': {'uri': '$info.uri', 'date': '$diary.date', 'poster': '$info.images.poster'}})
json_operations['lastMovie'] = op_role

op_role = []
op_role.append({'$project': {"_id": '$diary.id', 'uri': '$info.uri', 'rating': '$diary.dRating', 'date': '$diary.date', 'poster': '$info.images.poster', 'media': '$info.rating.average'}})
op_role.append({'$sort': {'diary.date': -1}})
op_role.append({'$group': {'_id': '$_id',
                           'uri': {'$first': '$uri'},
                           'poster': {'$first': '$poster'},
                           'media': {'$first': '$media'},
                           'rating': {'$first': '$rating'}}})
op_role.append({'$match': {"rating": {'$gt': 0}}})
op_role.append({'$match': {"media": {'$gt': 0}}})
op_role.append({'$addFields': {'rispettoMedia': {'$subtract': [{'$divide': ['$rating', 2]}, '$media']}}})
op_role.append({'$sort': {'rispettoMedia': -1}})
op_role.append({'$limit': 6})
json_operations['topToAverage'] = op_role

op_role = []
op_role.append({'$project': {"_id": '$diary.id', 'uri': '$info.uri', 'rating': '$diary.dRating', 'date': '$diary.date', 'poster': '$info.images.poster', 'media': '$info.rating.average'}})
op_role.append({'$sort': {'diary.date': -1}})
op_role.append({'$group': {'_id': '$_id',
                           'uri': {'$first': '$uri'},
                           'poster': {'$first': '$poster'},
                           'media': {'$first': '$media'},
                           'rating': {'$first': '$rating'}}})
op_role.append({'$match': {"rating": {'$gt': 0}}})
op_role.append({'$match': {"media": {'$gt': 0}}})
op_role.append({'$addFields': {'rispettoMedia': {'$subtract': [{'$divide': ['$rating', 2]}, '$media']}}})
op_role.append({'$sort': {'rispettoMedia': 1}})
op_role.append({'$limit': 6})
json_operations['flopToAverage'] = op_role


op_role = []
op_role.append({'$sort': {'diary.date': 1}})
op_role.append({'$project': {'_id': '$info.uri', 'date': '$diary.date', 'poster': '$info.images.poster'}})
json_operations['milestones'] = op_role


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
        op_role.append({'$project': {'_id': {'$first': '$info._id'}, 'uri': '$_id', 'sum': 1}})
    op_role.append({'$sort': {'_id': 1}})
    json_operations['total' + field.rsplit(".", 1)[0]] = op_role
