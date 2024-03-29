import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, Embedding, Flatten, Dot, Add, Activation
from mongodb import db
import warnings
from threading import Thread, Semaphore

global recommendations
global df
global tops
samplex = 1500000
sem = Semaphore()


def creaDf(usery):
    global recommendations
    global df
    global sem
    try:
        user = df[df['userId'] == usery]['user_id'].values[0]
        watched_movies = df[df['user_id'] == user]['movie_id']
        not_watched_movies = np.delete(np.arange(num_movies), watched_movies)
        predictions = model.predict([np.array([user] * len(not_watched_movies)), not_watched_movies], verbose=0)
        recommendations_user = pd.DataFrame({'user_id': [user] * len(not_watched_movies),
                                             'movie_id': not_watched_movies,
                                             'score': predictions.flatten()})
        #recommendations.append(recommendations_user)
        sem.acquire()
        recommendations = pd.concat([recommendations, recommendations_user])
        sem.release()
    except:
        pass


def creaPrediction(usery):
    global df
    global tops
    try:
        user = df[df['userId'] == usery]['user_id'].values[0]
        obj = db.Users.aggregate([
            {'$match': {'_id': usery}},
            {'$project': {'watched': 1}},
            {'$unwind': '$watched'},
            {'$project': {'_id': 0, 'id': '$watched.id'}},
        ])
        watched = []
        for x in obj:
            watched.append(x['id'])
        recs = []
        recommended_movie_ids = []
        user_tops = tops[tops['user_id'] == user]
        for index, row in user_tops.iterrows():
            recs.append([row['movie_name'], row['score']])
            recommended_movie_ids.append(row['movie_name'])
            # print(f"{row['movie_name']} - {row['score'] * 100:.2f}% preferenza")
        obj = db.Film.aggregate([
            {'$match': {'_id': {'$in': recommended_movie_ids}}},
            {'$project': {'_id': 1, 'uri': 1, 'poster': '$images.poster'}},
        ])
        obja = []
        for x in obj:
            obja.append(x)
        top = []
        top2 = []
        z = 0
        for movie in recs:
            for x in obja:
                if int(x['_id']) == int(movie[0]) and int(movie[0]) not in watched:
                    #if z < 48:
                    j = {}
                    j['uri'] = x['uri']
                    j['poster'] = x['poster']
                    j['perc'] = int(movie[1] * 90)
                    top.append(j)
                    #top2.append({'_id': x['_id'], 'perc': int(movie[1] * 100)})
                    z = z + 1
                    break
            #if z > 500:
            if z > 47:
                break
        db.Users.update_one({'_id': usery}, {'$set': {'sug': top}})
        #db.Users.update_one({'_id': usery}, {'$set': {'sug_list': top2}})
        print("username: " + str(usery) + "\n")
    except:
        print("errore: " + str(usery))


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
if samplex is not None:
    dfb = dfb.sample(samplex)
df = pd.concat([dfa, dfb])
print("Total size: " + str(len(df)))

# Normalizzazione
df['rating'] = df['rating'] / 10.0

# Creazione di un dizionario per gli id degli utenti e dei film
user_id = {id: i for i, id in enumerate(df['userId'].unique())}
movie_id = {id: i for i, id in enumerate(df['movieId'].unique())}
df['user_id'] = df['userId'].map(user_id)
df['movie_id'] = df['movieId'].map(movie_id)

# Divisione del dataset in train e test set
train, test = train_test_split(df, test_size=0.2)

# Creazione del modello di rete neurale
num_users = len(user_id)
num_movies = len(movie_id)
embedding_size = 64

# Input layers
user_input = Input(shape=[1])
user_embedding = Embedding(num_users, embedding_size)(user_input)
user_vec = Flatten()(user_embedding)
movie_input = Input(shape=[1])
movie_embedding = Embedding(num_movies, embedding_size)(movie_input)
movie_vec = Flatten()(movie_embedding)

# Dot product layer
prod = Dot(axes=1)([user_vec, movie_vec])

# Bias terms
user_bias = Embedding(num_users, 1)(user_input)
user_bias = Flatten()(user_bias)
movie_bias = Embedding(num_movies, 1)(movie_input)
movie_bias = Flatten()(movie_bias)
prod = Add()([prod, user_bias, movie_bias])

# Output activation function
output = Activation('relu')(prod)

# Modello finale
model = Model(inputs=[user_input, movie_input], outputs=output)
model.compile(loss='mean_squared_error', optimizer='adam')

# Addestramento del modello
#early_stopping = EarlyStopping(monitor='val_loss', patience=1, verbose=1, mode='min')
model.fit([train['user_id'], train['movie_id']], train['rating'],
          validation_data=([test['user_id'], test['movie_id']], test['rating']),
          epochs=2, verbose=1,
          #callbacks=[early_stopping],
          batch_size=64)

obj = db.Users.aggregate([
    {'$match': {'watched.1': {'$exists': True}}},
    {'$project': {'_id': 1}}
])
users = []
for x in obj:
    users.append(x['_id'])

recommendations = pd.DataFrame()
warnings.simplefilter(action='ignore', category=FutureWarning)
print("creo dataframe")
tth = []
#for userx in users:
for userx in users:
    tth.append(Thread(target=creaDf, args=(userx,)))
for t in tth:
    t.start()
for t in tth:
    t.join()
print("creo raccomandazioni")
recommendations = recommendations.sort_values(by=['user_id', 'score'], ascending=False)
tops = recommendations.groupby('user_id').head(1000)
tops['movie_name'] = tops['movie_id'].apply(lambda x: list(movie_id.keys())[list(movie_id.values()).index(x)])
tops.to_csv('recc.csv', index=False)
tth = []
#for userx in users:
for userx in users:
    tth.append(Thread(target=creaPrediction, args=(userx,)))
for t in tth:
    t.start()
for t in tth:
    t.join()
