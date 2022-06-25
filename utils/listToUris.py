import aiohttp
import asyncio
import requests
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import time

db = pd.DataFrame()
db1 = pd.DataFrame()
db2 = pd.DataFrame()

def fill_db(soup, i):
    #TITLE & YEAR
    try:
        title = soup.find("h1", {"class": "headline-1 js-widont prettify"}).text
        year = soup.find("small", {"class": "number"}).text
        db.loc[i, 'Title'] = title
        db.loc[i, 'Year'] = year
    except:
        pass

    #TMDB e IMDB LINK
    try:
        links = soup.findAll("a", {"class": "micro-button track-event"})
        try:
            imdb = links[0]['href']
            imdb = imdb.split("/")[4]
            db.loc[i, 'imdb'] = imdb
        except:
            pass
        try:
            tmdb = links[1]['href']
            tmdb = tmdb.split("/")[4]
            db.loc[i, 'tmdb'] = tmdb
        except:
            pass
    except:
        pass

async def get_watched3(url, session):
    async with session.get(url=url) as response:
        ret = await response.read()
        soup = BeautifulSoup(ret, 'lxml').find_all('li', class_="poster-container")
        for sup in soup:
            i = len(db1)
            i = i + 1
            link = sup.div['data-film-slug']
            # name = sup.img['alt']
            db1.at[i, 'Letterboxd URI'] = link
            # db.at[i, 'Name'] = name

async def get_watched2(urlx):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_watched3(url, session) for url in urlx])
    return db1

def get_list_urls(url):
    resp = requests.get(url)
    try:
        soup = BeautifulSoup(resp.text, 'lxml', parse_only=SoupStrainer('div', {'class': 'paginate-pages'}))
        pages = int(soup.find_all('li', class_="paginate-page")[-1].text)

        # PAGELIMIT
        pages = 30
        #if "1000" in url:
        #    pages = 10

        urlsx = []
        for i in range(pages):
            urlsx.append(url + '/page/' + str(i + 1) + "/")
    except:
        urlsx.append(url)
    db1 = asyncio.get_event_loop().run_until_complete(get_watched2(urlsx))
    return db1

async def get(url, session):
    start = time.time()
    i = len(db)
    db.at[i, 'Letterboxd URI'] = url
    url = 'http://letterboxd.com' + url
    async with session.get(url=url) as response:
        resp = await response.read()
        soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div', 'a', 'p', 'h1', 'small']))
        if i % 100 == 0 and i != 0:
            print(str(i) + " rows analyzed in %s seconds" % round((time.time() - start)))
        fill_db(soup, i)

async def main2(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session) for url in urls])
        return db

def main1(urls):
    db = asyncio.get_event_loop().run_until_complete(main2(urls))
    return db

urls_total = ["https://letterboxd.com/tobiasandersen2/list/random-movie-roulette/by/popular/",
              "https://letterboxd.com/masuddevilliers/list/italian/by/release/",
              "https://letterboxd.com/dave/list/imdb-top-250/",
              "https://letterboxd.com/prof_ratigan/list/top-1000-films-of-all-time/by/popular/"]
for a_url in urls_total:
    db1 = get_list_urls(a_url)
db1 = db1.drop_duplicates()
print(db1)

#db1 = get_list_urls("https://letterboxd.com/tobiasandersen2/list/random-movie-roulette/by/popular/")
#db1 = get_list_urls("https://letterboxd.com/masuddevilliers/list/italian/by/release/")
#db1 = get_list_urls("https://letterboxd.com/momas/list/italian-cinema/")
#db1 = get_list_urls("https://letterboxd.com/louiseudo/list/all-the-movies/by/popular/")

urls = db1["Letterboxd URI"].values
dbf = main1(urls)
dbf.to_csv(r'output.csv', index=False, header=True)
print(dbf)