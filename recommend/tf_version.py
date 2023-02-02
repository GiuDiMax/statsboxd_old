import pandas as pd
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt
import os
import tempfile
from mongodb import db
from threading import Thread

EMBEDDING_SIZE = 32
LOCAL_DIR = os.getcwd()
test = False
save = False
predict_sample = False
fullpredict = True


def predictuser(model, df, movie_df, movie2movie_encoded, username):
    movies_watched_by_user = df.loc[df['userId'] == username]
    movies_not_watched = movie_df[~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)]["movieId"]
    movies_not_watched = list(set(movies_not_watched).intersection(set(movie2movie_encoded.keys())))
    movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]
    user_movie_array = np.hstack(([[0]] * len(movies_not_watched), movies_not_watched))
    ratings = model.predict(user_movie_array).flatten()
    top_ratings_indices = ratings.argsort()[-50:][::-1]
    recommended_movie_ids = [movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices]
    obj = db.Film.aggregate([
        {'$match': {'_id': {'$in': recommended_movie_ids}}},
        {'$project': {'_id': 1, 'uri': 1, 'poster': '$images.poster'}},
    ])
    obja = []
    for x in obj:
        obja.append(x)
    top = []
    i = 0
    for y in recommended_movie_ids:
        for x in obja:
            if int(x['_id']) == int(y):
                j = {}
                j['uri'] = x['uri']
                j['poster'] = x['poster']
                j['perc'] = int(99 - i*0.5)
                top.append(j)
        i = i+1
    db.Users.update_one({'_id': username}, {'$set': {'sug': top}})


class RecommenderNet(keras.Model):
    def __init__(self, num_users, num_movies, embedding_size, **kwargs):
        super().__init__(**kwargs)
        self.num_users = num_users
        self.num_movies = num_movies
        self.embedding_size = embedding_size
        self.user_embedding = layers.Embedding(
            num_users,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.user_bias = layers.Embedding(num_users, 1)
        self.movie_embedding = layers.Embedding(
            num_movies,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.movie_bias = layers.Embedding(num_movies, 1)

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)
        # Add all the components (including bias)
        x = dot_user_movie + user_bias + movie_bias
        # The sigmoid activation forces the rating to between 0 and 1
        return tf.nn.sigmoid(x)


df1 = pd.read_csv("trainset.csv", header=0, low_memory=False)
if test:
    df = df1.sample(3000)
else:
    df = df1
user_ids = df["userId"].unique().tolist()
user2user_encoded = {x: i for i, x in enumerate(user_ids)}
userencoded2user = {i: x for i, x in enumerate(user_ids)}
movie_ids = df["movieId"].unique().tolist()
movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
df["user"] = df["userId"].map(user2user_encoded)
df["movie"] = df["movieId"].map(movie2movie_encoded)
num_users = len(user2user_encoded)
num_movies = len(movie_encoded2movie)
df["rating"] = df["rating"].values.astype(np.float32)
min_rating = min(df["rating"])
max_rating = max(df["rating"])


x = df[["user", "movie"]].values
y = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
df1['rating'] = df1["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
train_indices = int(0.9 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:],
)

model = RecommenderNet(num_users, num_movies, EMBEDDING_SIZE)
model.compile(loss=tf.keras.losses.BinaryCrossentropy(), metrics=["accuracy"], optimizer=keras.optimizers.Adam(learning_rate=0.001))
history = model.fit(
    x=x_train,
    y=y_train,
    batch_size=64,
    epochs=5,
    verbose=1,
    validation_data=(x_val, y_val),
)
model.summary()
test_loss = model.evaluate(x_val, y_val)
print('\\nTest Loss: {}'.format(test_loss))
print("Testing Model with 1 user")
if predict_sample:
    movie_df = pd.read_csv("movies.csv")
    user_id = "new_user"
    movies_watched_by_user = df.sample(100)
    movies_not_watched = movie_df[
        ~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)
    ]["movieId"]
    movies_not_watched = list(
        set(movies_not_watched).intersection(set(movie2movie_encoded.keys()))
    )
    movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]
    user_movie_array = np.hstack(
        ([[0]] * len(movies_not_watched), movies_not_watched)
    )
    ratings = model.predict(user_movie_array).flatten()
    top_ratings_indices = ratings.argsort()[-10:][::-1]
    recommended_movie_ids = [
        movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices
    ]
    print("Showing recommendations for user: {}".format(user_id))
    print("====" * 9)
    print("Movies with high ratings from user")
    print("----" * 8)
    top_movies_user = (
        movies_watched_by_user.sort_values(by="rating", ascending=False)
        .head(5)
        .movieId.values
    )
    movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
    for row in movie_df_rows.itertuples():
        print(row.uri)
    print("----" * 8)
    print("Top 10 movie recommendations")
    print("----" * 8)
    recommended_movies = movie_df[movie_df["movieId"].isin(recommended_movie_ids)]
    for row in recommended_movies.itertuples():
        print(row.uri)
    print("==="* 9)
if fullpredict:
    movie_df = pd.read_csv("movies.csv")
    obj = db.Users.aggregate([{'$project': {'_id': 1}}])
    userslist = []
    for x in obj:
        userslist.append(x['_id'])
    num = 10
    for i in range(int(len(userslist) / num)):
        threads = []
        for j in range(num):
            t = Thread(target=predictuser, args=(model, df1, movie_df, movie2movie_encoded, userslist[j + i*num], ))
            threads.append(t)
        for x in threads:
            x.start()
        for x in threads:
            x.join()
    threads2 = []
    for z in range(int(len(userslist) / num), len(userslist)):
        t2 = Thread(target=predictuser, args=(model, df1, movie_df, movie2movie_encoded, userslist[z], ))
        threads2.append(t2)
    for x2 in threads2:
        x2.start()
    for x2 in threads2:
        x2.join()

if save:
    print("Saving Model")
    print("==="* 9)
    MODEL_DIR = tempfile.gettempdir()
    version = 1
    export_path = os.path.join(LOCAL_DIR, f"ai-model/model/{version}")
    print('export_path = {}\\n'.format(export_path))
    tf.keras.models.save_model(
        model,
        export_path,
        overwrite=True,
        include_optimizer=True,
        save_format=None,
        signatures=None,
        options=None
    )
