from mongodb import db


def fix():
    a = db.Film.aggregate([
        {'$match': {"imdb": {'$lt': 1000000}}},
        {'$limit': 1000},
        {'$project': {'uri': 1, 'imdb': 1}}
    ])

    uris = []
    for x in a:
        y = str(x['imdb']).zfill(7)
        db.Film.update_one({'_id': x['_id']}, {'$set': {'imdb': y}}, True)
    print('1000 fatti')


if __name__ == '__main__':
    for a in range(50):
        fix()