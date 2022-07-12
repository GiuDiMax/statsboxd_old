from setRatings import get_watched
from cleanRatings import cleanRatings
import pandas as pd
from prediction import prediction
import pickle
import os
import time


def singleUser(username, direct=False):
    get_watched(username)
    dfx = pd.read_csv('lbd/'+username+'.csv')
    df = pd.read_csv('lbd/ratings.csv', low_memory=False)
    movies = pd.read_csv('lbd/movies.csv', low_memory=False)
    df2 = cleanRatings(dfx)
    unwatched = pd.merge(movies, df2, on='movieId', how="outer", indicator=True).query('_merge=="left_only"')
    unwatched = unwatched['movieId'].tolist()
    df = pd.concat([df, df2])
    df.to_csv('lbd/' + username + '.csv', index=False)
    if direct:

        with open('lbd/' + username+'.pickle', 'wb') as handle:
            pickle.dump(unwatched, handle, protocol=pickle.HIGHEST_PROTOCOL)
            pred = False
    else:
        pred = prediction(username, unwatched)
    os.remove('lbd/' + username + '.csv')
    return pred


if __name__ == '__main__':
    start = time.time()
    pred = singleUser('giudimax')
    print(pred)
    print(time.time() - start)