import pandas as pd


def cleanRatings(df, single=False):
    df[['userId']] = df[['userId']].apply(pd.to_numeric, errors='coerce')
    df[['movieId']] = df[['movieId']].apply(pd.to_numeric, errors='coerce')
    df[['rating']] = df[['rating']].apply(pd.to_numeric, errors='coerce')
    df = df.dropna().astype(int)
    '''
    movies = pd.read_csv('lbd/movies.csv', low_memory=False, error_bad_lines=False)
    df = pd.merge(df, movies, on='movieId', how='right')
    df['rating'] = df['rating'] - df['average']/5
    df = df.drop(columns=['uri', 'average']).dropna()
    df['rating'] = df['rating'].round(1)
    '''
    return df


if __name__ == '__main__':
    dfx = pd.read_csv('lbd/ratings.csv', low_memory=False, error_bad_lines=False)
    cleanRatings(dfx).to_csv('lbd/ratings_clean.csv', index=False)
    #cleanRatings('lbd/userSet.csv')

