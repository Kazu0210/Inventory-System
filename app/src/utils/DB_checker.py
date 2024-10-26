import pymongo
import sys

import pymongo.errors

class db_checker:
    def __init__(self, connection_string, db_name):
        self.connectionString = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect_to_client(self):
        try:
            self.client = pymongo.MongoClient(self.connectionString)
            print("Connected to MongoDB client")
        except pymongo.errors.ConnectionFailure as e:
            print("Error connecting to MongoDB client:", e)
            sys.exit(1)

    def connect_to_db(self):
        if self.client is not None:
            self.db = self.client[self.db_name]
            print(f"Connected to database: {self.db_name}")
        else:
            print("Error: Client is not connected")

    def check_db_exist(self):
        if self.client is not None:
            if self.db_name in self.client.list_database_names():
                print(f"Database {self.db_name} exists")
                return True
            else:
                print("Database does not exist")
                # create database
                self.create_db()
        else:
            print("Error: Client is not connected")

    def create_db(self):
        if self.client is not None:
            print(f"Creating Database: {self.db_name}")
            self.db = self.client[self.db_name]
            print(f"Database {self.db_name} created")  

            collection = self.db['temp']
            collection.insert_one({"data": ""})
        else:
            print("Error: Client is not connected")

    def create_collection(self, collection_name):
        if self.db is not None:
            if collection_name in self.db.list_collection_names():
                print(f"Collection {collection_name} already exists")
            else:
                print(f"Creating Collection: {collection_name}")
                self.db.create_collection(collection_name)
                print(f"Collection {collection_name} created")
        else:
            print("Error: Database is not connected")

    def check_collection_exist(self, collection_name):
        if self.db is not None:
            if collection_name in self.db.list_collection_names():
                print(f"Collection {collection_name} exists")
                return True
            else:
                print(f"Collection {collection_name} does not exist")
                return False
        else:
            print("Error: Database is not connected")

    def insert_document(self, collection_name, document):
        if self.db is not None:
            if collection_name in self.db.list_collection_names():
                collection = self.db[collection_name]
                try:
                    result = collection.insert_one(document)
                    print(f"Document inserted into {collection_name} with ID: {result.inserted_id}")
                except pymongo.errors.WriteError as e:
                    print(f"Error inserting document into {collection_name}: {e}")
            else:
                print(f"Collection {collection_name} does not exist")
        else:
            print("Error: Database is not connected")

    def find_documents(self, collection_name, filter):
        if self.db is not None:
            if collection_name in self.db.list_collection_names():
                collection = self.db[collection_name]
                try:
                    results = collection.find(filter)
                    for doc in results:
                        print(f"Found document: {doc}")
                except pymongo.errors.OperationFailure as e:
                    print(f"Error finding documents in {collection_name}: {e}")
            else:
                print(f"Collection {collection_name} does not exist")
        else:
            print("Error: Database is not connected")
# sample use
# db_name = "testingDB"
# checker = db_checker("mongodb://localhost:27017/", db_name)
# checker.connect_to_client()
# checker.connect_to_db()
# checker.check_db_exist()
# checker.create_collection("my_collection")
# checker.check_collection_exist("my_collection")
# checker.check_collection_exist("non_existent_collection")

# checker.find_documents("my_collection", {"age": {"$gt": 30}})