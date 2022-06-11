from mongodb import db
import time

#db.Users.delete_many({})
#db.Film.delete_many({})

db.Film.delete_many({ 'images': { '$exists': False }})

'''
print(1)
start = time.time()

a = db.alltimestats.find({})
for x in a:
    for y in x:
        print(y)

print(time.time()-start)
'''

