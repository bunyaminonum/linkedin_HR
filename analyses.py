import connect_database
from connect_database import MDB

# db = MDB()
# loc = db.collection.find({})
# for i in loc:
#     print(str(i['location']).split(','))

class Analyses:
    def __init__(self):
        self.db = MDB()
        self.info = self.db.collection.find({})
        self.locList = []
        self.loclist2 = []
        for i in self.info:
            list = str(i['location']).split(',')
            if 'Ankara' in list:
                print(i)


a = Analyses()
