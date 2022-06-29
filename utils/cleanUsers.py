from mongodb import db
from operations import fillMongodb
from recommend.multiUsers import createAlgo


def cleanUsers():
    createAlgo()
    db.Users.delete_many({})
    #db.Users.delete_many({'name': {'$exists': False}})


if __name__ == '__main__':
    cleanUsers()
