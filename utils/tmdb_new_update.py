import requests
from datetime import datetime, timedelta
from operations import fillMongodb, fillMongodbmembers, fillMongodbratings
from mongodb import db


def updatefromtmdb(onlytoday, dayoff=1):
    nowx = datetime.now() - timedelta(days=dayoff)
    past = (nowx - timedelta(days=14)).isoformat()
    if onlytoday:
        past = (nowx - timedelta(days=1)).isoformat()
    now = nowx.isoformat()
    url = "https://api.themoviedb.org/3/movie/changes?page={page}&api_key=6fff7e293df6a808b97101a26c86a545"
    urlx = url.format(page=1, start=past, end=now)
    r = requests.get(urlx).json()
    pages = int(r['total_pages'])
    for j in range(pages):
        ids = []
        uris = []
        urlx = url.format(page=j+1, start=past, end=now)
        r = requests.get(urlx).json()
        for id in r['results']:
            ids.append(id['id'])
        a = db.Film.aggregate([
            {'$match': {"tmdb": {'$in': ids}}},
            {'$match': {"updateDate": {'$lt': nowx}}},
            {'$project': {'_id': 0, 'uri': 1}}
        ])
        for x in a:
            uris.append(x['uri'])
        print("aggiorno: " + str(len(uris)))
        fillMongodb(uris)
        fillMongodbmembers(uris)
        fillMongodbratings(uris)


if __name__ == '__main__':
    updatefromtmdb(False)
