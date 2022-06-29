from mongodb import db
from operations import fillMongodb
from recommend.multiUsers import createAlgo


def cleanUsers():
    createAlgo()
    #db.Users.delete_many({})
    db.Users.delete_many({'name': {'$exists': False}})
    db.Users.update_many({}, {'$unset': {'diary': 1, 'stats': 1}})


if __name__ == '__main__':
    cleanUsers()
