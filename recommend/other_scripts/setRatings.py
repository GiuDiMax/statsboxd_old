import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
import lxml
from threading import Thread
import csv


async def get_watched3(url, userId, session):
    async with session.get(url=url) as response:
        ret = await response.read()
        soup = BeautifulSoup(ret, 'lxml', parse_only=SoupStrainer(['li'])).find_all('li', class_="poster-container")
        for sup in soup:
            movie = (int(sup.div['data-film-id']))
            try:
                rating = sup.p.span['class'][-1]
                if 'rated' in rating:
                    rating = int(rating.split("-", 1)[1])
                    writer.writerow([userId, movie, rating])
            except:
                pass


async def get_watched2(urlx, userId):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_watched3(url, userId, session) for url in urlx])


def threadFunction(user):
    resp = requests.get('http://letterboxd.com/' + user[1] + '/films/by/popular/')
    soup = BeautifulSoup(resp.text, 'lxml', parse_only=SoupStrainer('div', {'class': 'paginate-pages'}))
    try:
        pages = int(soup.find_all('li', class_="paginate-page")[-1].text)
        urls = []
        if pages > 20:
            pages = int(pages*0.8)
        for i in range(pages):
            urls.append('http://letterboxd.com/' + user[1] + '/films/by/popular/page/' + str(i + 1) + "/")
    except:
        urls = ['http://letterboxd.com/' + user[1] + '/films/by/popular/']

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(get_watched2(urls, user[0]))


def get_watched(username = None):
    global writer

    #for user in data:
    #    threadFunction(user)
    if username != None:
        f = open('lbd/'+username+'.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(['userId', 'movieId', 'rating'])
        threadFunction([0, username])
        f.close()

    else:
        f = open('lbd/ratings.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerow(['userId', 'movieId', 'rating'])

        with open('lbd/users.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)[1:]

        rangex = 20

        for z in range(int(len(data)/rangex) + 1):
            try:
                threads = []
                for k in range(rangex):
                    t = Thread(target=threadFunction, args=(data[k + z*rangex],))
                    threads.append(t)
                for x in threads:
                    x.start()
                for x in threads:
                    x.join()
            except:
                for k in range(rangex):
                    try:
                        threadFunction(data[z * rangex + k])
                    except:
                        pass


if __name__ == '__main__':
    get_watched('giudimax')
    #get_watched(None)

