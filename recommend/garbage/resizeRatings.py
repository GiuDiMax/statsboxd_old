import pandas as pd

ratings = pd.read_csv('../lbd/ratings.csv', low_memory=False)
movies = pd.read_csv('../lbd/movies.csv', low_memory=False)

ratings2 = pd.merge(ratings, movies, on='movieId', how='left')
ratings2.dropna().drop(columns=['size']).astype(int).to_csv('lbd/rating_resize.csv', index=False)
