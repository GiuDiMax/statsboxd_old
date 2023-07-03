from mongodb import db


def allowed(username):
    obj = list(db.Allowed.find({'_id': 1}))[0]['allowed']
    if username in obj:
        return True
    return False


def getLista():
    obj = list(db.Allowed.find({'_id': 1}))[0]['allowed']
    obj.sort()
    with open('lista.txt', 'w') as f:
        for line in obj:
            f.write(line)
            f.write('\n')
            print(line)


def addAllowed(username):
    obj = list(db.Allowed.find({'_id': 1}))[0]['allowed']
    if username not in obj:
        db.Allowed.update_one({'_id': 1}, {'$push': {'allowed': username}})


def addLista():
    lista = []
    with open('lista.txt') as f:
        lines = f.readlines()
    for l in lines:
        lista.append(l.replace("\n", ""))
    db.Allowed.insert_one({'_id': 1, 'allowed': lista})


if __name__ == '__main__':
    addAllowed('giudimax')
