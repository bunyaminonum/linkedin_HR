import pymongo
from pymongo import MongoClient


class MDB:
    def __init__(self):
        try:
            self.cluster = MongoClient('mongodb+srv://bentego:SbfLNqFrLveYojuP@linkedincluster0.wewjcl7.mongodb.net/?retryWrites=true&w=majority')
            self.db = self.cluster['linkedinCluster0']
            self.collection = self.db['info']
        except:
            print("Could not connected mongoDB")


        # self.collection.drop()
        # self.db.create_collection('info')
        try:
            self.linklistFromDB = []
            data = self.collection.find({})
            for i in data:
                self.linklistFromDB.append(i['_id'])
            print(self.linklistFromDB)
        except:
            print('error!')

