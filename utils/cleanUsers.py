from mongodb import db
from datetime import datetime, timedelta


def clean2():
    x = db.Users.update_many({}, {'$unset': {'diary': 1, 'stats': 1, 'stats_2023': 1,
                                 'stats_2022': 1, 'stats_2021': 1, 'stats_2020': 1,
                                 'stats_2019': 1, 'stats_2018': 1, 'stats_2017': 1,
                                 'stats_2016': 1, 'stats_2015': 1, 'stats_2014': 1,
                                 'years': 1, 'mostWatched': 1, 'image': 1, 'sug2': 1,
                                 'diaryperyear': 1, 'extra_stats': 1, 'diary2': 1, 'sug3': 1,
                                 'stats2': 1, 'ru': 1, 'fullUpdate': 1, 'update': 1,
                                 }})
    print("updated: " + str(x.modified_count))


def cleanUsers():
    #db.Users.delete_many({})
    db.Users.delete_many({'name': {'$exists': False}})
    datex = datetime.today()
    datey = datex - timedelta(days=30)
    x = db.Users.update_many({'$or': [{'update': {'$lt': datey}}, {'update': {'$exists': False}}]},
                                        {'$unset': {'diary': 1, 'stats': 1, 'stats_2023': 1,
                                         'stats_2022': 1, 'stats_2021': 1, 'stats_2020': 1,
                                         'stats_2019': 1, 'stats_2018': 1, 'stats_2017': 1,
                                         'stats_2016': 1, 'stats_2015': 1, 'stats_2014': 1,
                                         'years': 1, 'mostWatched': 1, 'image': 1, 'sug2': 1,
                                         'diaryperyear': 1, 'extra_stats': 1, 'diary2': 1, 'sug3': 1,
                                         'stats2': 1, 'update': 1, 'ru': 1, 'fullUpdate': 1,
                                         }})
    print("updated: " + str(x.modified_count))
    datey = datex - timedelta(days=90)
    x = db.Users.delete_many({'$or': [{'update': {'$lt': datey}}, {'update': {'$exists': False}}]})
    print("deleted: " + str(x.deleted_count))
    return
    o = db.Users.find({'$or': [{'update': {'$lt': datey}}, {'update': {'$exists': False}}]})
    for x in o:
        print(x['_id'])


if __name__ == '__main__':
    #db.Users.delete_one({'_id': 'giudimax'})
    #cleanUsers()
    clean2()
