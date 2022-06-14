from mongodb import db
import time
from datetime import date, timedelta, datetime
from operations import fillMongodb

#db.Users.delete_many({})
#db.Film.delete_many({})

#db.Film.delete_many({ 'images': { '$exists': False }})

datex = datetime.today()
datex = datex - timedelta(days=7)

current_year = date.today().year
a = db.Film.aggregate([
    {'$match': {"year": {'$gt': current_year - 2}}},
    {'$match': {"updateDate": {'$lt': datex}}},
    {'$project': {'uri': 1}}
])

uris = []
for x in a:
    uris.append(x['uri'])

print(len(uris))
fillMongodb(uris)

'''
print(1)
start = time.time()

a = db.alltimestats.find({})
for x in a:
    for y in x:
        print(y)

print(time.time()-start)
'''

