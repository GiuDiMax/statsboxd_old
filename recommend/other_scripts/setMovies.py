import pandas as pd
from mongodb import db

df = pd.read_csv('ratings.csv', low_memory=False, error_bad_lines=False, encoding_errors='ignore')
df[['movieId']] = df[['movieId']].apply(pd.to_numeric, errors='coerce')
df = df.dropna().astype({"movieId": int})
df = df[['movieId']].groupby(['movieId']).size().to_frame('size').nlargest(7000, 'size')
movies = df.index.tolist()
obj = db.Film.aggregate([
    {'$match': {"_id": {'$in': movies}}},
    {'$project': {'_id': 1, 'uri': 1}}
])
df = pd.DataFrame(obj)
df.rename(columns={'_id': 'movieId'}, inplace=True)
df.to_csv('movies.csv', index=False)
