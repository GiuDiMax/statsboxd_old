from mongodb import db
from utils.cleanUsers import cleanUsers


def seeUsers():
    #cleanUsers()
    a = db.Users.aggregate([
        {'$project': {'_id': 1, 'name': 1}},
    ])
    i = 0
    for x in a:
        i = i+1
        print(x)
    print('total: ' + str(i))


if __name__ == '__main__':
    seeUsers()

