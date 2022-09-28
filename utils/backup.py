from os.path import join
from bson.json_util import dumps
from mongodb import db
import shutil
import os


def backup_db(db, backup_db_dir):
    try:
        shutil.rmtree(backup_db_dir)
        os.remove('backup.zip')
    except:
        pass
    collections = db.list_collection_names()
    os.mkdir(backup_db_dir)
    for i, collection_name in enumerate(collections):
        collection = db[collection_name]
        cursor = collection.find({})
        with open(backup_db_dir+'\\'+collection_name+'.json', 'w') as file:
            file.write('[')
            for document in cursor:
                file.write(dumps(document))
                file.write(',')
            file.write(']')
    shutil.make_archive('backup', 'zip', backup_db_dir)
    shutil.rmtree(backup_db_dir)


if __name__ == '__main__':
    backup_db(db, "backup")
