from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from datetime import datetime
import json, os, pymongo, re, threading

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
        # self.orders_pushButton.clicked.connect(lambda: self.setActiveCollection('order_archive'))
        
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

        if selected_rows:

            row_index = selected_rows[0].row()
            print(f"Row {row_index} clicked")

        row_data = []
        for column in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row_index, column)
            if item is not None:
                row_data.append(item.text())
            else:
                row_data.append("")

        product_header_dir = "app/resources/config/table/items_tableHeader.json"

        with open(product_header_dir, 'r') as f:
            data = json.load(f)
            print(f'Data from items page (Table header): {data}')

        try:
            if 'Product ID' in data:
                productID_header_index = data.index('Product ID')
                print(f'Product id header index {productID_header_index}')
            else:
                print("Column doesn't exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

        document = self.connect_to_db("products_items").find_one({'product_id': row_data[productID_header_index]})

        # try:
        #     self.productID = document['product_id']
        #     self.productName = document['product_name']
        #     self.cylinderSize = document['cylinder_size']
        #     self.quantity = document['quantity_in_stock']
        #     self.price = document['price_per_unit']
        #     self.supplier = document['supplier']
        #     self.restockDate = document['last_restocked_date']
        #     self.description = document['description']
        #     self.totalValue = document['total_value']
        #     self.status = document['inventory_status']
        #     self.stock_level = document['stock_level']
        #     self.low_stock_threshold = document['minimum_stock_level']
        # except Exception as e:
        #     print(f"Error: {e}")

        # self.selected_row = row_index

    def handle_signal(self, collection_name):
        # Called when a change in any monitored collection is detected.
        if self.current_collection == collection_name:
            print(f'Data changed in active collection: {collection_name}, reloading table.')
            # self.loadTable(collection_name)
            load_table_thread = threading.Thread(target=self.loadTable(collection_name), daemon=True)
            load_table_thread.start()
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
    
    def clean_header(self, header):
            return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    
    def loadTable(self, collection_name):
        if collection_name == "account_archive":
            self.loadAccounts()
        elif collection_name == "product_archive":
            self.loadProducts()

    def loadProducts(self, page=0, rows_per_page=10):
            self.current_page = page  # Keep track of the current page
            self.rows_per_page = rows_per_page  # Number of rows per page

            table = self.tableWidget
            table.setSortingEnabled(True)
            vertical_header = table.verticalHeader()
            vertical_header.hide()
            table.setRowCount(0)  # Clear the table

            table.setStyleSheet("""
            QTableWidget{
            border-radius: 5px;
            background-color: #fff;
            color: #000;
            }
            QHeaderView:Section{
            background-color: #228B22;
            color: #fff;               
            font: bold 12pt "Noto Sans";
            }
            QTableWidget::item {
                border: none;  /* Remove border from each item */
                padding: 5px;  /* Optional: Adjust padding to make the items look nicer */
            }
                QScrollBar:vertical {
                    border: none;
                    background: #0C959B;
                    width: 13px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical {
                    background: #002E2C;
                    border-radius: 7px;
                    min-height: 30px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: #0C959B;
                }
                QScrollBar:horizontal {
                    border: none;
                    background: #f0f0f0;
                    height: 14px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:horizontal {
                    background: #555;
                    border-radius: 7px;
                    min-width: 30px;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                    background: none;
                }
                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                    background: #f0f0f0;
                }
            """)

            # Header JSON directory
            header_dir = "app/resources/config/table/product_tableHeader.json"

            # Settings directory
            settings_dir = "app/resources/config/settings.json"

            with open(header_dir, 'r') as f:
                header_labels = json.load(f)

            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            header = self.tableWidget.horizontalHeader()
            header.setSectionsMovable(True)
            header.setDragEnabled(True)

            for column in range(table.columnCount()):
                table.setColumnWidth(column, 145)

            # Set uniform row height for all rows
            table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

            header.setFixedHeight(50)

            table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

            # Clean the header labels
            self.header_labels = [self.clean_header(header) for header in header_labels]
            
            # query filter
            filter = {}

            # if self.search_lineEdit.text().strip():  # Check if the input is not empty and strip any whitespace
            #     filter = {
            #         "sale_id": {"$regex": self.search_lineEdit.text(), "$options": "i"}  # Case-insensitive match
            #     }

            # Get data from MongoDB
            data = list(self.connect_to_db('product_archive').find(filter).sort("_id", -1))
            if not data:
                return  # Exit if the collection is empty

            with open(settings_dir, 'r') as f:
                settings = json.load(f)
                self.current_time_format = settings['time_date'][0]['time_format']

            # Pagination logic
            start_row = page * rows_per_page
            end_row = start_row + rows_per_page
            paginated_data = data[start_row:end_row]

            # Populate table with paginated data
            for row, item in enumerate(paginated_data):
                table.setRowCount(row + 1)  # Add a new row for each item
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)

                    if value is not None:
                        
                        if header == 'priceperunit' or header == 'totalvalue':
                            print(f'Price per unit sa archive: {value}')
                            price = f"₱ {value:,.2f}"
                            value = price

                        # Add the value to the table as a QTableWidgetItem
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text

                        # Check if row index is even for alternating row colors
                        if row % 2 == 0:
                            table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                        
                        table.setItem(row, column, table_item)

    def loadAccounts(self, page=0, rows_per_page=10):
            self.current_page = page  # Keep track of the current page
            self.rows_per_page = rows_per_page  # Number of rows per page

            table = self.tableWidget
            table.setSortingEnabled(True)
            vertical_header = table.verticalHeader()
            vertical_header.hide()
            table.setRowCount(0)  # Clear the table

            table.setStyleSheet("""
            QTableWidget{
            border-radius: 5px;
            background-color: #fff;
            color: #000;
            }
            QHeaderView:Section{
            background-color: #228B22;
            color: #fff;               
            font: bold 12pt "Noto Sans";
            }
            QTableWidget::item {
                border: none;  /* Remove border from each item */
                padding: 5px;  /* Optional: Adjust padding to make the items look nicer */
            }
                QScrollBar:vertical {
                    border: none;
                    background: #0C959B;
                    width: 13px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical {
                    background: #002E2C;
                    border-radius: 7px;
                    min-height: 30px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: #0C959B;
                }
                QScrollBar:horizontal {
                    border: none;
                    background: #f0f0f0;
                    height: 14px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:horizontal {
                    background: #555;
                    border-radius: 7px;
                    min-width: 30px;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                    background: none;
                }
                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                    background: #f0f0f0;
                }
            """)

            # Header JSON directory
            header_dir = "app/resources/config/table/accounts_tableHeader.json"

            # Settings directory
            settings_dir = "app/resources/config/settings.json"

            with open(header_dir, 'r') as f:
                header_labels = json.load(f)

            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            header = self.tableWidget.horizontalHeader()
            header.setSectionsMovable(True)
            header.setDragEnabled(True)

            for column in range(table.columnCount()):
                table.setColumnWidth(column, 145)

            # Set uniform row height for all rows
            table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

            header.setFixedHeight(50)

            table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

            # Clean the header labels
            self.header_labels = [self.clean_header(header) for header in header_labels]
            
            # query filter
            filter = {}

            # if self.search_lineEdit.text().strip():  # Check if the input is not empty and strip any whitespace
            #     filter = {
            #         "sale_id": {"$regex": self.search_lineEdit.text(), "$options": "i"}  # Case-insensitive match
            #     }

            # Get data from MongoDB
            data = list(self.connect_to_db('account_archive').find(filter).sort("_id", -1))
            if not data:
                return  # Exit if the collection is empty

            with open(settings_dir, 'r') as f:
                settings = json.load(f)
                self.current_time_format = settings['time_date'][0]['time_format']

            # Pagination logic
            start_row = page * rows_per_page
            end_row = start_row + rows_per_page
            paginated_data = data[start_row:end_row]

            # Populate table with paginated data
            for row, item in enumerate(paginated_data):
                table.setRowCount(row + 1)  # Add a new row for each item
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)

                    if value is not None:

                        # Add the value to the table as a QTableWidgetItem
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text

                        # Check if row index is even for alternating row colors
                        if row % 2 == 0:
                            table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                        
                        table.setItem(row, column, table_item)

    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        try:
            client = pymongo.MongoClient(connection_string)
            db_name = "LPGTrading_DB"
            return client[db_name][collectionN]
        except pymongo.errors.ConnectionError as e:
            print(f"Database connection failed: {e}")
            return None