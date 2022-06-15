from mongodb import db
from operations import fillMongodb

def refresh():
    a = db.Film.aggregate([
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])

    print(len(uris))
    fillMongodb(uris)


if __name__ == '__main__':
    while True:
        try:
            refresh()
        except:
            pass