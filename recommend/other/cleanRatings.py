import pandas as pd


def cleanRatings(df, single=False):
    df[['userId']] = df[['userId']].apply(pd.to_numeric, errors='coerce')
    df[['movieId']] = df[['movieId']].apply(pd.to_numeric, errors='coerce')
    df[['rating']] = df[['rating']].apply(pd.to_numeric, errors='coerce')
    df = df.dropna().astype(int).drop_duplicates()
    movies = pd.read_csv('movies.csv', low_memory=False)
    df = pd.merge(df, movies, on='movieId', how='right')
    df = df.drop(columns=['uri']).dropna().sort_values(by=['userId'])
    '''
    df['rating'] = df['rating'] - df['average']/5
    df['rating'] = df['rating'].round(1)
    '''
    return df


if __name__ == '__main__':
    dfx = pd.read_csv('ratings.csv', low_memory=False, encoding_errors='ignore')
    cleanRatings(dfx).to_csv('ratings_clean.csv', index=False)
