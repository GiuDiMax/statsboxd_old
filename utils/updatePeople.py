from mongodb import db
from datetime import datetime, timedelta
from setPeople import fillMongodb, mainSetNames


def test():
    lista = list(db.People.aggregate([
        #{'$match': {'tmdbImg': {'$exists': True}}},
        #{'$match': {'tmdb': {'$exists': True}}},
        {'$match': {'update': {'$exists': True}}},
        {'$project': {'_id': 1}}
    ]))
    uris = [str(x['_id']) for x in lista]
    print(uris[:100])
    fillMongodb(uris, False)


def prePeople():
    datex = datetime.today()
    datex = datex - timedelta(days=365)
    lista = list(db.People.aggregate([
        {'$match': {'tmdbImg': {'$exists': True}}},
        {'$match': {'$or': [{'update': {'$lt': datex}}, {'update': {'$exists': False}}]}},
        {'$match': {'tmdb': {'$exists': False}}},
        {'$project': {'_id': 1}}
    ]))
    uris = [str(x['_id']) for x in lista]
    print("da pre aggiornare: " + str(len(uris)))
    #print(uris[:100])
    fillMongodb(uris, False)


def upPeople():
    datex = datetime.today()
    datex = datex - timedelta(days=365)
    lista = list(db.People.aggregate([
        {'$match': {'tmdbImg': {'$exists': True}}},
        {'$match': {'$or': [{'update': {'$lt': datex}}, {'update': {'$exists': False}}]}},
        {'$match': {'tmdb': {'$exists': True}}},
        {'$project': {'_id': 1}}
    ]))
    uris = [str(x['_id']) for x in lista]
    print("da aggiornare: " + str(len(uris)))
    fillMongodb(uris, True)


if __name__ == '__main__':
    #json1 = {'_id': 'kaan-guldur', 'update': datetime.today(), 'name': 'Kaan Guldur', 'tmdb': 1877487}
    #db.People.update_one({'_id': json1['_id']}, {'$set': json1}, True)
    #exit()
    #test()
    prePeople()
    upPeople()
    mainSetNames()
