from mongodb import db
from operations import fillMongodb


def fix():
    a = db.Film.aggregate([
        {'$match': {"imdb": {'$exists': True}}},
        {'$match': {"tt": {'$nin': 'imdb'}}},
        {'$limit': 1000},
        {'$project': {'uri': 1, 'imdb': 1}}
    ])

    uris = []
    for x in a:
        y = 'tt' + str(x['imdb']).zfill(7)
        db.Film.update_one({'_id': x['_id']}, {'$set': {'imdb': y}}, True)
    print('1000 fatti')


def fix2():
    a = db.Film.aggregate([
        {'$match': {"tmdb_tv": {'$exists': False}}},
        {'$match': {"tmdb": {'$exists': False}}},
        #{'$limit': 1000},
        {'$project': {'uri': 1}}
    ])
    uris = []
    for x in a:
        uris.append(x['uri'])
    #print(uris)
    print(len(uris))
    fillMongodb(uris)


if __name__ == '__main__':
    for a in range(50):
        fix()