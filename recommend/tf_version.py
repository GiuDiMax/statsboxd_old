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
    obj = db.Users.aggregate([
        {'$match': {'_id': username}},
        {'$project': {'watched': 1}},
        {'$unwind': '$watched'},
        {'$project': {'_id': 0, 'id': '$watched.id'}},
    ])
    watched = []
    for x in obj:
        watched.append(x['id'])
    movies_not_watched = movie_df[~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)]["movieId"]
    movies_not_watched = list(set(movies_not_watched).intersection(set(movie2movie_encoded.keys())))
    movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]
    user_movie_array = np.hstack(([[0]] * len(movies_not_watched), movies_not_watched))
    ratings = model.predict(user_movie_array, verbose=0).flatten()
    dbx = pd.DataFrame(ratings)
    dbx = dbx.sort_values(by=[0], ascending=False)
    dbx = dbx.head(200)
    rat2 = dbx[dbx.columns[0]].values.tolist()
    top_ratings_indices = ratings.argsort()[-200:][::-1]
    recommended_movie_ids = [movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices]
    obj = db.Film.aggregate([
        {'$match': {'_id': {'$in': recommended_movie_ids}}},
        {'$project': {'_id': 1, 'uri': 1, 'poster': '$images.poster'}},
    ])
    obja = []
    for x in obj:
        obja.append(x)
    top = []
    z = 0
    for index, y in enumerate(recommended_movie_ids):
        for x in obja:
            if (int(x['_id']) == int(y)) and (int(x['_id']) not in watched):
                j = {}
                j['uri'] = x['uri']
                j['poster'] = x['poster']
                j['perc'] = int(rat2[index]*100)
                top.append(j)
                z = z+1
        if z > 47:
            break
    print("predicted: " + str(username))
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


movie = pd.read_csv('movies.csv', low_memory=False)
movielist = movie['movieId'].tolist()
obj = db.Users.aggregate([
    {'$project': {'_id': 1, 'watched': 1}},
    {'$unwind': '$watched'},
    {'$match': {'watched.rating': {'$gt': 0}}},
    {'$match': {'watched.id': {'$in': movielist}}},
    {'$project': {'_id': 1, 'movieId': '$watched.id', 'rating': '$watched.rating'}},
])
dfa = pd.DataFrame(obj)
dfa.rename(columns={'_id': 'userId'}, inplace=True)
dfb = pd.read_csv('ratings_clean.csv', low_memory=False)
df1 = pd.concat([dfa, dfb])
#df1 = pd.read_csv("trainset.csv", header=0, low_memory=False)
#df1 = df1.sample(frac=1)
#df2 = pd.read_csv("ratings_clean.csv", header=0, low_memory=False)
if test:
    df = df1.sample(10000)
else:
    df = df1.sample(1500000)
df1 = df
user_ids = df["userId"].unique().tolist()
print("utenti: " + str(len(user_ids)))
user2user_encoded = {x: i for i, x in enumerate(user_ids)}
userencoded2user = {i: x for i, x in enumerate(user_ids)}
movie_ids = df["movieId"].unique().tolist()
print("films: " + str(len(movie_ids)))
movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
df["user"] = df["userId"].map(user2user_encoded)
df["movie"] = df["movieId"].map(movie2movie_encoded)
num_users = len(user2user_encoded)
num_movies = len(movie_encoded2movie)
df["rating"] = df["rating"].values.astype(np.float32)
#min_rating = min(df["rating"])
#max_rating = max(df["rating"])
#print("min: " + str(min_rating) + ", max: " + str(max_rating))

x = df[["user", "movie"]].values
y = df["rating"].apply(lambda x: round((x - 1) / (10 - 1), 1)).values
df1['rating'] = df1["rating"].apply(lambda x: round((x - 1) / (10 - 1), 1)).values
train_indices = int(0.9 * df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:],
)

model = RecommenderNet(num_users, num_movies, EMBEDDING_SIZE)
model.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=keras.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])
history = model.fit(
    x=x_train,
    y=y_train,
    batch_size=64,
    epochs=1,
    verbose=1,
    validation_data=(x_val, y_val),
)
model.summary()
test_loss = model.evaluate(x_val, y_val)
print('\\nTest Loss: {}'.format(test_loss))
if predict_sample:
    print("====" * 9)
    for i in range(2):
        #print("Testing Model with 1 user")
        movie_df = pd.read_csv("movies.csv")
        user_id = "new_user_" + str(i)
        movies_watched_by_user = df.sample(500)
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
        ratings = model.predict(user_movie_array, verbose = 0).flatten()
        top_ratings_indices = ratings.argsort()[-10:][::-1]
        recommended_movie_ids = [
            movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices
        ]
        print("Showing recommendations for user: {}".format(user_id))
        #print("====" * 9)
        #print("Movies with high ratings from user")
        print("----" * 8)
        top_movies_user = (
            movies_watched_by_user.sort_values(by="rating", ascending=False)
            .head(5)
            .movieId.values
        )
        movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
        for row in movie_df_rows.itertuples():
            pass
            #print(row.uri)
        #print("----" * 8)
        #print("Top 10 movie recommendations")
        #print("----" * 8)
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
    num = 5
    #predictuser(model, df1, movie_df, movie2movie_encoded, "giudimax")
    #exit()
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
