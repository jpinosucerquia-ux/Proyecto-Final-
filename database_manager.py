#me falta por hacer jajaj

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
    
    
class DatabaseManager:
     def __init__(self, uri="mongodb://localhost:27017/", db_name="mydatabase"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            print("Connected to MongoDB successfully!")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}") 
     def insert_metadata(self, collection_name, metadata):
        collection = self.db[collection_name]
        result = collection.insert_one(metadata)
        return result.inserted_id
        def get_metadata(self, collection_name, query):
                collection = self.db[collection_name]
                result = collection.find_one(query)
                return result   
    