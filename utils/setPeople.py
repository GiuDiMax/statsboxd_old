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
import time

global images_tmdb


def fill_db3(url, resp, image, studio):
    json1 = {}
    json1['_id'] = url[1]
    json1['name'] = url[2]
    json1['update'] = datetime.today()
    json1['uri'] = url[3]
    json1['tmdb'] = url[0]
    try:
        try:
            json1['tmdbImg'] = str(resp).rsplit('"profile_path":"', 1)[1].rsplit('"', 1)[0]
        except:
            json1['imgNone'] = True
    except:
        print('error tmdb for ' + url[1])
    if studio:
        db.Studios.update_one({'_id': json1['_id']}, {'$set': json1}, True)
    else:
        db.People.update_one({'_id': json1['_id']}, {'$set': json1}, True)
    #try:
    #    db.People.insert_one(json1)
    #except:
    #    db.People.update_one({'_id': json1['_id']}, {'$set': json1})


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


def fill_db(url, soup, image, studio, uri):
    uri = str(uri).rsplit('/', 2)[1]
    global images_tmdb
    json1 = {}
    json1['_id'] = url
    json1['update'] = datetime.today()
    json1['uri'] = uri
    passare_oltre = False
    try:
        name = (str(soup.find("h1", {"class": "title-1"})).split("</span>", 1)[1].split("</h1>", 1)[0]).strip()
        json1['name'] = name
        if not studio:
            try:
                tmdb = int(soup.find("div", {"class": "js-tmdb-person-bio"})['data-tmdb-id'])
                json1['tmdb'] = tmdb
                if image:
                    images_tmdb.append([tmdb, url, name, uri])
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
            if studio:
                db.Studios.update_one({'_id': json1['_id']}, {'$set': json1}, True)
            else:
                db.People.update_one({'_id': json1['_id']}, {'$set': json1}, True)
            #try:
            #    db.People.insert_one(json1)
            #except:
            #    db.People.update_one({'_id': json1['_id']}, {'$set': json1}, True)
    except:
        print("Errore: " + str(url))
        #db.People.delete_one({'_id': url})
        pass


async def get(url, session, image, studio):
    async with session.get(url='http://letterboxd.com/writer/contributor:' + str(url) + "/") as response:
        resp = await response.read()
        soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
        fill_db(url, soup, image, studio, response.url)


async def main2(urls, image, studio):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session, image, studio) for url in urls])


def fillMongodb2(urls, image, studio):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls, image, studio))


def fillMongodb(urls, image, studio=False):
    global images_tmdb
    n = 100
    if len(urls) < n:
        images_tmdb = []
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
                                   'sum': {'$sum': 1},
                                   'pop': {'$avg': '$rating.num'}}})
        op_role.append({'$match': {'$or': [{"sum": {'$gt': 4}}, {"pop": {'$gt': 100000}}]}})
        op_role.append({'$sort': {"sum": -1, 'pop': -1}})
        #if field in ['actors', 'crew.director']:
        #    op_role.append({'$match': {"sum": {'$lt': 10}}})
        if field == 'studio':
            op_role.append({'$lookup': {
                                'from': 'Studios',
                                'localField': '_id',
                                'foreignField': '_id',
                                'as': 'info'}})
        else:
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
                                   'sum': {'$sum': 1},
                                   'pop': {'$avg': '$rating.num'}}})
        op_role.append({'$match': {"pop": {'$gt': 0}}})
        op_role.append({'$match': {'$or': [{"sum": {'$gt': 9}}, {"pop": {'$gt': 100000}}]}})
        op_role.append({'$sort': {"sum": -1, 'pop': -1}})
        op_role.append({'$lookup': {
                            'from': 'People',
                            'localField': '_id',
                            'foreignField': '_id',
                            'as': 'info'}})
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
                    if z not in uris:
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


def mainSetNamesExt():
    listt = []
    studioss = []
    json_operations = {}
    for year in ['', '_2015', '_2016', '_2017', '_2018', '_2019', '_2020', '_2021', '_2022', '_2023', '_2024']:
        for field in field2 + ['studio']:
            for set in ['mostWatched', 'topRated']:
                op_role = []
                op_role.append({'$project': {'_id': '$stats' + year + '.' + set+field.replace(".", "_")+'._id'}})
                op_role.append({'$unwind': '$_id'})
                op_role.append({'$match': {'_id': {'$type': 16}}})
                json_operations[year+set+field.replace(".", "_")] = op_role
    ob3 = list(db.Users.aggregate([
        {'$facet': json_operations},
    ]))[0]

    for y in ob3:
        studio = 'studio' in y
        for z in ob3[y]:
            if studio:
                if z['_id'] not in studioss:
                    studioss.append(z['_id'])
            else:
                if z['_id'] not in listt:
                    listt.append(z['_id'])

    print('da aggiungere no immagini ' + str(len(listt)))
    fillMongodb(listt, False)
    print('da aggiungere studios ' + str(len(studioss)))
    fillMongodb(studioss, False, True)


def mainSetNames2():
    try:
        mainSetNames()
    except:
        time.sleep(5)
        mainSetNames2()


def testNames():
    obj = list(db.Users.aggregate([
        {'$match': {'_id': 'ale_ich'}},
        {'$project': {'_id': 1, 's': '$stats.topRatedcrew_director'}}
    ]))
    print(obj)


if __name__ == '__main__':
    #fillMongodb([71480], True)
    mainSetNamesExt()
    #mainSetNames2()
    #testNames()
