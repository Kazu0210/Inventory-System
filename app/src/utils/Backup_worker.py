from PyQt6.QtCore import QObject
import json, pymongo

class BackupWorker(QObject):
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path  # Path to the JSON file for backup

    def restoreDB(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            # Get the keys that hold arrays
            keys_with_array = self.get_keys_with_arrays(data)

            # Iterate over each key that holds an array of documents
            for key in keys_with_array:
                # Print the key for debugging purposes
                print(f'Inserting data for key: {key}')

                # Retrieve the array of documents (e.g., accounts, logs) from data[key]
                documents = data[key]

                # Insert data into MongoDB collection associated with the key
                if isinstance(documents, list):
                    # Insert multiple documents at once for arrays of documents
                    self.connect_to_db(key).insert_many(documents)
                else:
                    # Insert a single document if it’s not an array (unlikely in this structure but added for completeness)
                    self.connect_to_db(key).insert_one(documents)
        except Exception as e:
            print(f"Error restoring DB: {e}")
        # finally:
        #     self.finished_signal.emit()

    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = collectionN
        return client[db][collection_name]
    
    def get_keys_with_arrays(self, data):
        # get keys with arrays (lists) as values
        keys_with_arrays = []

        if isinstance(data, dict):  # If the data is a dictionary, iterate through its keys
            for key, value in data.items():
                if isinstance(value, list):  # Check if the value is a list (array)
                    keys_with_arrays.append(key)
                elif isinstance(value, dict):  # If the value is a dictionary, recurse into it
                    keys_with_arrays.extend(self.get_keys_with_arrays(value))
        elif isinstance(data, list):  # If the data is a list, we can directly check each element
            for item in data:
                if isinstance(item, dict):
                    keys_with_arrays.extend(self.get_keys_with_arrays(item))
        
        return keys_with_arrays