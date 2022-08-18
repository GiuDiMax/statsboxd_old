from mongodb import db


def clean():
    db.Film.update_many({}, {'$unset': {'genres.themes': 1, 'genres.mini-themes': 1}})


if __name__ == '__main__':
    clean()
