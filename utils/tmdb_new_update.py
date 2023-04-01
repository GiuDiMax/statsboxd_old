import requests
from datetime import datetime, timedelta
from operations import fillMongodb, fillMongodbmembers, fillMongodbratings
from mongodb import db
from threading import Thread

global ids


def getids(url, pag, start, end):
    global ids
    r = requests.get(url.format(page=pag, start=start, end=end)).json()
    for id in r['results']:
        ids.append(id['id'])


def updatefromtmdb(onlytoday, dayoff=1):
    global ids
    ids = []

    nowx = datetime.now() - timedelta(days=dayoff)
    past = (nowx - timedelta(days=14)).isoformat()
    if onlytoday:
        past = (nowx - timedelta(days=1)).isoformat()
    now = nowx.isoformat()
    url = "https://api.themoviedb.org/3/movie/changes?page={page}&api_key=6fff7e293df6a808b97101a26c86a545"
    urlx = url.format(page=1, start=past, end=now)
    r = requests.get(urlx).json()
    pages = int(r['total_pages'])
    th = []
    for j in range(pages+1):
        th.append(Thread(target=getids, args=(url, j+1, past, now,)))
    for t in th:
        t.start()
    for t in th:
        t.join()

    while True:
        uris = []
        a = db.Film.aggregate([
            {'$match': {"tmdb": {'$in': ids}}},
            {'$match': {"updateDate": {'$lt': nowx}}},
            {'$project': {'_id': 0, 'uri': 1}},
            {'$limit': 100}
        ])
        for x in a:
            uris.append(x['uri'])
        if len(uris) == 0:
            print("nessuna modifica da fare")
            break
        else:
            print(len(uris))
            fillMongodb(uris)
            fillMongodbmembers(uris)
            fillMongodbratings(uris)


if __name__ == '__main__':
    updatefromtmdb(False)
