import pandas as pd
import pickle
import time
from mongodb import db
from surprise import Dataset, Reader, SVD
import random
import os
from threading import Thread
#from setLists import updateLists
#from setPeople import mainSetNames
#from setCollections import mainSetCollection2
#from setThemes import all
#from cleanUsers import cleanUsers


def createAlgo(populate=False, algo=False):
    if algo:
        df = pd.read_csv('movies.csv', low_memory=False)
        movielist = df['movieId'].tolist()
        obj = db.Users.aggregate([
            {'$project': {'_id': 1, 'watched': 1}},
            {'$unwind': '$watched'},
            {'$match': {'watched.rating': {'$gt': 0}}},
            {'$match': {'watched.id': {'$in': movielist}}},
            {'$project': {'_id': 1, 'movieId': '$watched.id', 'rating': '$watched.rating'}},
        ])
        dfx = pd.DataFrame(obj)
        #dfx = pd.merge(dfx, df, on='movieId', how='right')
        userslist = dfx['_id'].unique().tolist()
        dfx.rename(columns={'_id': 'userId'}, inplace=True)
        #dfx = dfx.drop(columns=['uri', 'average']).dropna().sort_values(by=['userId'])
        #userslist = dfx.drop_duplicates(subset=['userId'])['userId'].tolist()
        df = pd.read_csv('ratings_clean.csv', low_memory=False)
        df = pd.concat([df, dfx])
        filename = 'trainset.csv'
        df.to_csv(filename, index=False)
        reader = Reader(sep=',', skip_lines=1, line_format='user item rating', rating_scale=(1, 10))
        data = Dataset.load_from_file(filename, reader=reader)
        #reader = Reader(rating_scale=(1, 10))
        #data = Dataset.load_from_df(df, reader=reader)
        trainset = data.build_full_trainset()
        print("trainset ready, fitting...")
        algo = SVD()
        algo = algo.fit(trainset)
        print("predicting...")
        with open('algo.pickle', 'wb') as handle:
            pickle.dump(algo, handle)
        with open('userslist.pickle', 'wb') as handle:
            pickle.dump(userslist, handle)
        os.remove(filename)
    else:
        with open('userslist.pickle', 'rb') as handle:
            userslist = pickle.load(handle)
    num = 5
    with open('algo.pickle', 'rb') as handle:
        algox = pickle.load(handle)
    if populate:
        for i in range(int(len(userslist)/num)):
            threads = []
            for j in range(num):
                t = Thread(target=predictUser, args=(userslist[j + i*num], algox))
                threads.append(t)
            for x in threads:
                x.start()
            for x in threads:
                x.join()
        threads2 = []
        for z in range(int(len(userslist)/num), len(userslist)):
            t2 = Thread(target=predictUser, args=(userslist[z], algox))
            threads2.append(t2)
        for x2 in threads2:
            x2.start()
        for x2 in threads2:
            x2.join()


def predictUser(username, algo, watched_list=None):
    print("predicting " + username)
    num = 60
    if watched_list is None:
        obj = db.Users.aggregate([
            {'$match': {'_id': username}},
            {'$project': {'movieId': '$watched.id'}},
        ])
        a = []
        for x in obj:
            a = x
            a = a['movieId']
            break
        watched = pd.DataFrame({'movieId': a})
    else:
        if len(watched_list) <= 0:
            return
        with open('userslist.pickle', 'rb') as handle:
            userslist = pickle.load(handle)
            if username not in userslist:
                return
        watched = pd.DataFrame(watched_list)
        watched = watched.rename(columns={'id': 'movieId'})
    movies = pd.read_csv('movies.csv', low_memory=False)
    unwatched = pd.merge(movies, watched, on='movieId', how="outer", indicator=True).query('_merge=="left_only"')
    unwatched = unwatched['movieId'].tolist()
    prediction_set = [(username, str(x), '0') for x in unwatched]
    predictions = algo.test(prediction_set)
    top_n = [(iid, est) for uid, iid, true_r, est, _ in predictions]
    top_n.sort(key=lambda x: (x[1], random.random()), reverse=True)
    top = []
    top_num = top_n[:num]
    for x in top_num:
        top.append(int(x[0]))
    obj = db.Film.aggregate([
        {'$match': {'_id': {'$in': top}}},
        {'$project': {'_id': 1, 'uri': 1, 'poster': '$images.poster'}},
    ])
    top = []
    for x in obj:
        j = {}
        for y in top_num:
            if x['_id'] == int(y[0]):
                j['uri'] = x['uri']
                j['poster'] = x['poster']
                j['perc'] = int(y[1]*10)
                top.append(j)
                break
    top = sorted(top, key=lambda d: d['perc'], reverse=True)
    db.Users.update_one({'_id': username}, {'$set': {'sug': top}})


if __name__ == '__main__':
    start = time.time()
    createAlgo(True, True)
    '''
    updateLists()
    mainSetNames()
    mainSetCollection2()
    cleanUsers()
    '''
    print(time.time() - start)
