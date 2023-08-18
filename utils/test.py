from mongodb import db
from time import time
import requests
from bs4 import BeautifulSoup, SoupStrainer

def test():
    start = time()
    obj = list(db.Users.aggregate([
        {'$match': {'_id': 'the_jyggalag'}},
        {'$project': {'watched': 1}},
        {'$unwind': '$watched'},
        {'$project': {'_id': '$watched.id'}},
        {'$lookup': {'from': 'Film',
                     'localField': '_id',
                     'foreignField': '_id',
                     'as': 'info'}},
        {'$project': {'_id': 1, 'uri': '$info.uri', 'actor': '$info.actors', 'r': '$info.rating.average'}},
        {'$unwind': '$uri'},
        {'$unwind': '$actor'},
        {'$match': {'actor': 'john-dimaggio-3'}},
        {'$sort': {'r': -1}},
        {'$project': {'_id': '$uri'}}
    ]))
    #print(obj)
    #print(len(obj))
    #print(time() - start)
    rx = []
    for x in obj:
        rx.append(x['_id'])
    return rx


def test2():
    urlx = 'https://letterboxd.com/the_jyggalag/films/with/actor/john-dimaggio-3/by/rating/'
    resp = requests.get(urlx).text
    soup = BeautifulSoup(resp, 'lxml', parse_only=SoupStrainer(['li']))
    r = soup.find_all('li', {"class": "poster-container"})
    rx = []
    for x in r:
        rx.append(x.div['data-target-link'].split("/")[-2])
    return rx


if __name__ == '__main__':
    a = test2()
    b = test()
    for e in a:
        if e not in b:
            print(e)
