from mongodb import db

gg = []
gen = list(db.Film.aggregate([
    #{'$project': {'g': '$genres.main'}},
    {'$project': {'g': '$spoken language'}},
    {'$unwind': '$g'},
    {'$group': {'_id': '$g',
                'sum': {'$sum': 1}}},
    {'$sort': {'sum': -1}}
]))

for x in gen:
    print(x)
    gg.append(x['_id'])

print(gg)