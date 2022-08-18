import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup, SoupStrainer
from mongodb import db
from datetime import datetime, timedelta
import requests
import lxml
from config import exclude_people

json0 = []


def fill_db(url, soup):
    json1 = {}

    try:
        json_lb = json.loads(soup.find("script", {"type": "application/ld+json"}).text.split('*/', 1)[1].split('/*', 1)[0])
    except:
        print("elimino " + url)
        db.Film.delete_one({'uri': url})
        return

    #ID
    try:
        json1['_id'] = int(soup.find("div", {"class": "film-poster"})['data-film-id'])
    except:
        print("errore " + url)
        return
    json1['uri'] = url

    #TITLE & YEAR
    try:
        json1['title'] = soup.find("h1", {"class": "headline-1 js-widont prettify"}).text
        json1['year'] = int(soup.find("small", {"class": "number"}).text)
    except:
        pass

    #TMDB e IMDB LINK
    try:
        links = soup.findAll("a", {"class": "micro-button track-event"})
        if 'href' in str(links[0]):
            json1['imdb'] = int(links[0]['href'].split('/')[-2].replace("tt", ""))
            json1['tmdb'] = int(links[1]['href'].split('/')[-2])
    except:
        pass

    # RUNTIME
    try:
        json1['runtime'] = int(soup.find('p', class_="text-link text-footer").text.replace("Adult", "").strip().split("min", 1)[0].strip().replace(",", ""))
    except:
        pass

    #GENRES
    try:
        genres = soup.find('div', {"id": "tab-genres"}).select('a')
        #json1['genres'] = {'main': [], 'themes': [], 'mini-themes': []}
        json1['genres'] = {'main': []}
        for genre in genres:
            '''
            if "/theme/" in str(genre['href']):
                json1['genres']['themes'].append(genre['href'].split("/")[3])
            if "/mini-theme/" in str(genre['href']):
                json1['genres']['mini-themes'].append(genre['href'].split("/")[3])
            '''
            if "/genre/" in str(genre['href']):
                json1['genres']['main'].append(genre['href'].split("/")[3])
    except:
        pass

    # DETAILS
    try:
        details = soup.find('div', {"id": "tab-details"})
        details = details.find_all('a', class_="text-slug")
        for detail in details:
            detail = detail['href']
            type = detail.split("/")[-3]
            code = detail.split("/")[-2]
            try:
                json1[type].append(code)
            except:
                json1[type] = [code]
    except:
        pass

    # ACTORS
    try:
        actors = soup.find('div', {"id": "tab-cast"}).select('a')
        json1['actors'] = []
        for actor in actors:
            try:
                code = actor['href'].split('/actor/')[-1][:-1]
                try:
                    title = actor['title']
                except:
                    title = ""
                #if 'uncredited' not in actor['title'] and 'voice' not in actor['title']:
                #if code not in exclude_people and 'uncredited' not in title:
                if 'uncredited' not in title:
                    json1['actors'].append(code)
            except:
                pass
    except:
        pass

    # CREWS
    try:
        crews = soup.find('div', {"id": "tab-crew"}).select('a')
        json1['crew'] = {}
        for crew in crews:
            crew = crew['href']
            role = crew.split("/")[-3]
            code = crew.split("/")[-2]
            try:
                json1['crew'][role].append(code)
            except:
                json1['crew'][role] = [code]
    except:
        pass

    #COLLECTIONS
    try:
        #json2 = {}
        collection = soup.find('section', {"id": "related"})
        link = collection.find('h2', {"class": "section-heading"}).find("a")['href']
        json1['collection'] = link.split("/", 4)[3]
    except:
        pass

    #USERS
    try:
        json1['rating'] = {'num': int(json_lb['aggregateRating']['ratingCount']), 'average': float(json_lb['aggregateRating']['ratingValue'])}
    except:
        pass

    #POSTERS and BACKDROP
    try:
        #poster = soup.find('div', {"class": "film-poster"}).select('img')[0]['src']
        #poster = poster.rsplit("-0-", 2)[0].replace("https://a.ltrbxd.com/resized/", "")
        poster = soup.find('script', {"type": "application/ld+json"}).text.split('"image":"', 1)[1].split('",', 1)[0]
        poster = poster.rsplit("-0-", 2)[0].replace("https://a.ltrbxd.com/resized/", "")
        try:
            backdrop = soup.find('div', {"class": "backdrop-wrapper"})['data-backdrop']
            backdrop = backdrop.rsplit("-1200-1200-", 1)[0].replace("https://a.ltrbxd.com/resized/", "")
            json1['images'] = {'poster': poster, 'backdrop': backdrop}
        except:
            json1['images'] = {'poster': poster}
    except:
        pass

    # RELATEDMOVIES
    json1['related'] = []
    rels = soup.find_all('div', {"class": "linked-film-poster"})
    for rel in rels:
        json1['related'].append(int(rel['data-film-id']))

    #DATE
    json1['updateDate'] = datetime.today()
    json1['modifiedDate'] = datetime.strptime(json_lb['dateModified'], '%Y-%m-%d')


    if __name__ == '__main__':
        print(json1)

    db.Film.delete_one({'uri': json1['uri']})
    #db.Film.update_one({'_id': json1['_id']}, {'$set': json1}, True)

    #OLD#db.Film.update_one({'uri': json1['uri']}, {'$set': json1}, True)


async def get(url, session):
    async with session.get(url='http://letterboxd.com/film/' + url + "/") as response:
            resp = await response.read()
            soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div', 'a', 'p', 'h1', 'small', 'script']))
            fill_db(url, soup)


async def main2(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session) for url in urls])


def fillMongodb(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls))
    #return asyncio.get_event_loop().run_until_complete(main2(urls))


if __name__ == '__main__':
    fillMongodb(['breakfast-at-tiffanys'])
