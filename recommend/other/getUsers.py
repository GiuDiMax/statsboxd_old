import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup, SoupStrainer
import lxml
import csv


async def get_users3(url, session):
    global writer, y
    async with session.get(url=url) as response:
        ret = await response.read()
        soup = BeautifulSoup(ret, 'lxml', parse_only=SoupStrainer(['tr'])).find_all('a', class_='name')
        for sup in soup:
            y = y+1
            writer.writerow([y, sup['href'].split("/")[1]])


async def get_users2(urlx):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[get_users3(url, session) for url in urlx])


def get_users(url):
    global writer, y
    y = 0
    f = open('users.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['id', 'username'])
    urls = []
    for i in range(50):
        urls.append(url + str(i + 1) + "/")
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(get_users2(urls,))
    f.close()


url = 'https://letterboxd.com/members/popular/page/'
get_users(url)