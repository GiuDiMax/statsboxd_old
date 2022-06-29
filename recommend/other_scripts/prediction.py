from surprise import Dataset, Reader, KNNWithZScore, KNNWithMeans, BaselineOnly, SVD
import random
import pickle
import os
import time


def adasfasfas(filename):
    reader = Reader(sep=',', skip_lines=1, line_format='user item rating', rating_scale=(1, 10))
    data = Dataset.load_from_file(filename, reader=reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo = algo.fit(trainset)
    return algo


def prediction(username, uwatched):
    reader = Reader(sep=',', skip_lines=1, line_format='user item rating', rating_scale=(1, 10))
    data = Dataset.load_from_file('lbd/' + username+".csv", reader=reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo = algo.fit(trainset)
    prediction_set = [('0', str(x), '0') for x in uwatched]
    predictions = algo.test(prediction_set)
    top_n = [(iid, est) for uid, iid, true_r, est, _ in predictions]
    top_n.sort(key=lambda x: (x[1], random.random()), reverse=True)
    return top_n[:10]


if __name__ == '__main__':
    username = ''
    with open('lbd/' + username+'.pickle', 'rb') as handle:
        uwatched = pickle.load(handle)
    prediction(username, uwatched)
    os.remove('lbd/' + username+'.pickle')


