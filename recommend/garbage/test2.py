import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm.data import Dataset
import csv
from itertools import islice
import json


def get_ratings():
    csvfile = open('lbd\\rating_resize.csv', newline='')
    return csv.DictReader(csvfile, delimiter=',')


def get_features():
    csvfile = open('lbd\\movies_full.csv', newline='')
    return csv.DictReader(csvfile, delimiter=',')


def make_model():
    dataset = Dataset()
    dataset.fit((x['userId'] for x in get_ratings()), (x['movieId'] for x in get_ratings()))
    num_users, num_items = dataset.interactions_shape()
    dataset.fit_partial(items=(x['movieId'] for x in get_features()),
                        item_features=[(x['director'] for x in get_features()),
                                       (x['year'] for x in get_features()),
                                       (x['country'] for x in get_features()),
                                       (x['genre'] for x in get_features()),
                                       (x['theme'] for x in get_features()),
                                       (x['mini'] for x in get_features())])
    interactions, weights = dataset.build_interactions(((x['userId'], x['movieId']) for x in get_ratings()))
    item_features = dataset.build_item_features(((x['movieId'],
                                                  [x['director'], x['year'], x['country'],
                                                   x['genre'], x['theme'], x['mini']]) for x in get_features()))
    model = LightFM(loss='bpr')
    model.fit(interactions, item_features=item_features)
    scores = model.predict(190, np.arange(num_items))
    print(scores)

make_model()
