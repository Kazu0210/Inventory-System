import threading
import pymongo
from PyQt6.QtCore import pyqtSignal, QObject

class InventoryMonitor(QObject):
    # Signals
    data_changed_signal = pyqtSignal(bool)

    def __init__(self, collection_name):
        super().__init__()
        # Initialize MongoDB connection
        self.collection = self.connect_to_db(collection_name)
        self._stop_event = threading.Event()  # Stop event for controlled thread termination

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db_name = "LPGTrading_DB"
        return client[db_name][collection_name]
    
    def start_change_stream(self):
        # Listens for changes and checks stop signal
        print("Starting change stream listener.")
        
        try:
            with self.collection.watch() as stream:
                for change in stream:
                    if self._stop_event.is_set():  # Check if stop signal is set
                        print("Change stream listener stopped.")
                        break
                    print(f"Change detected: {change}")
                    self.data_changed_signal.emit(True)
        except pymongo.errors.PyMongoError as e:
            print(f"Error in change stream: {e}")

    def start_listener_in_background(self):
        # Starts the change stream listener in a background thread
        self.listener_thread = threading.Thread(target=self.start_change_stream, daemon=True)
        self.listener_thread.start()

    def stop_listener_in_background(self):
        # Stops the change stream listener in the background thread
        if hasattr(self, 'listener_thread') and self.listener_thread.is_alive():
            print("Stopping change stream listener.")
            self._stop_event.set()  # Signal to stop the thread
            self.listener_thread.join()  # Wait for thread to terminate
            print("Listener thread stopped.")
            self._stop_event.clear()  # Reset the stop event for future use

# Example usage
# monitor = InventoryMonitor('logs')
# monitor.start_listener_in_background()