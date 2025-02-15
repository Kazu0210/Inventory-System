from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QFrame, QVBoxLayout, QAbstractItemView, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QIcon
from src.ui.prices_page import Ui_Form as Ui_price_page
from src.utils.Inventory_Monitor import InventoryMonitor
from src.utils.Graphics import AddGraphics
from src.custom_widgets.message_box import CustomMessageBox
from src.utils.dir import ConfigPaths
from src.utils.Logs import Logs

import json, pymongo, datetime, re, os

class PricesPage(QWidget, Ui_price_page):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        # Initialize config paths
        self.directory = ConfigPaths()

        self.is_updating_table = False  # Flag to track if the table is being updated

        self.logs = Logs

        self.load_all()
        # Initialize Inventory Monitor for prices table
        self.prices_monitor = InventoryMonitor("products")
        self.prices_monitor.start_listener_in_background()
        self.prices_monitor.data_changed_signal.connect(lambda: self.load_prices())

        # Initialize Inventory Monitor for prices history table
        self.prices_monitor = InventoryMonitor("price_history")
        self.prices_monitor.start_listener_in_background()
        self.prices_monitor.data_changed_signal.connect(lambda: self.load_price_history_table())

        self.search_pushButton.clicked.connect(lambda: self.search_button_clicked())

        # search bar connection
        self.searchBar_lineEdit.textChanged.connect(lambda: self.handle_search_change())

        # call function that hide all widgets once
        # self.hide_widgets()

        # set max lenght for search bar to 50 characters
        self.searchBar_lineEdit.setMaxLength(50)

        self.add_graphics()

    def search_button_clicked(self):
        """handles the click event for the search button"""
        # Disconnect the signal from the slot
        self.prices_tableWidget.itemChanged.disconnect(self.price_table_item_changed)
        self.load_prices()

    def set_search_icon(self):
        """Add icon to search button"""
        self.search_pushButton.setIcon(QIcon("D:/Inventory-System/app/resources/icons/black-theme/search.png"))

    def handle_search_change(self):
        """Check if the search bar is empty"""
        # Disconnect the signal from the slot

        if self.searchBar_lineEdit.text() == "":
            try:
                self.prices_tableWidget.itemChanged.disconnect(self.price_table_item_changed)
            except Exception as e:
                print(f'Error: {e}')
            self.load_prices()

    def handle_search(self):
        """Handle search when search button is clicked"""
        search_input = self.searchBar_lineEdit.text()
        print(f'Search input: {search_input}')


        collected_data = self.find_product_by_name_or_id(search_input)
        for data in collected_data:
            print(f"Collected data: {data}")

        self.load_prices()

    def add_graphics(self):
        """Add shadows, etc. to widgets."""
        graphics = AddGraphics()
        # graphics.shadow_effect(self.price_history_tableWidget, blur=10, x=-0, y=0, alpha=160)

        self.set_search_icon()

    def find_product_by_name_or_id(self, product_data):
        """Searches the collection using product id or product name"""
        # Handle blank input
        if not product_data.strip():  # Check if input is empty or only whitespace
            return []

        # Query to check for product name or product ID
        query = {
            "$or": [
                {"product_name": {"$regex": product_data, "$options": "i"}},  # Case-insensitive match
                {"product_id": {"$regex": product_data, "$options": "i"}}
            ]
        }

        # Perform the query
        results = list(self.connect_to_db("prices").find(query))

        # Return the results
        return results

    def price_table_item_changed(self, item):
        """Handles the price table item changed event"""
        try:
            if self.is_updating_table:
                print('Table is being updated, ignoring item change.')
                return

            self.prices_tableWidget.blockSignals(True)  # Temporarily block signals

            # Retrieve new value, column, and row
            new_value, column, row = item.text(), item.column(), item.row()
            product_id_item = self.prices_tableWidget.item(row, 1)
            header = self.prices_tableWidget.horizontalHeaderItem(column)

            if not product_id_item or not header:
                print("Product ID or header is missing.")
                return

            product_id, cleaned_header = product_id_item.text(), header.text().replace(' ', '_').lower()
            db = self.connect_to_db('products')
            original_value = db.find_one({'product_id': product_id}, {cleaned_header: 1}).get(cleaned_header)

            # Skip if no change
            if str(original_value) == new_value:
                print("No changes detected, skipping update.")
                return

            # Define update and log logic
            update_fields = {
                'selling_price': {'field': 'price_per_unit', 'log_event': 'product_updated'},
                'supplier_price': {'field': 'supplier_price', 'log_event': 'product_updated'}
            }

            if cleaned_header in update_fields:
                field = update_fields[cleaned_header]['field']
                try:
                    db.update_one({'product_id': product_id}, {'$set': {field: float(new_value)}})
                    if cleaned_header == 'selling_price':
                        self.save_to_price_history(product_id, new_value)
                    self.logs.record_log(event=update_fields[cleaned_header]['log_event'], product_id=product_id)
                except Exception as e:
                    print(f"Error updating {cleaned_header}: {e}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.prices_tableWidget.blockSignals(False)  # Re-enable signals


    def save_to_price_history(self, product_id, new_price):
        """Save price before and after the change to the price history collection."""        
        try:
            # Get the current date in 'YYYY-MM-DD' format
            today = datetime.datetime.today()
            formatted_date = today.strftime('%Y-%m-%d')

            # Retrieve product data (assuming only one record per product_id)
            product_data = self.connect_to_db('products').find_one({'product_id': product_id})

            if not product_data:
                print(f"Product with ID {product_id} not found.")
                return

            old_price = product_data.get('price_per_unit')
            brand = product_data.get('product_name', 'Unknown')

            # Avoid saving duplicate entries
            price_history_collection = self.connect_to_db('price_history')
            existing_entry = price_history_collection.find_one({
                'product_id': product_id,
                'price_before': float(old_price),
                'price_after': float(new_price),
                'date_of_change': formatted_date
            })

            if existing_entry:
                print(f"Duplicate entry detected in price history: Product ID {product_id}")
                return
            
            created_at = datetime.datetime.now()

            # Prepare the price history data
            prices_history_data = {
                'brand': brand,
                'date_of_change': formatted_date,
                'product_id': product_id,
                'price_before': float(old_price),
                'price_after': float(new_price),
                'created_at': created_at
            }

            # Insert the new entry
            price_history_collection.insert_one(prices_history_data)
            print(f"Price history updated for Product ID {product_id}: {prices_history_data}")
        
        except Exception as e:
            print(f"Error saving to price history: {e}")

            
    def load_price_history_table(self):
        """Loads price history table"""

        table = self.price_history_tableWidget
        table.setSortingEnabled(True)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # disable edit
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
            font: bold 10pt "Noto Sans";
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

        # header json directory
        header_dir = self.directory.get_path('price_history_header')

        # settings directory
        settings_dir = self.directory.get_path('settings')

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)
                
        header = self.price_history_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        
        # Set uniform row height for all rows
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 100

        header.setFixedHeight(40)
        header.setStretchLastSection(True)

        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]
    
        table.setColumnHidden(0, True) # hide the 1nd column assuming that is the product id

        # Filters
        # filter_query = {}
        # job_filter = self.job_filter.currentText()
        # account_status_filter = self.account_status_filter.currentText()

        # if job_filter != "Show All":
        #     filter_query['job'] = job_filter

        # if account_status_filter != "Show All":
        #     filter_query['status'] = account_status_filter

        # Get data from MongoDB
        #data = list(self.collection.find(filter_query).sort("_id", -1))
        data = list(self.connect_to_db('price_history').find({}).sort("_id", -1))
        if not data:
            return  # Exit if the collection is empty
        
        with open(settings_dir, 'r') as f:
            settings = json.load(f)
            self.current_time_format = settings['time_date'][0]['time_format']
        
        # Populate table with data
        for row, item in enumerate(data):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)
                if value is not None:
                    if header == 'pricebefore' or header == 'priceafter':
                        formatted_value = f"₱ {float(value):,.2f}"
                        value = formatted_value
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # check if row index is even
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6"))) # change item's background color to #F6F6F6 when row index is even
                    
                    table_item.setFlags(Qt.ItemFlag.NoItemFlags)  # No Interaction
                    table.setItem(row, column, table_item)

    def hide_widgets(self):
        """Hide all QWidgets that need to be hidden"""
        self.frame_11.hide() # price history frame

    def load_all(self):
        """Load all the widgets that need to be updated once or multiple times"""
        self.load_prices()
        self.load_price_history_table()
        
    def update_navigation_controls(self, total_items, current_page, rows_per_page):
        """Update the pagination navigation controls."""
        # Calculate total pages
        total_pages = (total_items - 1) // rows_per_page + 1

        # Enable/Disable "Previous" button
        if current_page > 0:
            self.prev_pushButton.setEnabled(True)
            self.prev_pushButton.setStyleSheet(
                """
                #prev_pushButton {
                background-color: #274D60;
                border-radius: 5px;
                color: #fff;
                font: 87 10pt "Noto Sans Black";
                }
                """
            )
        else:
            self.prev_pushButton.setEnabled(False)
            self.prev_pushButton.setStyleSheet(
                """
                QPushButton {
                background-color: #597784;
                border-radius: 5px;
                color: #fff;
                font: 87 10pt "Noto Sans Black";
                }
                """
            )

        # Enable/Disable "Next" button
        if current_page < total_pages - 1:
            self.next_pushButton.setEnabled(True)
            self.next_pushButton.setStyleSheet(
                """
                #next_pushButton {
                background-color: #274D60;
                border-radius: 5px;
                color: #fff;
                font: 87 10pt "Noto Sans Black";
                }
                """
            )
        else:
            self.next_pushButton.setEnabled(False)
            self.next_pushButton.setStyleSheet(
                """
                QPushButton {
                background-color: #597784;
                border-radius: 5px;
                color: #fff;
                font: 87 10pt "Noto Sans Black";
                }
                """
            )

        # Update page label
        # self.page_label.setText(f"Page: {current_page + 1}/{total_pages}")

    def get_prices_data(self, filter):
        """Get prices data for prices table"""
        result = list(self.connect_to_db('products').find(filter).sort("_id", -1))
        
        # Rename 'product_name' to 'brand' in each item in the result
        for item in result:
            if 'product_name' in item:
                item['brand'] = item.pop('product_name')  # Rename the key

            if 'price_per_unit' in item:
                item['selling_price'] = item.pop('price_per_unit')
        return result

    def load_prices(self, page=0, rows_per_page=10):
        """Load prices current price on the prices table with pagination."""
        self.current_page = page  # Keep track of the current page
        self.rows_per_page = rows_per_page  # Number of rows per page

        table = self.prices_tableWidget

        # Set the flag to indicate the table is being updated
        self.is_updating_table = True

        # Temporarily block signals to prevent itemChanged from being emitted during table population
        table.blockSignals(True) 

        self.is_updating_table = True
        table.blockSignals(True) 
        table.setSortingEnabled(True)
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table

        table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

        table.setStyleSheet("""
            QTableWidget{
            border-radius: 5px;
            background-color: #fff;
            color: #000;
            }
            QHeaderView:Section{
            background-color: #228B22;
            color: #fff;               
            font: bold 10pt "Noto Sans";
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

        header_dir = self.directory.get_path('price_header') # Header JSON directory
        settings_dir = self.directory.get_path('settings') # Settings directory

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.prices_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setStretchLastSection(True)
        
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50
        header.setFixedHeight(40)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.header_labels = [self.clean_header(header) for header in header_labels] # Clean the header labels
        # query filter
        filter = {}

        if self.searchBar_lineEdit != "":
            filter = {"$or": [
                {"product_name": {"$regex": self.searchBar_lineEdit.text(), "$options": "i"}},  # Case-insensitive match
                {"cylinder_size": {"$regex": self.searchBar_lineEdit.text(), "$options": "i"}}
            ]}

        data = self.get_prices_data(filter)
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
                    if header in ['sellingprice', 'supplierprice']: 
                        value = f"₱ {value:,.2f}"

                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    
                    # Check if row index is even
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color

                    # Make only 'sellingprice' and 'supplierprice' columns editable
                    if header == 'sellingprice' or header == 'supplierprice':
                        table_item.setFlags(table_item.flags() | Qt.ItemFlag.ItemIsEditable)  # Make editable
                    else:
                        table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make non-editable
                    
                    # Make 'Brand' and 'Cylinder Size' columns non-selectable
                    if header in ['brand', 'cylindersize']:
                        # table_item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Non-selectable
                        table_item.setFlags(Qt.ItemFlag.NoItemFlags)  # No Interaction

                    table.setItem(row, column, table_item)

        table.setColumnHidden(0, True) # hide the first column
        table.setColumnHidden(1, True) # hide the 2nd column assuming that is the product id
        # Unblock signals after table is populated
        table.blockSignals(False)
        # Reset the flag once the table is updated
        self.is_updating_table = False

        table.itemChanged.connect(self.price_table_item_changed)

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    