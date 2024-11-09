from PyQt6.QtWidgets import QMessageBox

from pathlib import Path
import os, json, pymongo, sys

def connect_to_db(collection_name):
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
        db = client['LPGTrading_DB']  # Replace with your database name
        return db[collection_name]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        QMessageBox.critical(
            None, 
            "Error",
            "Error connecting to MongoDB: " + str(e)
        )
        return None
    
def create_collection(collection_name):
    print(f'Creating collection')
    collection = connect_to_db(collection_name)

    try:
        temp_data = {
            "temp": "temp",
        }
        collection.insert_one(temp_data) # insert data to automatically create collection
        collection.delete_many({}) # delete all the data in the collection
    except Exception as e:
        QMessageBox.warning(
            None,
            "Warning",
            "Error creating collection: " + str(e)
        )
    
def get_json_data():
    # Define the path to the JSON file
    relative_path = Path("setup/collections.json")
    json_directory = Path.cwd() / relative_path

    # Check if the JSON file exists
    try:
        if not json_directory.exists():
            print(f"The file {json_directory} does not exist.")
        else:
            print(f"File path: {json_directory}")
    except Exception as e:
        print(f"Error accessing the file path: {e}")

    # Attempt to read the JSON file
    try:
        with open(json_directory, 'r') as f:
            data = json.load(f)
            print("Data loaded successfully:", data)

        for i, collection_name in enumerate(data['collections']):
            print(f"Collection {i}: {collection_name}")
            if not is_collection_exist(collection_name):
                print(f"Collection {collection_name} doesn't exis")
                create_collection(collection_name)

    except FileNotFoundError:
        print(f"File not found: {json_directory}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def is_collection_exist(collection_name):
    # returns True if collection exists, False otherwise

    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
    db = client['LPGTrading_DB']  # Database name

    if collection_name not in db.list_collection_names():
        print("Collection doesn't exist")
        return False
    else:
        print("Collection already exists")
        return True

def main():
    get_json_data()