from PyQt6.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QApplication, QAbstractItemView
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

# from ui.NEW.orders_page import Ui_orderPage_Form
from ui.final_ui.orders_page import Ui_Form as Ui_orderPage_Form
# from pages.admin.new_order_page import NewOrderPage
from pages.admin.new_order_page import AddOrderForm

from utils.Inventory_Monitor import InventoryMonitor
import pymongo, json, re
from datetime import datetime

class OrderPage(QWidget, Ui_orderPage_Form):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # self.createOrder_pushButton.clicked.connect(lambda: self.createOrder())
        # self.cancelOrder_pushButton.clicked.connect(lambda: print('cancel order button clicked'))
        # self.editOrder_pushButton.clicked.connect(lambda: print('edit order button clicked'))
        # self.orderHistory_pushButton.clicked.connect(lambda: print('order history button clicked'))

        # if not hasattr(self, 'createOrderBtn_connected'):
        #     self.creae.clicked.connect(lambda: self.createOrder())
        #     self.createOrderBtn_connected = True

        # self.run_monitor(self.update_table)
        # self.update_table()

        self.update_total_orders()

    def get_total_orders_today(self):
        """
        Retrieves the total number of orders created today from the MongoDB database.
        """
        try:
            # Get today's date in string format: "YYYY-MM-DD"
            today_date = datetime.now().strftime("%Y-%m-%d")

            # Query to find orders where order_date equals today's date
            query = {
                "order_date": today_date
            }

            # Get the total count of orders
            total_orders = self.connect_to_db("orders").count_documents(query)
            return total_orders

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def update_total_orders(self):
        """Update total orders label"""
        total_orders_today = self.get_total_orders_today()
        self.total_orders_label.setText(str(total_orders_today))

    def run_monitor(self, object_to_update):
        # Initialize Inventory Monitor
        self.order_monitor = InventoryMonitor('orders')
        self.order_monitor.start_listener_in_background()
        self.order_monitor.data_changed_signal.connect(object_to_update)
  

    def createOrder(self):
        print(f'Create order button clicked')
        # self.new_order_page = NewOrderPage()
        # self.new_order_page.show(
        self.new_order_page = AddOrderForm(None)
        self.new_order_page.show()

    def update_table(self):
            table = self.orders_tableWidget
            table.setRowCount(0)  # Clear the table

            header_dir = "app/resources/config/table/order_tableHeader.json"

            # Read header labels from the JSON file
            with open(header_dir, 'r') as f:
                header_labels = json.load(f)

            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            # Clean the header labels
            self.header_labels = [self.clean_header(header) for header in header_labels]

            # filter_query = {}
            # order_filter = self.orderStatus.currentText()
            # paymentStatus_filter = self.paymentStatus.currentText()

            # if order_filter != "Show All":
            #     filter_query['order_status'] = order_filter

            # if paymentStatus_filter != "Show All":
            #     filter_query['payment_status'] = paymentStatus_filter

            data = list(self.connect_to_db("orders").find().sort("_id", -1))
            # data = list(self.collection.find(filter_query).sort("_id", -1))
            if not data:
                return  # Exit if the collection is empty

            # Populate table with data
            for row, item in enumerate(data):
                table.setRowCount(row + 1)
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)
                    if value is not None:
                        table.setItem(row, column, QTableWidgetItem(str(value)))

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    
    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]