import requests
from datetime import datetime, timedelta
from operations import fillMongodb, fillMongodbmembers, fillMongodbratings
from mongodb import db
from threading import Thread
import time

global ids, idp, limitx
limitx = 50


def updatePhoto(id):
    url = "https://api.themoviedb.org/3/person/{id}?api_key=6fff7e293df6a808b97101a26c86a545"
    r = requests.get(url.format(id=str(id))).json()
    if 'profile_path' in r:
        db.People.update_one({'tmdb': id}, {'$set': {'update': datetime.today(), 'tmdbImg': r['profile_path']}}, True)


def getids(url, pag, start, end):
    global ids
    r = requests.get(url.format(page=pag, start=start, end=end)).json()
    if 'results' in r:
        for id in r['results']:
            ids.append(id['id'])
    else:
        time.sleep(0.5)
        getids(url, pag, start, end)


def getidp(url, pag, start, end):
    global idp
    r = requests.get(url.format(page=pag, start=start, end=end)).json()
    if 'results' in r:
        for id in r['results']:
            idp.append(id['id'])
    else:
        time.sleep(0.5)
        getidp(url, pag, start, end)


def updatePeople(onlytoday, dayoff=1):
    global idp
    idp = []

    nowx = datetime.now() - timedelta(days=dayoff)
    past = (nowx - timedelta(days=14)).isoformat()
    if onlytoday:
        past = (nowx - timedelta(hours=25)).isoformat()
    now = nowx.isoformat()
    url = "https://api.themoviedb.org/3/person/changes?page={page}&api_key=6fff7e293df6a808b97101a26c86a545&start_date={start}&end_date={end}"
    urlx = url.format(page=1, start=past, end=now)
    r = requests.get(urlx).json()
    pages = int(r['total_pages'])
    th = []
    for j in range(pages+1):
        th.append(Thread(target=getidp, args=(url, j+1, past, now,)))
    for t in th:
        t.start()
    for t in th:
        t.join()
    while True:
        uris = []
        a = db.People.aggregate([
            {'$match': {"tmdb": {'$in': idp}}},
            {'$match': {'tmdbImg': {'$exists': True}}},
            {'$match': {"updateDate": {'$lt': nowx}}},
            {'$project': {'_id': '$tmdb'}},
            {'$limit': limitx}
        ])
        for x in a:
            uris.append(x['_id'])
        if len(uris) == 0:
            print("nessuna modifica da fare")
            break
        else:
            print(len(uris))
            th = []
            for u in uris:
                th.append(Thread(target=updatePhoto, args=(u, )))
            for t in th:
                t.start()
            for t in th:
                t.join()


def updatefromtmdb(onlytoday, dayoff=1):
    global ids
    ids = []

    nowx = datetime.now() - timedelta(days=dayoff)
    past = (nowx - timedelta(days=14)).isoformat()
    if onlytoday:
        past = (nowx - timedelta(hours=25)).isoformat()
    now = nowx.isoformat()
    url = "https://api.themoviedb.org/3/movie/changes?page={page}&api_key=6fff7e293df6a808b97101a26c86a545&start_date={start}&end_date={end}"
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
            {'$limit': limitx}
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
    updatefromtmdb(False, 0)
    updatePeople(False, 0)
