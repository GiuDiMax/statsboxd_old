from pymongo import MongoClient
from config import client_string
from pprint import pprint

client = MongoClient(client_string, connect=False)
db = client.Letterboxd
#film = {'_id': 0, 'a': '2', 'b': '3'}
#result = db.Film.insert_one(film)
#obj = db.Film.aggregate([{'$limit': 5}])
#for obj0 in obj:
#    print(obj0)