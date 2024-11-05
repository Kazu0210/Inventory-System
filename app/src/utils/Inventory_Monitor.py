import threading
import pymongo

class InventoryMonitor:
    def __init__(self, collection_name):
        # Initialize MongoDB connection
        self.collection = self.connect_to_db(collection_name)

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db_name = "LPGTrading_DB"
        return client[db_name][collection_name]
    
    def start_change_stream(self):
        # Listens for changes in a separate thread
        print("Starting change stream listener.")
        
        with self.collection.watch() as stream:
            for change in stream:
                print(f"Change detected: {change}")
                # Call a method here if you want to process each change further
                # For example: self.handle_change(change)

    def start_listener_in_background(self):
        # Corrected typo in variable name
        listener_thread = threading.Thread(target=self.start_change_stream, daemon=True)
        listener_thread.start()

monitor = InventoryMonitor('accounts')
monitor.start_listener_in_background()