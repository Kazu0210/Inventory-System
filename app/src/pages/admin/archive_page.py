from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from datetime import datetime
import json, os, pymongo, re

from ui.NEW.archive_page import Ui_Form as Ui_archive
from utils.Inventory_Monitor import InventoryMonitor

class ArchivePage(QWidget, Ui_archive):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # set currennt collection 
        self.current_collection = None

        # Connect button
        self.accounts_pushButton.clicked.connect(lambda: self.setActiveCollection('account_archive'))
        self.products_pushButton.clicked.connect(lambda: self.setActiveCollection('product_archive'))
        self.orders_pushButton.clicked.connect(lambda: self.setActiveCollection('order_archive'))
        
        # Initialize monitor for each collection
        self.accounts_monitor = InventoryMonitor('account_archive')
        self.products_monitor = InventoryMonitor('product_archive')
        self.orders_monitor = InventoryMonitor('order_archive')

        # Start monitoring
        self.accounts_monitor.start_listener_in_background()
        self.products_monitor.start_listener_in_background()
        self.orders_monitor.start_listener_in_background()

        # Connect each monitor’s data_changed_signal to the handle_signal method
        self.accounts_monitor.data_changed_signal.connect(lambda: self.handle_signal("account_archive"))
        self.orders_monitor.data_changed_signal.connect(lambda: self.handle_signal("order_archive"))
        self.products_monitor.data_changed_signal.connect(lambda: self.handle_signal("product_archive"))

        # MongoDB connection
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.db_client["LPGTrading_DB"]

        # For table
        self.tableWidget.itemSelectionChanged.connect(self.on_row_clicked)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

    def on_item_clicked(self, item):
        row = self.tableWidget.row(item)
        self.tableWidget.selectRow(row)

    def on_row_clicked(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()

    def handle_signal(self, collection_name):
        # Called when a change in any monitored collection is detected.
        if self.current_collection == collection_name:
            print(f'Data changed in active collection: {collection_name}, reloading table.')
            self.loadTable(collection_name)
        else:
            print(f"Data changed in {collection_name}, but it's not currently displayed.")

    def setActiveCollection(self, collection_name):
        # Sets the current collection and loads its data into the table.
        self.current_collection = collection_name
        print(f'Current Active Collection: {self.current_collection}')
        self.loadTable(collection_name)

    def clean_key(self, key):
        """Clean headers and keys by removing special characters and spaces."""
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def loadTable(self, collection_name):
        if collection_name == "account_archive":
            print("Loading accounts archive table.")
            self.loadAccounts()
        elif collection_name == "product_archive":
            self.loadProducts()

    def loadProducts(self):
            table = self.tableWidget
            table.setRowCount(0)  # Clear the table
            table.verticalHeader().hide()

            # Load table headers from JSON
            header_dir = "app/resources/config/table/product_tableHeader.json"
            with open(header_dir, 'r') as f:
                header_labels = json.load(f)
            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            for column in range(table.columnCount()):
                table.setColumnWidth(column, 200)

            # Clean headers for use as dictionary keys
            self.header_labels = [self.clean_key(header) for header in header_labels]

            # Load and parse settings
            settings_dir = "app/resources/config/settings.json"
            with open(settings_dir, 'r') as f:
                settings = json.load(f)
            self.current_time_format = settings['time_date'][0]['time_format']

            # Get data from MongoDB with error handling
            try:
                data = list(self.db["account_archive"].find().sort("_id", -1))
            except pymongo.errors.PyMongoError as e:
                print(f"Error accessing MongoDB: {e}")
                return

            if not data:
                return  # Exit if the collection is empty
            
            # Populate table with data
            for row, item in enumerate(data):
                table.setRowCount(row + 1)  # Add a new row for each item
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)
                    if value is not None:
                        # Format datetime if necessary
                        if header == 'lastlogin' and value:
                            try:
                                date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                                value = date_time.strftime(
                                    "%Y-%m-%d %I:%M:%S %p" if self.current_time_format == "12hr" else "%Y-%m-%d %H:%M:%S"
                                )
                            except Exception as e:
                                pass
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        if row % 2 == 0:
                            table_item.setBackground(QBrush(QColor("#F6F6F6")))
                        table.setItem(row, column, table_item)

    def loadAccounts(self):
            table = self.tableWidget
            table.setRowCount(0)  # Clear the table
            table.verticalHeader().hide()

            # Load table headers from JSON
            header_dir = "app/resources/config/table/accounts_tableHeader.json"
            with open(header_dir, 'r') as f:
                header_labels = json.load(f)
            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            for column in range(table.columnCount()):
                table.setColumnWidth(column, 200)

            # Clean headers for use as dictionary keys
            self.header_labels = [self.clean_key(header) for header in header_labels]

            # Load and parse settings
            settings_dir = "app/resources/config/settings.json"
            with open(settings_dir, 'r') as f:
                settings = json.load(f)
            self.current_time_format = settings['time_date'][0]['time_format']

            # Get data from MongoDB with error handling
            try:
                data = list(self.db["account_archive"].find().sort("_id", -1))
            except pymongo.errors.PyMongoError as e:
                print(f"Error accessing MongoDB: {e}")
                return

            if not data:
                return  # Exit if the collection is empty
            
            # Populate table with data
            for row, item in enumerate(data):
                table.setRowCount(row + 1)  # Add a new row for each item
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)
                    if value is not None:
                        # Format datetime if necessary
                        if header == 'lastlogin' and value:
                            try:
                                date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                                value = date_time.strftime(
                                    "%Y-%m-%d %I:%M:%S %p" if self.current_time_format == "12hr" else "%Y-%m-%d %H:%M:%S"
                                )
                            except Exception as e:
                                pass
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        if row % 2 == 0:
                            table_item.setBackground(QBrush(QColor("#F6F6F6")))
                        table.setItem(row, column, table_item)