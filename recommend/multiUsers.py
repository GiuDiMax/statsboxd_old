import pandas as pd
import pickle
import time
from mongodb import db
from surprise import Dataset, Reader, SVD
import random
import os


def createAlgo(populate=False):
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
    userslist = dfx['_id'].unique().tolist()
    dfx.rename(columns={'_id': 'userId'}, inplace=True)
    #userslist = dfx.drop_duplicates(subset=['userId'])['userId'].tolist()
    df = pd.read_csv('ratings_clean.csv', low_memory=False)
    df = pd.concat([df, dfx])
    filename = 'trainset.csv'
    df.to_csv(filename, index=False)
    reader = Reader(sep=',', skip_lines=1, line_format='user item rating', rating_scale=(1, 10))
    data = Dataset.load_from_file(filename, reader=reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo = algo.fit(trainset)
    with open('algo.pickle', 'wb') as handle:
        pickle.dump(algo, handle)
    with open('userslist.pickle', 'wb') as handle:
        pickle.dump(userslist, handle)
    os.remove(filename)
    if populate:
        for user in userslist:
            print("recommendations for " + user)
            predictUser(user)


def predictUser(username, watched_list=None):
    num = 24
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
    with open('algo.pickle', 'rb') as handle:
        algo = pickle.load(handle)
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
    createAlgo(True)
    print(time.time() - start)
