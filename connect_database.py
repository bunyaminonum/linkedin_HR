import pymongo
from pymongo import MongoClient


class MDB:
    def __init__(self):
        try:
            self.cluster = MongoClient('mongodb://bentegoHR:EBmoZxlm22oy5Trl@ac-fcb4edc-shard-00-00.yl8zrbx.mongodb.net:27017,ac-fcb4edc-shard-00-01.yl8zrbx.mongodb.net:27017,ac-fcb4edc-shard-00-02.yl8zrbx.mongodb.net:27017/?ssl=true&replicaSet=atlas-f6fz0k-shard-0&authSource=admin&retryWrites=true&w=majority')
            self.db = self.cluster['profileDB']
            self.collection = self.db['info']
            # self.collection.drop()
            # self.db.create_collection('info')

            # data = self.db.find({})
            # for i in data:
            #     print(i)
        except:
            print("Could not connected mongoDB")

# db = MDB()