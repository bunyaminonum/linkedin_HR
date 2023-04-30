import pymongo
from pymongo import MongoClient

class MDB:
    def __init__(self):
        try:
            self.cluster = MongoClient('mongodb+srv://bentego:CLdCM3U86DOJ56KC@linkedincluster0.wewjcl7.mongodb.net/?retryWrites=true&w=majority')
            self.db = self.cluster['linkedinCluster0']
            self.collection = self.db['info']
            print("db connection successful")
        except Exception as e:
            print("Could not connected mongoDB", e)


        # self.collection.drop()
        # self.db.create_collection('info')
        try:
            self.linklistFromDB = []
            data = self.collection.find({})
            for i in data:
                self.linklistFromDB.append(i['_id'])
            # print(self.linklistFromDB)
        except:
            self.linklistFromDB = []
# m = MDB()