import threading
import pymongo
from PyQt6.QtCore import pyqtSignal, QObject

class InventoryMonitor(QObject):  # Inherit from QObject
    # signals
    data_changed_signal = pyqtSignal(bool)

    def __init__(self, collection_name):
        super().__init__()  # Call the constructor of QObject
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
                # Emit the signal when a change is detected
                self.data_changed_signal.emit(True)

    def start_listener_in_background(self):
        # Starts the change stream listener in a background thread
        listener_thread = threading.Thread(target=self.start_change_stream, daemon=True)
        listener_thread.start()

# Example usage
# monitor = InventoryMonitor('accounts')
# monitor.start_listener_in_background()
