from mongodb import db
from themes import themes, mini, nano
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup, SoupStrainer
import time
from utils.cleanUsers import cleanUsers

url = 'http://letterboxd.com/films/ajax/theme/relationship-comedy'


def fill_db(soup, x):
   numm = int(soup.text.split('There are ', 1)[1].split("films", 1)[0])
   lista = []
   if numm == x['size']:
       return
   movies = soup.find_all('div', {"class": "poster"})
   for movie in movies:
       lista.append(int(movie['data-film-id']))
   print("update " + x['uri'])
   db.Themes.update_one({'_id': x['_id']}, {'$set': {'num': numm}}, True)
   db.Themes.update_one({'_id': x['_id']}, {'$addToSet': {'list': {'$each': lista}}}, True)
   db.Film.update_many({"_id": {"$in": lista}}, {'$addToSet': {'genres.' + x['type']: x['_id']}})


async def get(x, session):
    url = 'http://letterboxd.com/films/ajax/' + x['type'] + "/" + x['uri'] + "/by/release/size/small/page/1/"
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div', 'section']))
            fill_db(soup, x)
    except:
        print("Errore chiamate")
        time.sleep(1)
        await get(x, session)


async def main2(lista):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(x, session) for x in lista])


def set(lista):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(lista))


def ttry(f):
    try:
        f()
        return
    except:
        ttry(f())


def updateThemes2():
    a = list(db.Themes.aggregate([
        {'$project': {'_id': 1, 'uri': 1, 'type': 1, 'size': '$num'}}
    ]))
    set(a[:1])


def checkThemes():
    nn = []
    a = list(db.Themes.aggregate([
        {'$project': {'_id': 1, 'uri': 1, 'type': 1, 'size': '$num', 'size2': {'$size': '$list'}}}
    ]))
    for x in a:
        if x['size'] != x['size2']:
            nn.append(x['_id'])
    print(nn)


def updateThemes():
    updateThemes2()
    checkThemes()


if __name__ == '__main__':
    updateThemes()
