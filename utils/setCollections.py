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


def fill_db(url, soup):
    try:
        json2 = {}
        json2['_id'] = url
        json2['name'] = soup.find('h1', {"class": "title-1"}).text
        x = requests.get('https://letterboxd.com/films/ajax/in/' + url + "/")
        soup = BeautifulSoup(x.content, 'lxml', parse_only=SoupStrainer(['div', 'section']))
        json2['num'] = int(soup.text.split("are ", 1)[1].split("\xa0", 1)[0])
        json2['numRat'] = 0
        json2['posters'] = []
        ob3 = db.Film.aggregate([
            {'$match': {'collection': url}},
            {'$sort': {'year': 1}},
            {'$limit': 3},
            {'$project': {'_id': 1, 'poster': '$images.poster', 'numRat': '$rating.num'}}
        ])
        for x in ob3:
            json2['posters'].append(x['poster'])
            json2['numRat'] = json2['numRat'] + x['numRat']
        try:
            db.Collections.insert_one(json2)
        except:
            db.Collections.update_one({'_id': json2['_id']}, {'$set': json2})
    except:
        pass


async def get(url, session):
    async with session.get(url='https://letterboxd.com/films/in/' + url + "/") as response:
        resp = await response.read()
        soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
        fill_db(url, soup)


async def main2(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session) for url in urls])


def fillMongodb(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls))
    #asyncio.get_event_loop().run_until_complete(main2(urls))


def mainSetCollection():
    json_operations = {}
    op_role = []
    op_role.append({'$unwind': '$collection'})
    op_role.append({'$group': {'_id': '$collection',
                               'sum': {'$sum': 1}}})
    op_role.append({'$match': {"sum": {'$gt': 2}}})
    op_role.append({'$lookup': {
                        'from': 'Collections',
                        'localField': '_id',
                        'foreignField': '_id',
                        'as': 'info'}})
    op_role.append({'$match': {"info": {'$eq': []}}})
    #op_role.append({'$match': {"info.numRat": {'$exists': False}}})
    json_operations['collection'] = op_role

    ob3 = db.Film.aggregate([
        {'$facet': json_operations},
    ])

    uris = []
    for x in ob3:
        for y in x:
            for z in x[y]:
                uris.append(z['_id'])
    print(len(uris))
    fillMongodb(uris)


def mainSetCollection2():
    while True:
        try:
            mainSetCollection()
            break
        except:
            pass


if __name__ == '__main__':
    #mainSetCollection2()
    fillMongodb(['venom-collection-1'])
