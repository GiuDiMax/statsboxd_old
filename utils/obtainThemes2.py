from mongodb import db
from datetime import date
from bs4 import BeautifulSoup, SoupStrainer
import aiohttp
import asyncio

global list1, list2


def fill_db(url, soup):
    global list1, list2
    temi = soup.find_all('section', {"class": "genre-group"})
    for tema in temi:
        temax = tema.find('a')['href'].split("/")
        if temax[2] == 'mini-theme':
            if temax[3] not in list2:
                list2.append(temax[3])
        else:
            if temax[3] not in list1:
                list1.append(temax[3])


async def get(url, type, session):
    async with session.get(url='http://letterboxd.com/film/' + url + '/' + type) as response:
            resp = await response.read()
            soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['section']))
            fill_db(url, soup)


async def main2(urls, type):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, type, session) for url in urls])


def set(target, type):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(target, type))


def obtain():
    global list1, list2
    current_year = date.today().year
    a = db.Film.aggregate([
        {'$match': {"year": {'$gt': current_year - 2}}},
        {'$sort': {'rating.num': -1}},
        {'$limit': 1000},
        {'$project': {'uri': 1}}
    ])

    uris = []
    for x in a:
        uris.append(x['uri'])
    type = 'themes'
    list1 = []
    list2 = []
    set(uris, type)
    print(list1, list2)
    list1 = []
    list2 = []
    type = 'nanogenres'
    set(uris, type)
    print(list1)


if __name__ == '__main__':
    obtain()
