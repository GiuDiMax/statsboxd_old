import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup, SoupStrainer
from mongodb import db
from datetime import datetime
#import requests
#import lxml
#from config import exclude_people
from config import gen_l, lan_l, cou_l

json0 = []


def fill_db(url, soup):
    json1 = {}
    try:
        #json_lb = json.loads(soup.find("script", {"type": "application/ld+json"}).text.split('*/', 1)[1].split('/*', 1)[0])
        json_lb = json.loads(
            soup.find("script", {"type": "application/ld+json"}).text.split('/* <![CDATA[ */', 1)[1].split('/* ]]> */', 1)[0])
    except:
        print("elimino " + url)
        db.Film.delete_one({'uri': url})
        return

    if int(json_lb['dateModified'].split("-", 1)[0]) < datetime.now().year:
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
            for link in links:
                if 'TMDb' in link['data-track-action'] and '/movie/' in link['href']:
                    json1['tmdb'] = int(link['href'].split('/')[-2])
                if 'TMDb' in link['data-track-action'] and '/tv/' in link['href']:
                    json1['tmdb_tv'] = int(link['href'].split('/')[-2])
                if 'IMDb' in link['data-track-action']:
                    json1['imdb'] = str(link['href'].split('/')[-2])
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
                json1['genres']['main'].append(gen_l.index(genre['href'].split("/")[3]))
                #json1['genres']['main'].append(genre['href'].split("/")[3])
    except:
        pass

    # DETAILS
    try:
        details = soup.find('div', {"id": "tab-details"})
        details_set = details.find_all('div', class_="text-sluglist")
        details_type = details.find_all('span')
        for i in range(len(details_set)):
            typex = str(details_type[i].text).lower()
            details2 = details_set[i].find_all('a')
            if typex == 'original language':
                typex = 'language'
            elif typex == 'original languages':
                typex = 'language'
            elif typex == 'spoken languages':
                typex = 'spoken_lang'
            elif typex == 'spoken language':
                typex = 'spoken_lang'
            elif typex == 'language':
                typex = 'language'
            elif typex == 'languages':
                typex = 'language'
            elif typex == 'country':
                typex = 'country'
            elif typex == 'countries':
                typex = 'country'
            elif typex == 'studio':
                typex = 'studio'
            elif typex == 'studios':
                typex = 'studio'
            for code in details2:
                if typex == 'studio':
                    code = code['href'].split("/")[-2]
                elif typex == 'country':
                    code = cou_l.index(code['href'].split("/")[-2])
                elif typex == 'language':
                    code = lan_l.index(code['href'].split("/")[-2])
                elif typex == 'spoken_lang':
                    code = lan_l.index(code['href'].split("/")[-2])
                else:
                    code = code['href'].split("/")[-2]
                try:
                    json1[typex].append(code)
                except:
                    json1[typex] = [code]
    except:
        pass

    # ACTORS
    try:
        actors = soup.find('div', {"id": "tab-cast"}).select('a')
        json1['actors'] = []
        for actor in actors:
            try:
                #code = int(actor['href'].split('/actor/contributor:')[-1][:-1])
                code = actor['href'].split("/")[-2]
                try:
                    title = actor['title']
                except:
                    title = ""
                #if 'uncredited' not in actor['title'] and 'voice' not in actor['title']:
                #if code not in exclude_people and 'uncredited' not in title:
                if ('uncredited' not in title) and ('archive footage' not in title) and ('Additional Voices' not in title):
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
            #code = int(crew.split("/")[-2].replace("contributor:", ""))
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
        if "https://a.ltrbxd.com/resized/" in poster:
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
    rels = soup.find_all('div', {"class": "linked-film-poster"})
    if len(rels) > 0:
        json1['related'] = []
    for rel in rels:
        json1['related'].append(int(rel['data-film-id']))

    #DATE
    json1['updateDate'] = datetime.today()
    json1['modifiedDate'] = datetime.strptime(json_lb['dateModified'], '%Y-%m-%d')
    json1['updateRating'] = datetime.today()


    obj = db.Film.find_one({'uri': json1['uri']})
    if obj is not None:
        if 'genres' in obj:
            if 'theme' in obj['genres']:
                json1['genres']['theme'] = obj['genres']['theme']
            if 'mini-theme' in obj['genres']:
                json1['genres']['mini-theme'] = obj['genres']['mini-theme']
            if 'nanogenre' in obj['genres']:
                json1['genres']['nanogenre'] = obj['genres']['nanogenre']

        #if 'statsLists' in obj:
        #    json1['statsLists'] = obj['statsLists']

        for xx in ['statsLists', 'members', 'updateMembers']:
            if xx in obj:
                json1[xx] = obj[xx]


    #if __name__ == '__main__':
    #    print(json1)

    db.Film.delete_one({'uri': json1['uri']})
    db.Film.update_one({'_id': json1['_id']}, {'$set': json1}, True)

    #OLD#db.Film.update_one({'uri': json1['uri']}, {'$set': json1}, True)


def fill_dbMembers(url, soup):
    try:
        members = soup.find('a', {"class": "icon-watched"})['title']
        members = members.split('Watched by ', 1)[1].split("member", 1)[0].replace(",", "")
        db.Film.update_one({'uri': url}, {'$set': {'members': int(members), 'updateMembers': datetime.today()}}, True)
    except:
        db.Film.update_one({'uri': url}, {'$set': {'updateMembers': datetime.today()}}, True)


def fill_dbRatings(url, soup):
    try:
        rating = {}
        rr = soup.find('a', {"class": "display-rating"})['title']
        rating['average'] = float(rr.split("of ", 1)[1].split(" based", 1)[0])
        rating['num'] = int(rr.split("based on ", 1)[1].split("ratings", 1)[0].replace(",", ""))
        db.Film.update_one({'uri': url}, {'$set': {'rating': rating, 'updateRating': datetime.today()}}, True)
    except:
        db.Film.update_one({'uri': url}, {'$set': {'updateRating': datetime.today()}}, True)


async def get(url, session, members, ratings):
    if members:
        async with session.get(url='https://letterboxd.com/esi/film/' + url + "/stats/") as response:
                resp = await response.read()
                soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['li']))
                fill_dbMembers(url, soup)
    elif ratings:
        async with session.get(url='https://letterboxd.com/csi/film/' + url + "/rating-histogram/") as response:
                resp = await response.read()
                soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['span']))
                fill_dbRatings(url, soup)
    else:
        async with session.get(url='http://letterboxd.com/film/' + url + "/") as response:
                resp = await response.read()
                soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div', 'a', 'p', 'h1', 'small', 'script']))
                fill_db(url, soup)


async def main2(urls, members=False, ratings=False):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session, members, ratings) for url in urls])


def fillMongodb(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls))
    #return asyncio.get_event_loop().run_until_complete(main2(urls))


def fillMongodbmembers(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls, True, False))


def fillMongodbratings(urls):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls, False, True))


if __name__ == '__main__':
    uris = ['war-horse']
    fillMongodb(uris)
    fillMongodbratings(uris)
    fillMongodbmembers(uris)

