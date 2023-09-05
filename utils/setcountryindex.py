from mongodb import db
from config import *

x = list(db.Countries.find({}))
ll = []
for a in x:
    a['index'] = cou_l.index(a['uri'])
    db.Countries.update_one({'_id': a['_id']}, {'$set': a}, upsert=True)
    #try:
    #    a['index'] = cou_l.index(a['uri'])
    #except:
    #    ll.append(a['uri'])
print(x)
#print(ll)
#db.Countries.insert_many(x)