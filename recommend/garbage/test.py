import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm.data import Dataset


def make_model_for_recommendation_with_dataset():
    _dataset = Dataset()
    _data_pd = pd.read_csv('lbd\\rating_resize.csv')
    movies_pd = pd.read_csv('../lbd/movies.csv')
    _dataset.fit(users=_data_pd["userId"], items=_data_pd["movieId"])
    #ratings_gp = _data_pd["rating"].apply(lambda x: x / 5.0)  #-> 0.0 >= weight >= 1.0
    ratings_gp = _data_pd["rating"]
    interaction_list = (zip(_data_pd["userId"], _data_pd["movieId"], ratings_gp))
    interactions, weights = _dataset.build_interactions(interaction_list)
    model = LightFM(loss='warp')
    model.fit(interactions, num_threads=2)
    items_id_mapping = _dataset.mapping()[2]
    max_inner_id = max(items_id_mapping.values()) + 1
    item_labels = np.empty(max_inner_id, dtype=np.object)
    for movie_id in list(movies_pd['movieId']):
        iid = int(movie_id)
        if iid in items_id_mapping:
            item_labels[items_id_mapping[iid]] = movie_id
    return (model, {
        "train": interactions,
        "item_labels": item_labels,
        "mapping": _dataset.mapping()
    })


def sample_recommendation(_model, _data, user_ids):
    n_users, n_items = _data['train'].shape
    for user_id in user_ids:
        if 'mapping' in _data.keys():
            user_id_mapping, _, _, _ = _data['mapping']
            user_id = user_id_mapping[user_id]
        known_positives = _data['item_labels'][_data['train'].tocsr()[user_id].indices]
        scores = _model.predict(user_id, np.arange(n_items))
        top_items = _data['item_labels'][np.argsort(-scores)]
        print("User %s" % user_id)
        print("     Known positives:")
        for x in known_positives[:6]:
            print("        %s" % x)
        print("     Recommended:")
        for x in top_items[:6]:
            print("        %s" % x)


def recommendations():
    model, data = make_model_for_recommendation_with_dataset()
    while True:
        _user_id = int(input("Enter user id (0 for exit):\n").strip(" \n"))
        if _user_id == 0:
            break
        sample_recommendation(model, data, [_user_id])


recommendations()
