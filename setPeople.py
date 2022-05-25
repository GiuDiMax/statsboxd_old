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

json0 = []

def fill_db(url, soup):
    json1 = {}
    json1['_id'] = url
    json1['name'] = (str(soup.find("h1", {"class": "title-1"})).split("</span>", 1)[1].split("</h1>", 1)[0]).strip()
    tmdb = int(soup.find("div", {"class": "js-tmdb-person-bio"})['data-tmdb-id'])
    json1['tmdb'] = tmdb
    req = "https://api.themoviedb.org/3/person/"+str(tmdb)+"?api_key="+api_tmdb+"&language=en-US"
    x = requests.get(req)
    try:
        json1['tmdbImg'] = x.text.rsplit('"profile_path":"', 1)[1].rsplit('"', 1)[0]
    except:
        pass
    db.People.insert_one(json1)
    return json1

async def get(url, session):
    async with session.get(url='http://letterboxd.com/writer/' + url + "/") as response:
            resp = await response.read()
            soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
            json0.append(fill_db(url, soup))

async def main2(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session) for url in urls])
        return json0

def fillMongodb(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    return asyncio.get_event_loop().run_until_complete(main2(urls))
    #return asyncio.get_event_loop().run_until_complete(main2(urls))


def mainSetNames():
    json_operations = {}
    for field in field2:
        op_role = []
        op_role.append({'$unwind': '$'+field})
        op_role.append({'$group': {'_id': '$'+field,
                                   'sum': {'$sum': 1}}})
        op_role.append({'$match': {"sum": {'$gt': 2}}})
        op_role.append({'$lookup': {
                            'from': 'People',
                            'localField': '_id',
                            'foreignField': '_id',
                            'as': 'info'}})
        op_role.append({'$match': {"info": {'$eq': []}}})
        json_operations[field.replace(".", "_")] = op_role

    ob3 = db.Film.aggregate([
        {'$facet': json_operations},
    ])

    uris = []
    for x in ob3:
        for y in x:
            for z in x[y]:
                uris.append(z['_id'])
    fillMongodb(uris)

def mainSetNames2():
    while True:
        try:
            mainSetNames()
            break
        except:
            pass
