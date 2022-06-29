import pandas as pd
from surprise import SVD
from surprise import Dataset, Reader, accuracy, KNNWithZScore, BaselineOnly, KNNBasic
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
import csv
import pickle


def main():
    with open('../lbd/movies.csv', newline='') as f:
        reader = csv.reader(f)
        movies = list(reader)[1:]
    reader = Reader(sep=',', skip_lines=1, line_format='user item rating', rating_scale=(1, 10))
    testset = pd.read_csv('../lbd/testSet.csv')
    testset = Dataset.load_from_df(testset[['userId', 'movieId', 'rating']], reader)
    testset = [testset.df.loc[i].to_list() for i in range(len(testset.df))]
    with open('algo.pkl', 'rb') as f:
        algo = pickle.load(f)
    print(algo.test(testset))

'''
    for movie in movies:
        pred = algo.predict('150', str(movie[0]))
        print(pred)
'''

if __name__ == '__main__':
    main()
