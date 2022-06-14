from mongodb import db
from operations import fillMongodb

def cleanUsers():
    #db.Users.delete_many({})
    db.Users.delete_many({'name': {'$exists': False}})

if __name__ == '__main__':
    cleanUsers()