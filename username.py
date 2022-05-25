import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
from mongodb import db
from datetime import datetime

global listx


async def get_watched3(url, session, diary):
    async with session.get(url=url) as response:
        ret = await response.read()
    if diary:
        soup = BeautifulSoup(ret, 'lxml').find_all('tr')
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

            test = sup.find("td", class_="td-day diary-day center")
            date = test.a['href'].split("/", 5)[5][:-1]
            test = sup.find("td", class_="td-film-details")
            diaryx['uri'] = test.div['data-film-slug'].split("/")[-2]
            diaryx['date'] = datetime.strptime(date, '%Y/%m/%d')
            listx.append(diaryx)
    else:
        soup = BeautifulSoup(ret, 'lxml').find_all('li', class_="poster-container")
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
            listx.append(watched)


async def get_watched2(urlx, diary):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_watched3(url, session, diary) for url in urlx])


def get_watched(username, diary=False):
    global listx
    listx = []
    if diary:
        url = 'http://letterboxd.com/' + str(username) + '/films/diary/page/1/'
    else:
        url = 'http://letterboxd.com/' + str(username) + '/films/page/1/'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml', parse_only=SoupStrainer('div', {'class': 'paginate-pages'}))
    pages = int(soup.find_all('li', class_="paginate-page")[-1].text)
    urls = []
    for i in range(pages):
        if diary:
            urls.append('http://letterboxd.com/' + str(username) + '/films/diary/page/' + str(i+1) +"/")
        else:
            urls.append('http://letterboxd.com/' + str(username) + '/films/page/' + str(i + 1) + "/")
    asyncio.get_event_loop().run_until_complete(get_watched2(urls, diary))
    return listx


def getFromusername(username):
    obj = db.Users.find_one({"username": username})
    if obj is not None:
        return obj
    try:
        watched_list = get_watched(username, False)
        diary_list = get_watched(username, True)
        db.Users.insert_one({'username': username, 'watched': watched_list, 'diary': diary_list})
        return db.Users.find_one({"username": username})
    except:
        return None

