from mongodb import db
from themes import themes, mini, nano
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup, SoupStrainer
import time
from utils.cleanUsers import cleanUsers

url = 'http://letterboxd.com/films/ajax/theme/relationship-comedy'


def fill_db(url, i, type, code, stat, soup, pag):
    list = []
    movies = soup.find_all('div', {"class": "poster"})
    for movie in movies:
       list.append(int(movie['data-film-id']))
    if pag == 1:
        try:
            num = int(soup.text.split("are ", 1)[1].split("\xa0", 1)[0])
        except:
            print("ERRORE: " + url)
            return
        name = soup.find('span', {"class": "capitalize"}).text
        db.Themes.update_one({'_id': code + i}, {'$set': {'uri': url, 'num': num, 'name': name, 'type': type, 'stat': stat}, '$addToSet': {'list': {'$each': list}}}, True)
    else:
        db.Themes.update_one({'_id': code + i}, {'$addToSet': {'list': {'$each': list}}}, True)
    db.Film.update_many({"_id": {"$in": list}}, {'$addToSet': {'genres.' + type: code + i}})


async def get(url, i, type, code, stat, session):
    try:
        url2 = type + '/' + url
        if stat == 'N':
            max_num = 3
        else:
            max_num = 4
        for h in range(1, max_num):
            async with session.get(url='http://letterboxd.com/films/ajax/' + url2 + "/size/small/page/"+str(h)+"/") as response:
                    resp = await response.read()
                    soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div', 'section']))
                    fill_db(url, i, type, code, stat, soup, h)
    except:
        time.sleep(1)
        await get(url, i, type, code, stat, session)


async def main2(urls, type, code, stat):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, i, type, code, stat, session) for i, url in enumerate(urls)])


def set(target, type, code, stat):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(target, type, code, stat))


def base():
    db.Film.update_many({}, {'$unset': {'genres.theme': 1}})
    db.Themes.delete_many({'type': {'$eq': 'theme'}})
    set(themes, 'theme', 0, 'T')
    print('themes ok')


def minifun():
    db.Themes.delete_many({'type': {'$eq': 'mini-theme'}})
    db.Film.update_many({}, {'$unset': {'genres.mini-theme': 1}})
    num = 50
    for x in range(int(len(mini)/num)):
        set(mini[x * num:(x * num) + num], 'mini-theme', 10000 + x * num, 'T')
        print(str(x * num + num) + ' mini-themes ok')
        time.sleep(1)
    set(mini[int(len(mini)/num)*num:], 'mini-theme', 10000 + int(len(mini)/num) * num, 'T')
    print(str(len(mini)) + ' mini-themes ok')


def nanofun():
    db.Themes.delete_many({'type': {'$eq': 'nanogenre'}})
    db.Film.update_many({}, {'$unset': {'genres.nanogenre': 1}})
    num = 100
    for x in range(int(len(nano)/num)):
        set(nano[x * num:(x * num) + num], 'nanogenre', 20000 + x * num, 'N')
        print(str(x * num + num) + ' nanogenres ok')
        time.sleep(1)
        """
        while True:
            try:
                set(nano[x*num:(x*num)+num], 'nanogenre', 20000+x*num, 'N')
                print(str(x*num+num) + ' nanogenres ok')
                break
            except Exception as e:
                print(e)
                time.sleep(5)
                pass
        """
    set(nano[int(len(nano)/num)*num:], 'nanogenre', 20000 + int(len(nano)/num) * num, 'N')
    print(str(len(nano)) + ' nanogenres ok')


def ttry(f):
    try:
        f()
        return
    except:
        ttry(f())


def all():
    base()
    minifun()
    nanofun()


if __name__ == '__main__':
    base()
    #nanofun()
