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
        #if collection_name != 'Users':
        with open(backup_db_dir+'\\'+collection_name+'.json', 'w') as file:
            cursor = collection.find()
            file.write(dumps(cursor))
    shutil.make_archive('backup', 'zip', backup_db_dir)
    shutil.rmtree(backup_db_dir)


if __name__ == '__main__':
    backup_db(db, "backup")
