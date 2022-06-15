from mongodb import db
import time
from datetime import date, timedelta, datetime
from operations import fillMongodb

#db.Users.delete_many({})
#db.Film.delete_many({})

#db.Film.delete_many({ 'images': { '$exists': False }})

a = db.Users.aggregate([
    {'$match': {"_id": 'moviefinger'}},
    {'$unwind': '$watched'},
    {'$lookup': {
        'from': 'Film',
        'localField': 'watched.id',
        'foreignField': '_id',
        'as': 'info'}},
    {'$unwind': '$info'},
    {'$sort': {'info.uri': 1}},
    {'$unwind': '$info.actors'},
    {'$group': {'_id': '$info.actors',
                'average': {'$avg': '$watched.rating'},
                'list': {'$push': '$info.uri'},
                'sum': {'$sum': 1}}},
    {'$sort': {'sum': -1}},
    {'$limit': 2},
])

for x in a:
    print(x)

'''
print(1)
start = time.time()

a = db.alltimestats.find({})
for x in a:
    for y in x:
        print(y)

print(time.time()-start)
'''

