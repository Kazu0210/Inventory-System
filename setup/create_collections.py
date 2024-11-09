from PyQt6.QtWidgets import QMessageBox

from pathlib import Path
import os, json, pymongo, sys

def connect_to_db(collection_name):
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
        db = client['your_database_name']  # Replace with your database name
        return db[collection_name]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        QMessageBox.critical(
            None, 
            "Error",
            "Error connecting to MongoDB: " + str(e)
        )
        return None
    
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
    except FileNotFoundError:
        print(f"File not found: {json_directory}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

get_json_data()