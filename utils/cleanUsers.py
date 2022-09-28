from mongodb import db
from operations import fillMongodb
#from recommend.multiUsers import createAlgo


def cleanUsers():
    #createAlgo()
    #db.Users.delete_many({})
    db.Users.delete_many({'name': {'$exists': False}})
    db.Users.update_many({}, {'$unset': {'diary': 1, 'stats': 1,
                                         'stats_2022': 1, 'stats_2021': 1, 'stats_2020': 1,
                                         'stats_2019': 1, 'stats_2018': 1, 'stats_2017': 1,
                                         'stats_2016': 1, 'stats_2015': 1, 'stats_2014': 1,
                                         'years': 1, 'mostWatched': 1, 'image': 1,
                                         }})


if __name__ == '__main__':
    cleanUsers()
