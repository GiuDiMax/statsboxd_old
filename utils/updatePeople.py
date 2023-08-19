from mongodb import db
from datetime import datetime, timedelta
from setPeople import fillMongodb, mainSetNames
import aiohttp
import asyncio
from config import *


def fill_db4(url, resp):
    json1 = {}
    json1['_id'] = url[1]
    json1['name'] = url[2]
    json1['update'] = datetime.today()
    try:
        try:
            json1['tmdbImg'] = str(resp).rsplit('"profile_path":"', 1)[1].rsplit('"', 1)[0]
        except:
            json1['imgNone'] = True
    except:
        print('error tmdb for ' + url[1])
    #print(json1)
    db.People.update_one({'_id': json1['_id']}, {'$set': json1}, True)


async def get3(url, session):
    async with session.get(url="https://api.themoviedb.org/3/person/" + str(url[0]) + "?api_key=" + api_tmdb + "&language=en-US") as response:
            resp = await response.read()
            fill_db4(url, resp)


async def main4(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get3(url, session) for url in urls])


def fillMongodb4(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main4(urls))


def fillMongodbOnlyImage(urls):
    n = 100
    if len(urls) < n:
        fillMongodb4(urls)
    else:
        fillMongodb4(urls[:n])
        print("aggiunti " + str(n) + " nuovi record")
        fillMongodbOnlyImage(urls[n:])


def test():
    lista = list(db.People.aggregate([
        #{'$match': {'tmdbImg': {'$exists': True}}},
        #{'$match': {'tmdb': {'$exists': True}}},
        {'$match': {'update': {'$exists': True}}},
        {'$project': {'_id': 1}}
    ]))
    uris = [str(x['_id']) for x in lista]
    print(uris[:100])
    fillMongodb(uris, False)


def prePeople():
    datex = datetime.today()
    datex = datex - timedelta(days=365)
    lista = list(db.People.aggregate([
        {'$match': {'tmdbImg': {'$exists': True}}},
        {'$match': {'$or': [{'update': {'$lt': datex}}, {'update': {'$exists': False}}]}},
        {'$match': {'tmdb': {'$exists': False}}},
        {'$project': {'_id': 1}}
    ]))
    uris = [str(x['_id']) for x in lista]
    print("da pre aggiornare: " + str(len(uris)))
    #print(uris[:100])
    fillMongodb(uris, False)


def upPeople():
    datex = datetime.today()
    datex = datex - timedelta(days=365)
    lista = db.People.aggregate([
        {'$match': {'tmdbImg': {'$exists': True}}},
        {'$match': {'$or': [{'update': {'$lt': datex}}, {'update': {'$exists': False}}]}},
        {'$match': {'tmdb': {'$exists': True}}},
        {'$project': {'_id': 1, 'tmdb': 1, 'name': 1}}
    ])
    lx = []
    for p in lista:
        lx.append([p['tmdb'], p['_id'], p['name']])
    #print(lx)
    print("da aggiornare: " + str(len(lx)))
    fillMongodbOnlyImage(lx)


if __name__ == '__main__':
    #json1 = {'_id': 'kaan-guldur', 'update': datetime.today(), 'name': 'Kaan Guldur', 'tmdb': 1877487}
    #db.People.update_one({'_id': json1['_id']}, {'$set': json1}, True)
    #exit()
    #test()
    prePeople()
    upPeople()
    mainSetNames()