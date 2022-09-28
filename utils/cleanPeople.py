from mongodb import db


def cleanPeople():
    x = db.People.find({'imgNone': True})
    y = 0
    for a in x:
        y = y+1
    print(y)
    db.People.delete_many({'imgNone': True})


if __name__ == '__main__':
    cleanPeople()
