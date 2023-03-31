op_role = []
op_role.append({'$project': {'user': '$_id', 'id': '$info.related', 'rating': '$watched.rating'}})
op_role.append({'$unwind': '$id'})
op_role.append({'$group': {'_id': {'$toInt': '$id'},
                           'user': {'$first': '$user'},
                           'avg': {'$avg': '$rating'},
                           'sum': {'$sum': 1}}})
op_role.append({'$match': {'sum': {'$gt': 1}}})
op_role.append({'$sort': {'avg': -1}})
op_role.append({'$lookup': {
    'from': 'Users',
    'localField': 'user',
    'foreignField': '_id',
    'let': {'movie_id': "$_id"},
    'pipeline': [{'$unwind': '$watched'},
                 {'$group': {'_id': '$id', 'lista': {'$push': '$watched.id'}}},
                 {'$project': {'_id': 1, 'watched': {'$in': ['$$movie_id', '$lista']}}},
                 {'$match': {'watched': False}},
                 ],
    'as': 'info2'}})
op_role.append({'$match': {'info2': {'$ne': []}}})
op_role.append({'$lookup': {
    'from': 'Film',
    'localField': '_id',
    'foreignField': '_id',
    'as': 'info'}})
op_role.append({'$unwind': '$info'})
op_role.append({'$sort': {'avg': -1, 'info.rating.average': -1}})
op_role.append({'$project': {'_id': 1, 'uri': '$info.uri', 'poster': '$info.images.poster', 'perc': {'$toInt': {'$multiply': ['$avg', 10]}}}})
op_role.append({'$limit': 60})