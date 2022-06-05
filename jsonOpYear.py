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
        op_role.append({'$group': {'_id': '$info.' + field,
                                   'average': {'$avg': '$watched.rating'},
                                   'sum': {'$sum': 1}}})
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

op_role = []
op_role.append({'$group': {'_id': '$_id',
                           'movies': {'$sum': 1},
                           'runtime': {'$sum': '$info.runtime'}}})
json_operations['total'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.dRating',
                           'sum': {'$sum': 1}}})
json_operations['rating'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.dLike',
                           'sum': {'$sum': 1}}})
json_operations['liked'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.rewatch',
                           'sum': {'$sum': 1}}})
json_operations['rewatch'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$diary.review',
                           'sum': {'$sum': 1}}})
json_operations['review'] = op_role

op_role = []
op_role.append({'$group': {'_id': '$info.year',
                           'sum': {'$sum': 1}}})
json_operations['years'] = op_role

op_role = []
op_role.append({'$sort': {'info.rating.average': -1}})
op_role.append({'$limit': 1})
json_operations['bestMovie'] = op_role

op_role = []
op_role.append({'$sort': {'info.rating.average': 1}})
op_role.append({'$limit': 1})
json_operations['worstMovie'] = op_role

op_role = []
op_role.append({'$sort': {'info.rating.num': -1}})
op_role.append({'$limit': 1})
json_operations['mostPopularMovie'] = op_role

op_role = []
op_role.append({'$sort': {'info.rating.num': 1}})
op_role.append({'$limit': 1})
json_operations['lessPopularMovie'] = op_role

op_role = []
op_role.append({'$sort': {'diary.date': 1}})
op_role.append({'$limit': 1})
json_operations['firstMovie'] = op_role

op_role = []
op_role.append({'$sort': {'diary.date': -1}})
op_role.append({'$limit': 1})
json_operations['lastMovie'] = op_role