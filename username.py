import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
from mongodb import db
from datetime import datetime
from stats import getStats, getLists
from operations import fillMongodb
from setPeople import mainSetNames2
from threading import Thread
import time

global watched_list, diary_list
watched_list = []
diary_list = []

async def get_watched3(url, session, diary):
    global watched_list, diary_list
    async with session.get(url=url) as response:
        ret = await response.read()
    if diary:
        soup = BeautifulSoup(ret, 'lxml', parse_only=SoupStrainer(['tr'])).find_all('tr')
        for sup in soup[1:]:
            diaryx = {}
            diaryx['id'] = int(sup.find("div", class_="film-poster")['data-film-id'])
            diaryx['dRating'] = int(sup.find("td", class_="td-rating rating-green").input['value'])
            test = sup.find("td", class_="td-like center diary-like")
            if "icon-liked" in str(test):
                diaryx['dLike'] = True
            else:
                diaryx['dLike'] = False
            if sup.find("td", class_="td-rewatch center"):
                diaryx['rewatch'] = True
            else:
                diaryx['rewatch'] = False
            if sup.find("td", class_="td-review center"):
                diaryx['review'] = True
            else:
                diaryx['review'] = False

            date = sup.find("td", class_="td-day diary-day center").a['href'].split("/", 5)[5][:-1]
            diaryx['uri'] = sup.find("td", class_="td-film-details").div['data-film-slug'].split("/")[-2]
            diaryx['date'] = datetime.strptime(date, '%Y/%m/%d')
            diary_list.append(diaryx)

    else:
        soup = BeautifulSoup(ret, 'lxml', parse_only=SoupStrainer(['li'])).find_all('li', class_="poster-container")
        for sup in soup:
            watched = {}
            watched['id'] = int(sup.div['data-film-id'])
            watched['uri'] = sup.div['data-film-slug'].split("/")[-2]
            try:
                rating = sup.p.span['class'][-1]
                if 'rated' in rating:
                    rating = int(rating.split("-", 1)[1])
                else:
                    rating = ""
                watched['rating'] = rating
            except:
                pass
            if len(sup.p.find_all('span')) > 1:
                watched['liked'] = True
            else:
                watched['liked'] = False
            watched_list.append(watched)


async def get_watched2(urlx, diary):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_watched3(url, session, diary) for url in urlx])


def get_watched(username, diary=False):
    global watched_list, diary_list
    watched_list = []
    diary_list = []
    if diary:
        url = 'http://letterboxd.com/' + str(username) + '/films/diary/page/1/'
    else:
        url = 'http://letterboxd.com/' + str(username) + '/films/page/1/'

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml', parse_only=SoupStrainer('div', {'class': 'paginate-pages'}))
    try:
        pages = int(soup.find_all('li', class_="paginate-page")[-1].text)
        urls = []
        if diary:
            for i in range(pages):
                if diary:
                    urls.append('http://letterboxd.com/' + str(username) + '/films/diary/page/' + str(i+1) +"/")
        else:
            for i in range(pages):
                    urls.append('http://letterboxd.com/' + str(username) + '/films/page/' + str(i + 1) + "/")
    except:
        urls = [url]

    #asyncio.get_event_loop().run_until_complete(get_watched2(urls, diary))
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(get_watched2(urls, diary))


def getFromusername(username):
    obj = db.Users.find_one({"username": username})
    if obj is not None:
        return obj
    fullCreation(username)
    obj = db.Users.find_one({"username": username})
    if obj is not None:
        return obj


def fullCreation(username):
    global watched_list, diary_list
    get_watched(username, False)
    if len(watched_list) > 0:
        get_watched(username, True)
        db.Users.insert_one({'username': username, 'watched': watched_list, 'diary': diary_list})
        #db.Users.insert_one({'username': username, 'watched': watched_list})
        fullOperation(username)


def fullUpdate(username):
    global watched_list, diary_list
    start = time.time()
    t1 = Thread(target=get_watched, args=(username, False))
    t2 = Thread(target=get_watched, args=(username, True))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('watched + diary in: ' + str(time.time() - start))
    start = time.time()
    db.Users.update_one({'username': username}, {'$set': {'watched': watched_list, 'diary': diary_list}})
    fullOperation(username)
    print('stats in: ' + str(time.time() - start))


def fullOperation(username):
    username_object = getFromusername(username)
    watched = username_object['watched']
    ids = []
    uris = []
    for movie in watched:
        ids.append(movie['id'])
        uris.append(movie['uri'])

    db.tmpUris.delete_many({})
    if len(uris) > 0:
        db.tmpUris.insert_many(username_object['watched'])

    while True:
        obj1 = db.Film.find({"_id": {"$in": ids}})
        uris2 = list(set(uris) - set(obj1.distinct('uri')))
        print('film da aggiungere: ' + str(len(uris2)))
        if len(uris2) > 0:
            try:
                fillMongodb(uris2)
            except:
                pass
        else:
            break

    json3 = getStats(username)
    for x in json3:
        y = x

    min = y['totalyear'][0]['_id']
    max = y['totalyear'][-1]['_id']

    y2 = []
    for i in range(min, max + 1):
        check = False
        for a in y['totalyear']:
            if a['_id'] == i:
                y2.append(a)
                check = True
                break
        if not check:
            y2.append({'_id': i, 'average': 0, 'sum': 0})
    y['totalyear'] = y2

    db.Users.update_one({'username': username}, {'$set': {'stats': y}})

fullUpdate('giudimax')

