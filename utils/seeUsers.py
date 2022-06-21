from mongodb import db

a = db.Users.aggregate([
    {'$project': {'_id': 1, 'name': 1}},
])
for x in a:
    print(x)
