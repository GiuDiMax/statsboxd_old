from mongodb import db


def seeUsers():
    a = db.Users.aggregate([
        {'$project': {'_id': 1, 'name': 1, 'years': 1}},
    ])
    i = 0
    j = 0
    for x in a:
        i = i+1
        if 'years' in x:
            j = j+1
        print(x)
    print('total: ' + str(i))
    print('total with stats: ' + str(j))


if __name__ == '__main__':
    seeUsers()

