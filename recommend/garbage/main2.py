import pandas as pd
import csv
import pickle
from lightfm import LightFM
from lightfm.datasets import fetch_movielens
from lightfm.evaluation import precision_at_k
import csv
import numpy as np
import scipy.sparse as sps


def save_object(obj, filename):
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def _process_data(row_array):
    return row_array


def sparse(input_file_name):
    sep = ","
    sp_data = []
    with open(input_file_name) as csv_file:
        for row in csv_file:
            data = np.fromstring(row, sep=sep)
            data = _process_data(data)
            data = sps.coo_matrix(data)
            sp_data.append(data)
    sp_data = sps.vstack(sp_data)
    return sp_data


def save_object(obj, filename):
    with open(filename, 'wb') as outp:
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def main2():
    data = sparse('../lbd/ratings.csv')
    save_object(data, 'sparseMatrix.pkl')
    model = LightFM(loss='warp')
    model = model.fit(data, epochs=30, num_threads=2)
    save_object(model, 'model.pkl')


def main():
    with open('sparseMatrix.pkl', 'rb') as f:
        data = pickle.load(f)
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    n_users, n_items = data.shape
    #test = sparse('lbd\\testSet.csv')
    #model = model.fit_partial(test, epochs=30)
    scores = model.predict(190, np.arange(n_items))
    print(scores)


if __name__ == '__main__':
    main()
