from PyQt6.QtWidgets import *
from ui.dashboard_page import Ui_Form as Ui_dashboard_page

from utils.DB_checker import db_checker
from utils.Inventory_Monitor import InventoryMonitor

from PyQt6.QtCore import QThread, pyqtSignal
import pymongo

class Dashboard(QWidget, Ui_dashboard_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        # Database connection
        self.collection_name = self.connect_to_db("products_items")

        # Create and start the update thread for total stock
        self.update_thread = UpdateThread(self.collection_name)
        self.update_thread.updated.connect(self.update_total_stock_label)
        self.update_thread.start()
        
        # Set up the layout for the QScrollArea
        cylinderContainerWidget = self.scrollAreaWidgetContents
        self.cylinderContainerLayout = QVBoxLayout(cylinderContainerWidget)
        self.cylinderTypes_scrollArea.setWidget(cylinderContainerWidget)

        self.labels = []

        # Initialize the inventory monitor to listen for changes
        self.products_monitor = InventoryMonitor('products_items')
        self.products_monitor.start_listener_in_background()
        self.products_monitor.data_changed_signal.connect(self.update_cylinder_list)

        # Call the function to update the cylinder list
        self.update_cylinder_list()

    def update_cylinder_list(self):
        processed_data = self.get_quantity_in_stock()
        self.display_cylinder_data(processed_data)

    def display_cylinder_data(self, processed_data):
        # This method will update the scroll area with new data
        # Make sure to reuse existing labels or create new ones as needed
        print(f"Received update signal with {processed_data} items")
        
        # First, clear the existing labels in the scroll area (if needed)
        for label in self.labels:
            self.cylinderContainerLayout.removeWidget(label)
            label.deleteLater()  # Ensure the widgets are deleted properly
        self.labels.clear()  # Clear the list of stored labels

        # Now, create new labels based on the processed data
        for data in processed_data:
            cylinder_size = data['cylinder_size']
            total_quantity = data['total_quantity']

            label = QLabel(f'{cylinder_size}KG - {total_quantity} cylinder in stock')
            label.setMaximumHeight(50)  # Set max height if needed
            self.labels.append(label)  # Store reference to the label
            self.cylinderContainerLayout.addWidget(label)  # Add the label to the layout

    def get_quantity_in_stock(self):
        try:
            # Use aggregation to group by cylinder_size and sum quantity_in_stock
            pipeline = [
                {
                    "$group": {
                        "_id": "$cylinder_size",  # Group by cylinder_size
                        "total_quantity": {"$sum": "$quantity_in_stock"}  # Sum the quantities
                    }
                }
            ]
            # Run the aggregation pipeline on the "products_items" collection
            result = self.connect_to_db("products_items").aggregate(pipeline)

            processed_data = []
            # Process the results
            for item in result:
                cylinder_size = item['_id']
                processed_cylinder_size = cylinder_size.replace('kg', '')
                total_quantity = item['total_quantity']

                processed_data.append({
                    "cylinder_size": processed_cylinder_size,
                    "total_quantity": total_quantity
                })

            processed_data.sort(key=lambda x: int(x['cylinder_size']))

            return processed_data  # Return the result (list) if needed for further processing

        except Exception as e:
            print(f"Error getting quantity in stock: {e}")
            return []

    def update_total_stock_label(self, total_stock=None):
        # display the total on a label
        if total_stock is None:
            total_stock = self.get_total_stock()
        try:
            self.totalItemStock_label.setText(f'{total_stock}')
        except Exception as e:
            print(e)

    def get_total_stock(self):
        try:
            total_stock = self.connect_to_db("products_items").count_documents({})
            print(f'total stock: {total_stock}')
            return total_stock
        except Exception as e:
            print(f"Error getting total stock: {e}")
            return 0

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
# class UpdateAvailableSize(QThread):
#     update_signal = pyqtSignal(list)

#     def __init__(self, collection, dashboard_page):
#         super().__init__()
#         self.collection = collection
#         self.dashboard_page = dashboard_page  # Pass the existing instance of Dashboard
#         self.running = True

#     def run(self):
#         while self.running:
#             try:
#                 # Call get_quantity_in_stock and get the result
#                 cylinder_sizes = self.dashboard_page.get_quantity_in_stock()

#                 # Emit the signal with updated cylinder sizes (or any relevant data)
#                 self.update_signal.emit(cylinder_sizes)  # Emit the list of processed data
#                 self.running = False  # Stop after one run (if you want to update periodically, set this logic accordingly)

#             except Exception as e:
#                 print(f"Error updating cylinder sizes: {e}")

#             QThread.msleep(100)  # Sleep for 100ms

#     def stop(self):
#         self.running = False

class UpdateThread(QThread):
    updated = pyqtSignal(int)

    def __init__(self, collection):
        super().__init__()
        self.collection = collection
        self.running = True

    def run(self):
        while self.running:
            try:
                total_stock = self.collection.count_documents({})
                self.updated.emit(total_stock)
            except Exception as e:
                print(f"Error updating total stock: {e}")
            QThread.msleep(1000)  # Update every second

    def stop(self):
        self.running = False
