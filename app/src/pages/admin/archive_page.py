from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QFrame, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from datetime import datetime
import json, os, pymongo, re, threading

from ui.NEW.archive_page import Ui_Form as Ui_archive
from ui.final_ui.archive_account_information import Ui_Frame as Ui_archive_account_info
from utils.Inventory_Monitor import InventoryMonitor

class AccountArchive(QFrame, Ui_archive_account_info):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        
class ArchivePage(QWidget, Ui_archive):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # hide the preview frames
        self.hide_preview_frames()
        self.hide_buttons()

        # set currennt collection 
        self.current_collection = None

        # Connect button
        self.accounts_pushButton.clicked.connect(lambda: self.setActiveCollection('account_archive'))
        self.products_pushButton.clicked.connect(lambda: self.setActiveCollection('product_archive'))
        self.restore_pushButton.clicked.connect(lambda: self.restoreButtonClicked())
        self.delete_pushButton.clicked.connect(lambda: self.deleteButtonClicked())
        
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
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

    def deleteButtonClicked(self):
        """Handle clicked event of delete button"""
        data = self.current_document
        print(f'Retrieved data when button clicked: {data}')

        if '_id' in data:
            del data['_id']

        if self.current_collection == 'account_archive':
            account_id = data['account_id'] # get account id 
            filter = {
                'account_id': account_id
            }
            self.connect_to_db(self.current_collection).delete_one(filter)
            QMessageBox.information(self, "Success", "Account deleted successfully")

        elif self.current_collection == 'product_archive':
            product_id = data['product_id'] # get account id 
            filter = {
                'product_id': product_id
            }
            self.connect_to_db(self.current_collection).delete_one(filter)
            QMessageBox.information(self, "Success", "Product deleted successfully")

    def restoreButtonClicked(self):
        """Handle clicked event of restore button"""
        data = self.current_document
        print(f'Retrieved data when button clicked: {data}')

        if '_id' in data:
            del data['_id']


        if self.current_collection == 'account_archive':
            account_id = data['account_id'] # get account id 
            filter = {
                'account_id': account_id
            }
            self.connect_to_db("accounts").insert_one(data)
            self.connect_to_db(self.current_collection).delete_one(filter)
            QMessageBox.information(self, "Success", "Account restored successfully")

        elif self.current_collection == 'product_archive':
            product_id = data['product_id'] # get account id 
            filter = {
                'product_id': product_id
            }
            self.connect_to_db("products_items").insert_one(data)
            self.connect_to_db(self.current_collection).delete_one(filter)
            QMessageBox.information(self, "Success", "Product restored successfully")

    def on_item_clicked(self, item):
        row = self.tableWidget.row(item)
        self.tableWidget.selectRow(row)

    def on_row_clicked(self):
        self.selected_rows = self.tableWidget.selectionModel().selectedRows()

        if self.selected_rows:
            # Show action buttons
            self.frame_23.show()

            row_index = self.selected_rows[0].row()
            print(f"Row {row_index} clicked")

            row_data_with_headers = {}

            for column in range(self.tableWidget.columnCount()):
                header_item = self.tableWidget.horizontalHeaderItem(column)
                header_text = header_item.text() if header_item is not None else f"Column {column + 1}"
                cleaned_header = self.clean_header(header_text)

                item = self.tableWidget.item(row_index, column)
                cell_text = item.text() if item is not None else ""

                row_data_with_headers[cleaned_header] = cell_text

            print(f"Row data with headers: {row_data_with_headers}")

            header = list(row_data_with_headers.keys())[0]
            value = row_data_with_headers[header]
            print(f'Header: {header}')
            print(f'Value: {value}')

            print(f'Current collection: {self.current_collection}')
            if self.current_collection == "account_archive":
                filter = {
                    "account_id": value,
                }
            else:
                filter = {
                    "product_id": value,
                }

            # Fetch the document and store it in an instance variable
            self.current_document = self.connect_to_db(str(self.current_collection)).find_one(filter)

            # Update preview section
            if self.current_collection in ["account_archive", "product_archive"]:
                self.set_label(self.current_document)

        else:
            self.hide_buttons()
            self.clearPreviewSection()

    # def restoreButtonClicked(self):
    #     if hasattr(self, 'current_document') and self.current_document:
    #         # Perform restore action using the current document
    #         print(f"Restoring document: {self.current_document}")
    #         # Add your restore logic here
    #     else:
    #         print("No document selected for restore.")

    def clearPreviewSection(self):
        """Clear the preview section labels"""
        self.name_label.clear()
        self.username_label.clear()
        self.email_label.clear()
        self.usertype_label.clear()
        self.job_label.clear()
        self.status_label.clear()
        self.lastlogin_label.clear()
        self.productid_label.clear()
        self.product_name_label.clear()
        self.cylinder_size_label.clear()
        self.quantity_label.clear()
        self.price_label.clear()
        self.supplier_label.clear()
        self.restock_date_label.clear()
        self.inv_stat_label.clear()

    def set_label(self, data):
        """insert data to the labels of preview""" 
        print(f'DATA TO SET LABELS: {data}')

        collection = self.current_collection

        if collection == "account_archive":
            try:
                # get data
                fname = data.get('first_name', 'N/A')
                lname = data.get('last_name', 'N/A')

                full_name = f"{lname}, {fname}"
                username = data.get('username', 'N/A')
                email = data.get('email', 'N/A')
                user_type = data.get('user_type', 'N/A')
                job = data.get('job', 'N/A')
                status = data.get('status', 'N/A')
                last_login = data.get('last_login', 'N/A')

                # set labels
                self.name_label.setText(full_name)
                self.username_label.setText(username)
                self.email_label.setText(email)
                self.usertype_label.setText(user_type)
                self.job_label.setText(job)
                self.status_label.setText(status)
                self.lastlogin_label.setText(last_login)
            except Exception as e:
                print(f'Error: {e}')
                QMessageBox.critical(self, f"Error", f"An Error Occurred\n{e}")

        elif collection == "product_archive":
            try:
                # get data
                product_id = data.get('product_id', 'N/A')
                product_name = data.get('product_name', 'N/A')
                cylinder_size = data.get('cylinder_size', 'N/A')
                quantity_in_stock = str(data.get('quantity_in_stock', 'N/A'))

                price = data.get('price_per_unit', 'N/A')
                formatted_price = f"₱ {price:,.2f}"

                supplier = data.get('supplier', 'N/A')
                last_restock_date = data.get('last_restocked_date', 'N/A')
                inventory_status = data.get('inventory_status', 'N/A')

                # set labels
                self.productid_label.setText(product_id)
                self.product_name_label.setText(product_name)
                self.cylinder_size_label.setText(cylinder_size)
                self.quantity_label.setText(quantity_in_stock)
                self.price_label.setText(formatted_price)
                self.supplier_label.setText(supplier)
                self.restock_date_label.setText(last_restock_date)
                self.inv_stat_label.setText(inventory_status)
            except Exception as e:
                print(f'Error: {e}')
                QMessageBox.critical(self, f"Error", f"An Error Occurred\n{e}")
        
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
            self.selected_rows = None
            self.table_name_label.setText('Archived Accounts')
            self.archive_account_frame.show()
            self.archive_product_frame.hide()
            self.loadAccounts()
        elif collection_name == "product_archive":
            self.selected_rows = None
            self.table_name_label.setText('Archived Products')
            self.archive_account_frame.hide()
            self.archive_product_frame.show()
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
            QTableWidget::item:selected {
            color: #000;  /* Change text color */
            background-color: #E7E7E7;  /* Optional: Change background color */
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
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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
            QTableWidget::item:selected {
                color: #000;  /* Change text color */
                background-color: #E7E7E7;  /* Optional: Change background color */
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
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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

                        if header == "lastlogin":
                            if value:
                                try:
                                    parsed_datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                                    # Format the date and time
                                    formatted_date = parsed_datetime.strftime("%Y/%m/%d")
                                    formatted_time = parsed_datetime.strftime("%H:%M:%S")

                                    value = f'{formatted_date}, {formatted_time}'
                                except Exception as e:
                                    print(f'An error occured: {e}')

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
        
    def hide_preview_frames(self):
        """Hide the preview frames in the UI"""
        self.archive_account_frame.hide()
        self.archive_product_frame.hide()

    def hide_buttons(self):
        """Hide action buttons"""
        self.frame_23.hide()