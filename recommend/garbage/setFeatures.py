from mongodb import db
import csv

def main():
    with open('../lbd/movies.csv', newline='') as csvfile:
        movies = csv.reader(csvfile, delimiter=',')
        ids = []
        for x in movies:
            try:
                ids.append(int(x[0]))
            except:
                pass
    obj = db.Film.aggregate([
        {'$match': {"_id": {'$in': ids}}},
        {'$project': {'_id': 1, 'uri': 1, 'year': 1, 'genre': '$genres.main',
                      'theme': '$genres.themes', 'mini': '$genres.mini-themes', 'director': '$crew.director',
                      'country': '$country'}}
        ])
    f = open('lbd/movies_full.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['movieId', 'uri', 'year', 'country', 'director', 'genre', 'theme', 'mini'])
    for x in obj:
        if 'director' in x and len(x['director']) > 0:
            director = x['director'][0]
        else:
            director = ''
        if 'genre' in x and len(x['genre']) > 0:
            genre = x['genre'][0]
        else:
            genre = ''
        if 'theme' in x and len(x['theme']) > 0:
            theme = x['theme'][0]
        else:
            theme = ''
        if 'mini' in x and len(x['mini']) > 0:
            mini = x['mini'][0]
        else:
            mini = ''
        if 'country' in x and len(x['country']) > 0:
            country = x['country'][0]
        else:
            country = ''
        writer.writerow([x['_id'], x['uri'], x['year'], country, director, genre, theme, mini])


if __name__ == '__main__':
    main()
