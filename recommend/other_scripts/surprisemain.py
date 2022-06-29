import pandas as pd
from surprise import SVD
from surprise import Dataset, Reader, accuracy, KNNWithZScore, BaselineOnly, KNNBasic, SVDpp
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
import csv
import pickle
import time


def save_object(obj, filename):
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def test(data):
    start = time.time()
    trainset, testset = train_test_split(data, test_size=.25)
    algo = BaselineOnly()
    predictions = algo.fit(trainset).test(testset)
    accuracy.rmse(predictions)
    print('baseline in ' + str(time.time()-start))
    start = time.time()
    algo = SVDpp()
    predictions = algo.fit(trainset).test(testset)
    accuracy.rmse(predictions)
    print('SVDpp in ' + str(time.time()-start))
    start = time.time()
    algo = KNNBasic()
    predictions = algo.fit(trainset).test(testset)
    accuracy.rmse(predictions)
    print('KNNBasic in ' + str(time.time()-start))
    start = time.time()
    algo = KNNWithZScore()
    predictions = algo.fit(trainset).test(testset)
    accuracy.rmse(predictions)
    print('KNNWithZScore in ' + str(time.time()-start))


def main():
    #ratings = pd.read_csv("dataset/ratings_min.csv", sep=",", low_memory=False).drop(columns=['timestamp'])
    #movies = pd.read_csv("dataset/movies.csv", sep=",", low_memory=False)
    #tags = pd.read_csv("dataset/tags.csv", sep=",", low_memory=False)
    reader = Reader(sep=',', skip_lines=1, line_format='user item rating', rating_scale=(1, 10))
    data = Dataset.load_from_file("lbd/ratings_clean.csv", reader=reader)
    #data = Dataset.load_from_file("dataset/ratings_min.csv", reader=reader)

    test(data)

    #test(data)
    #data = Dataset.load_from_file("dataset/ratings_min.csv", reader=reader)


if __name__ == '__main__':
    main()
