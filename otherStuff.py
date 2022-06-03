from mongodb import db

#db.Users.delete_many({})
#db.Film.delete_many({})

a = db.delete_many.find({ 'images': { '$exists': False }})
