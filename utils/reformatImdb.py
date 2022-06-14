import pandas as pd
from mongodb import db

def reformat_imdb(username):
    watched = db.Users.find_one({"_id": username.lower()})

    watched = db.Users.aggregate([
        {'$match': {'_id': username.lower()}},
        {'$unwind': '$watched'},
        {'$match': {'watched.rating': {'$gt': 0}}},
        {'$project': {'_id': '$watched.id', 'rating': '$watched.rating'}},
        {'$lookup': {
            'from': 'Film',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'info'}},
        {'$unwind': '$info'},
        {'$project': {'_id': '$info.imdb', 'rating': '$rating'}}
    ])

    for watch in watched:
        watched = watched
        break

    df = pd.DataFrame(columns=['Const', 'Your Rating', 'Date Rated', 'Title', 'URL', 'Title Type',
                               'IMDb Rating', 'Runtime (mins)', 'Year', 'Genres', 'Num Votes',
                               'Release Date', 'Directors'])
    for watch in watched:
        df.loc[len(df.index)] = ['tt'+str(watch['_id']).zfill(7), watch['rating'], '2019-01-01', 'Title',
                                 'https://www.imdb.com/title/'+'tt'+str(watch['_id']).zfill(7)+'/', 'movie', 6.0,
                                 '120', '2019', 'Comedy, Drama', '9999', '2019-01-01', 'Director']

    df.to_csv(r'ratings.csv', index=False, header=True, line_terminator='\n')
    print("File saved")

reformat_imdb('giudimax')