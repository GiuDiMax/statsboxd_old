import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
from mongodb import db
from datetime import datetime
from stats import getStats
from operations import fillMongodb
from threading import Thread
import time
from year_stats import year_stats
global watched_list, diary_list
from datetime import datetime
#from recommend.multiUsers import predictUser


def diary_function(sup):
    diaryx = {}
    diaryx['id'] = int(sup.find("div", class_="film-poster")['data-film-id'])
    dRating = int(sup.find("td", class_="td-rating rating-green").input['value'])
    if dRating > 0:
        diaryx['dRating'] = dRating
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
    #diaryx['uri'] = sup.find("td", class_="td-film-details").div['data-film-slug'].split("/")[-2]
    diaryx['date'] = datetime.strptime(date, '%Y/%m/%d')
    diary_list.append(diaryx)


def diary_function_threading(url):
    ret = requests.request("GET", url)
    soup = BeautifulSoup(ret.text, 'lxml', parse_only=SoupStrainer(['tr'])).find_all('tr')
    for sup in soup[1:]:
        diary_function(sup)


async def get_watched3(url, session, diary):
    global watched_list, diary_list
    async with session.get(url=url) as response:
        ret = await response.read()
    if diary:
        soup = BeautifulSoup(ret, 'lxml', parse_only=SoupStrainer(['tr'])).find_all('tr')
        for sup in soup[1:]:
            diary_function(sup)

        #sys.setrecursionlimit(0x100000)
        #if __name__ == '__main__':
        #    with Pool(5) as p:
        #        p.map(diary_function, [soup[1:]])

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
                    watched['rating'] = rating
            except:
                pass
            #if len(sup.p.find_all('span')) > 1:
            #    watched['liked'] = True
            #else:
            #    watched['liked'] = False
            watched_list.append(watched)


async def get_watched2(urlx, diary):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_watched3(url, session, diary) for url in urlx])


def get_watched(username, diary, fastUpdate):
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
                if fastUpdate:
                    urls.append('http://letterboxd.com/' + str(username) + '/films/diary/for/' + str(datetime.now().year) + '/page/' + str(i+1) +"/")
                else:
                    urls.append('http://letterboxd.com/' + str(username) + '/films/diary/page/' + str(i + 1) + "/")
        else:
            for i in range(pages):
                    urls.append('http://letterboxd.com/' + str(username) + '/films/page/' + str(i + 1) + "/")
    except:
        urls = [url]

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(get_watched2(urls, diary))



def threadgeneral(username, fastUpdate=False):
    if not fastUpdate:
        start3 = time.time()
        resp = requests.get('http://letterboxd.com/' + str(username))
        soup = BeautifulSoup(resp.text, 'lxml', parse_only=SoupStrainer('div', {'id': 'content'}))
        sup = soup.find('div', class_="profile-summary")
        db.Users.update_one({'_id': username}, {'$set': {'name': sup.find('h1', {'class': 'title-1'}).text, 'image': sup.find('img')['src']}}, True)
        print('general in: ' + str(time.time() - start3))


def threadxwatched(username, fastUpdate=False):
    global watched_list
    start2 = time.time()
    get_watched(username, False, fastUpdate)
    db.Users.update_one({'_id': username}, {'$set': {'watched': watched_list}}, True)
    """
    if not fastUpdate:
        start2 = time.time()
        predictUser(username, watched_list)
        print('Recommendations in : ' + str(time.time() - start2))
    """
    print('watched in: ' + str(time.time() - start2))


def threadxdiary(username, fastUpdate=False):
    global diary_list
    start3 = time.time()
    get_watched(username, True, fastUpdate)
    db.Users.update_one({'_id': username}, {'$set': {'diary': diary_list}}, True)
    #year_stats(username)
    print('diary in: ' + str(time.time() - start3))


def fullUpdate(username, fastUpdate):
    global watched_list, diary_list
    start = time.time()
    print('analysis username')
    t1 = Thread(target=threadxwatched, args=(username, fastUpdate)) #WATCHED
    t2 = Thread(target=threadxdiary, args=(username, fastUpdate)) #DIARY
    t3 = Thread(target=threadgeneral, args=(username, fastUpdate)) #GENERAL
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    if len(watched_list) > 0:
        fullOperation(username, fastUpdate, watched_list)
        print('All op in: ' + str(time.time() - start))
        return True
    else:
        return False


def fullOperation(username, fastUpdate, watched=None):
    if watched is None:
        username_object = db.Users.find_one({"_id": username})
        watched = username_object['watched']
    ids = []
    uris = []
    start3 = time.time()
    for movie in watched:
        ids.append(movie['id'])
        uris.append(movie['uri'])

    #db.tmpUris.delete_many({})
    #if len(uris) > 0:
    #    db.tmpUris.insert_many(watched)

    while True:
        obj1 = db.Film.find({"_id": {"$in": ids}})
        uris2 = list(set(uris) - set(obj1.distinct('uri')))
        print('check new in: ' + str(time.time() - start3))
        print('film da aggiungere: ' + str(len(uris2)))
        if len(uris2) > 0:
            try:
                fillMongodb(uris2)
            except:
                pass
        else:
            break

    #y = None
    #getStats(username)
    #db.Users.update_one({'_id': username}, {'$set': {'stats': y}})
    start4 = time.time()
    t1 = Thread(target=getStats, args=(username,))
    t2 = Thread(target=year_stats, args=(username, fastUpdate))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('stats in: ' + str(time.time() - start4))


def getFromusername(username):
    obj = db.Users.find_one({"_id": username})
    if obj is not None:
        return obj
    fullUpdate(username, False)
    return db.Users.find_one({"_id": username})


def checkUsername(username):
    return db.Users.find_one({"_id": username})


if __name__ == '__main__':
    #fullUpdate('giudimax', False)
    threadxdiary('giudimax', fastUpdate=False)
