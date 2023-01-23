import connect_database
from connect_database import MDB
from getProfileLinks import GetProfileLinks as gpl

class Filter:
    def __init__(self):
        self.db = MDB()

    def Byloc(self, location):
        location = str(location).lower()
        locationInDB = self.db.collection.find({})
        for loc in locationInDB:
            editedLoc = str(loc['location']).lower().replace(',', '').strip().split()
            if location in editedLoc:
                print(loc)


    def ByFollowerSize(self, min_size, maxs_ize):
        followers = self.db.collection.find({})
        for follower in followers:
            followSize = follower['num_connection']
            if followSize >= min_size and followSize <= maxs_ize:
                print(follower)

    def ByWorksAt(self, works_at):
        works_at = str(works_at).lower()
        works_at_ = self.db.collection.find({})
        for wa in works_at_:
            worksAt_ = str(wa['works at']).lower()
            if works_at in worksAt_:
                print(wa)


filter = Filter()
filter.ByWorksAt('software')
