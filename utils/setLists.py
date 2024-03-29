from mongodb import db
from config import *
import aiohttp
import asyncio
from bs4 import BeautifulSoup, SoupStrainer
import requests


global uri


async def get_watched3(url, session):
    global uris
    async with session.get(url=url) as response:
        ret = await response.read()
        soup = BeautifulSoup(ret, 'lxml').find_all('li', class_="poster-container")
        for sup in soup:
            movie = sup.div['data-film-slug'].split("/")[2]
            uris.append(movie)


async def get_watched2(urlx):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_watched3(url, session) for url in urlx])


def get_list_urls(url):
    resp = requests.get(url)
    urlsx = []
    try:
        soup = BeautifulSoup(resp.text, 'lxml', parse_only=SoupStrainer('div', {'class': 'paginate-pages'}))
        pages = int(soup.find_all('li', class_="paginate-page")[-1].text)
        for i in range(pages):
            urlsx.append(url + '/page/' + str(i + 1) + "/")
    except:
        urlsx.append(url)
    asyncio.get_event_loop().run_until_complete(get_watched2(urlsx))


def updateLists():
    global uris
    db.Film.update_many({}, {'$unset': {'statsLists': ""}})
    for list in listsSelection:
        print(list[1])
        uris = []
        get_list_urls("https://letterboxd.com/" + list[0])
        try:
            db.Lists.insert_one({'_id': list[0], 'name': list[1], 'uris': uris, 'isStats': True, 'order': list[2], 'num': len(uris)})
        except:
            db.Lists.update_one({'_id': list[0]}, {'$set': {'name': list[1], 'num': len(uris), 'uris': uris, 'isStats': True, 'order': list[2]}})
        db.Film.update_many({"uri": {"$in": uris}}, {'$push': {'statsLists': list[0]}})


if __name__ == '__main__':
    updateLists()
