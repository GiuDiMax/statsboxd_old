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

global images_tmdb


def fill_db3(url, resp, image, studio):
    json1 = {}
    json1['_id'] = url[1]
    json1['name'] = url[2]
    try:
        try:
            json1['tmdbImg'] = str(resp).rsplit('"profile_path":"', 1)[1].rsplit('"', 1)[0]
        except:
            json1['imgNone'] = True
    except:
        print('error tmdb for ' + url[1])
    try:
        db.People.insert_one(json1)
    except:
        db.People.update_one({'_id': json1['_id']}, {'$set': json1})


async def get3(url, session, image, studio):
    async with session.get(url="https://api.themoviedb.org/3/person/" + str(url[0]) + "?api_key=" + api_tmdb + "&language=en-US") as response:
            resp = await response.read()
            #soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
            fill_db3(url, resp, image, studio)


async def main3(urls, image, studio):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get3(url, session, image, studio) for url in urls])


def fillMongodb3(urls, image, studio):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main3(urls, image, studio))


def fill_db(url, soup, image, studio):
    global images_tmdb
    json1 = {}
    json1['_id'] = url
    passare_oltre = False
    try:
        name = (str(soup.find("h1", {"class": "title-1"})).split("</span>", 1)[1].split("</h1>", 1)[0]).strip()
        json1['name'] = name
        if not studio:
            try:
                tmdb = int(soup.find("div", {"class": "js-tmdb-person-bio"})['data-tmdb-id'])
                json1['tmdb'] = tmdb
                if image:
                    images_tmdb.append([tmdb, url, name])
                    #req = "https://api.themoviedb.org/3/person/" + str(tmdb) + "?api_key=" + api_tmdb + "&language=en-US"
                    #x = requests.get(req)
                    #try:
                    #    json1['tmdbImg'] = x.text.rsplit('"profile_path":"', 1)[1].rsplit('"', 1)[0]
                    #except:
                    #    json1['imgNone'] = True
                    passare_oltre = True
            except:
                print('error tmdb for ' + url)
        if not passare_oltre:
            try:
                db.People.insert_one(json1)
            except:
                db.People.update_one({'_id': json1['_id']}, {'$set': json1})
    except:
        pass


async def get(url, session, image, studio):
    async with session.get(url='http://letterboxd.com/writer/' + url + "/") as response:
            resp = await response.read()
            soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
            fill_db(url, soup, image, studio)


async def main2(urls, image, studio):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session, image, studio) for url in urls])


def fillMongodb2(urls, image, studio):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls, image, studio))
    #return asyncio.get_event_loop().run_until_complete(main2(urls))


def fillMongodb(urls, image, studio=False):
    global images_tmdb
    n = 100
    if len(urls) < n:
        fillMongodb2(urls, image, studio)
        if image:
            fillMongodb3(images_tmdb, image, studio)
    else:
        urlsx = urls[:n]
        images_tmdb = []
        fillMongodb2(urlsx, image, studio)
        if image:
            fillMongodb3(images_tmdb, image, studio)
        print("aggiunti " + str(n) + " nuovi record")
        fillMongodb(urls[n:], image, studio)


def mainSetNames():
    json_operations = {}
    for field in field2 + ['studio']:
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

    for field in ['crew.director', 'actors']:
        op_role = []
        op_role.append({'$unwind': '$'+field})
        op_role.append({'$group': {'_id': '$'+field,
                                   'sum': {'$sum': 1}}})
        #if 'director' in field:
        #    op_role.append({'$match': {"sum": {'$gt': 4}}})
        #else:
        #    op_role.append({'$match': {"sum": {'$gt': 9}}})
        op_role.append({'$match': {"sum": {'$gt': 4}}})
        op_role.append({'$sort': {"sum": -1}})
        op_role.append({'$lookup': {
                            'from': 'People',
                            'localField': '_id',
                            'foreignField': '_id',
                            'as': 'info'}})
        #op_role.append({'$match': {"info": {'$eq': []}}})
        op_role.append({'$match': {"info.tmdbImg": {'$exists': False}}})
        op_role.append({'$match': {"info.imgNone": {'$exists': False}}})
        json_operations[field.replace(".", "_")+'_img'] = op_role

    ob3 = db.Film.aggregate([
        {'$facet': json_operations},
    ])

    uris = []
    uris2 = []
    uris3 = []
    for x in ob3:
        for y in x:
            if (y == 'actors_img') or (y == 'crew_director_img'):
                for z in x[y]:
                    uris.append(z['_id'])
            elif y == 'studio':
                for z in x[y]:
                    uris3.append(z['_id'])
            else:
                for z in x[y]:
                    uris2.append(z['_id'])

    if len(uris) > 0:
        print('da aggiungere con immagini ' + str(len(uris)))
        fillMongodb(uris, True)

    if len(uris2) > 0:
        print('da aggiungere no immagini ' + str(len(uris2)))
        fillMongodb(uris2, False)

    if len(uris3) > 0:
        print('da aggiungere studios ' + str(len(uris3)))
        fillMongodb(uris3, False, True)


def mainSetNames2():
    try:
        mainSetNames()
    except:
        mainSetNames2()


if __name__ == '__main__':
    mainSetNames()
