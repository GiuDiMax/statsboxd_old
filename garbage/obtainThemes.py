from mongodb import db


def obtain(nano=False):
    theme = 'themes'
    if nano:
        theme = "mini-themes"
    a = db.Film.aggregate([
        {'$project': {'_id': 1, 'g': '$genres.'+str(theme)}},
        {'$unwind': '$g'},
        {'$group': {'_id': '$g', 'num': {'$sum': 1}}},
        {'$sort': {'num': -1}}
    ])
    lista = []
    for x in a:
        lista.append(x['_id'])
    print(lista)


if __name__ == '__main__':
    obtain(True)

