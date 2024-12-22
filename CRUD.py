from pymongo import MongoClient
import json

class AnimalShelter(object):

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        self.client = MongoClient('mongodb://%s:%s@localhost:37348' % (username, password))
        self.database = self.client['AAC']

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            self.database.animals.insert(data) # data should be dict.
            return True
            
        else:
            raise Exception("Nothing to save, because data parameter is empty")
            return False

    # Create method to implement the R in CRUD
    def read(self, id_number):
        if id_number is not None:
            data = self.database.animals.find(id_number)
            for r in data:
                print(r)

        else:
            raise Exception("Nothing to read, id parameter is empty")
    
    def update(self, old_Data, new_Data):
        if old_Data is not None and new_Data is not None:
            updated = self.database.animals.update_many(old_Data,{'$set':new_Data})
            print(updated.modified_count, " documents updated.")
        
        else:
            raise Exception("Enter values to modify both the key and the value from the collection")
        
    def delete(self, animal):
        if animal is not None:
            data = self.read(animal)
            if data is None:
                print("This entry does not exist")
            deleted = self.database.animals.delete_many(animal)
            print(deleted.deleted_count, " documents deleted")
            
        else:
            raise Exception("The data for this entry does not exist")
