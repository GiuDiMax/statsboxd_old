from mongodb import db
from config import *
import aiohttp
import asyncio
import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
from mongodb import db
from datetime import datetime, timedelta
from config import *
from threading import Thread


def fill_db(url, soup, image):
    json1 = {}
    json1['_id'] = url
    json1['name'] = (str(soup.find("h1", {"class": "title-1"})).split("</span>", 1)[1].split("</h1>", 1)[0]).strip()
    tmdb = int(soup.find("div", {"class": "js-tmdb-person-bio"})['data-tmdb-id'])
    json1['tmdb'] = tmdb
    if image:
        req = "https://api.themoviedb.org/3/person/"+str(tmdb)+"?api_key="+api_tmdb+"&language=en-US"
        x = requests.get(req)
        try:
            json1['tmdbImg'] = x.text.rsplit('"profile_path":"', 1)[1].rsplit('"', 1)[0]
        except:
            pass
    try:
        db.People.insert_one(json1)
    except:
        db.People.update_one({'_id': json1['_id']}, {'$set': json1})


async def get(url, session, image):
    async with session.get(url='http://letterboxd.com/writer/' + url + "/") as response:
            resp = await response.read()
            soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
            fill_db(url, soup, image)


async def main2(urls, image):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session, image) for url in urls])


def fillMongodb2(urls, image):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls, image))
    #return asyncio.get_event_loop().run_until_complete(main2(urls))


def fillMongodb(urls, image):
    if len(urls) < 1000:
        fillMongodb2(urls, image)
    else:
        urlsx = urls[:1000]
        fillMongodb2(urlsx, image)
        print("added 1000 new records")
        fillMongodb(urls[1000:], image)


def mainSetNames():
    json_operations = {}
    for field in field2:
        op_role = []
        op_role.append({'$unwind': '$'+field})
        op_role.append({'$group': {'_id': '$'+field,
                                   'sum': {'$sum': 1}}})
        op_role.append({'$match': {"sum": {'$gt': 4}}})
        #if field in ['actors', 'crew.director']:
        #    op_role.append({'$match': {"sum": {'$lt': 10}}})
        op_role.append({'$lookup': {
                            'from': 'People',
                            'localField': '_id',
                            'foreignField': '_id',
                            'as': 'info'}})
        op_role.append({'$match': {"info": {'$eq': []}}})
        json_operations[field.replace(".", "_")] = op_role

    for field in ['actors', 'crew.director']:
        op_role = []
        op_role.append({'$unwind': '$'+field})
        op_role.append({'$group': {'_id': '$'+field,
                                   'sum': {'$sum': 1}}})
        op_role.append({'$match': {"sum": {'$gt': 9}}})
        op_role.append({'$lookup': {
                            'from': 'People',
                            'localField': '_id',
                            'foreignField': '_id',
                            'as': 'info'}})
        op_role.append({'$match': {"info": {'$eq': []}}})
        json_operations[field.replace(".", "_")+'_img'] = op_role

    ob3 = db.Film.aggregate([
        {'$facet': json_operations},
    ])

    uris = []
    uris2 = []
    for x in ob3:
        for y in x:
            if (y == 'actors_img') or (y == 'crew_director_img'):
                for z in x[y]:
                    uris.append(z['_id'])
            else:
                for z in x[y]:
                    uris2.append(z['_id'])
    if len(uris) > 0:
        print('da aggiungere persone (con immagini) ' + str(len(uris)))
        fillMongodb(uris, True)
        '''
        t1 = Thread(target=fillMongodb, args=(uris, True))
        t2 = Thread(target=fillMongodb, args=(uris2, False))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        '''
    if len(uris2) > 0:
        print('da aggiungere persone (no immagini) ' + str(len(uris2)))
        fillMongodb(uris2, False)


def mainSetNames2():
    try:
        mainSetNames()
    except:
        mainSetNames2()


if __name__ == '__main__':
    mainSetNames()
