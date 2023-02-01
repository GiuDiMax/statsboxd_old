import aiohttp
import asyncio
from bs4 import BeautifulSoup, SoupStrainer
import pickle
from mongodb import db
import threading
import requests

url = "https://letterboxd.com/tobiasandersen2/list/random-movie-roulette/by/popular/page/"
max = 95
#max = 3
lista = []
lista2 = []

async def get(url, session):
    async with session.get(url=url) as response:
        pag = int(url.rsplit("/", 1)[-1])
        if pag < 31:
            diff = 1
        elif pag < 62:
            diff = 2
        else:
            diff = 3
        resp = await response.read()
        soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['div']))
        films = soup.find_all('div', {'class': 'film-poster'})
        for film in films:
            lista.append([int(film['data-film-id']), diff])
        with open('lista9000.pickle', 'wb') as handle:
            pickle.dump(lista, handle)


async def main2(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get(url, session) for url in urls])


def fill():
    urls = []
    for i in range(max-1):
        urls.append(url + str(i+1))
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main2(urls))
    #return asyncio.get_event_loop().run_until_complete(main2(urls))


def associa():
    with open('lista9000.pickle', 'rb') as handle:
        listax = pickle.load(handle)
    print(listax)
    obj = db.Film.aggregate([
        #{'$match': {'_id': listax[0]}}
        {'$match': {'_id': {'$in': listax}}},
        {'$match': {'tmdb': {'$gt': 0}}},
        {'$project': {'title': 1, 'tmdb': 1}},
    ])
    listab = []
    for a in obj:
        listab.append([a['title'], a['tmdb']])
    print(listab)
    with open('listabis.pickle', 'wb') as handle:
        pickle.dump(listab, handle)


def mongo_tmdb(element):
    a = db.Film.find_one(element[0])
    if a is not None:
        if 'tmdb' in a:
            req = "https://api.themoviedb.org/3/movie/"+str(a['tmdb'])+"?api_key=6fff7e293df6a808b97101a26c86a545&language=it"
            r = requests.get(req)
            try:
                titolo2 = r.text.rsplit('title":"', 1)[1].split('"', 1)[0]
                lista2.append([a['title'], titolo2, a['tmdb'], element[1]])
            except:
                print(r.text)


def ass2():
    with open('lista9000.pickle', 'rb') as handle:
        listax = pickle.load(handle)
    lx = len(listax)
    a = int(lx/20)
    for j in range(int(lx/a)):
        print(j*a)
        thh = []
        for element in listax[j*a:j*a + a - 1]:
            thh.append(threading.Thread(target=mongo_tmdb, args=(element,)))
        for t in thh:
            t.start()
        for t in thh:
            t.join()
    mongo_tmdb(listax[-1])
    with open('listabis.pickle', 'wb') as handle:
        pickle.dump(lista2, handle)

#fill()
#associa()
ass2()