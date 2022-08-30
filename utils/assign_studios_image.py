from mongodb import db
import glob
import os

my_path = os.path.abspath(os.path.dirname(__file__)).rsplit("\\", 1)[0]
files = glob.glob(my_path+"/static/images/studios/*.*")
for file in files:
    filename = file.rsplit("\\", 1)[1]
    name = filename.rsplit(".", 1)[0]
    db.People.update_one({'_id': name}, {'$set': {'img': filename}})