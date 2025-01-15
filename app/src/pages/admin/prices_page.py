from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QFrame, QVBoxLayout, QAbstractItemView, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QIcon
from src.ui.final_ui.prices_page import Ui_Form as Ui_price_page
from src.utils.Inventory_Monitor import InventoryMonitor
from src.utils.Graphics import AddGraphics
from src.custom_widgets.message_box import CustomMessageBox

import json, pymongo, datetime, re, os

class PricesPage(QWidget, Ui_price_page):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        self.load_all()

        # Initialize Inventory Monitor for prices table
        self.prices_monitor = InventoryMonitor("prices")
        self.prices_monitor.start_listener_in_background()
        self.prices_monitor.data_changed_signal.connect(lambda: self.load_prices())

        # Initialize Inventory Monitor for prices history table
        self.prices_monitor = InventoryMonitor("price_history")
        self.prices_monitor.start_listener_in_background()
        self.prices_monitor.data_changed_signal.connect(lambda: self.load_price_history_table())

        # button connections
        # self.price_history_pushButton.clicked.connect(lambda: self.show_price_history())
        # self.prev_pushButton.clicked.connect(lambda: self.load_prices(self.current_page - 1, self.rows_per_page))
        # self.next_pushButton.clicked.connect(lambda: self.load_prices(self.current_page + 1, self.rows_per_page))
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

    def show_price_history(self):
        """Run when price history button is clicked"""
        self.frame_11.show()
        self.price_history_pushButton.setText("Hide Price History")

        self.price_history_pushButton.clicked.connect(lambda: self.hide_price_history())

    def hide_price_history(self):
        """Run when hide price history button is clicked"""
        self.frame_11.hide()
        self.price_history_pushButton.setText("Show Price History")
        self.price_history_pushButton.clicked.connect(lambda: self.show_price_history())

    def price_table_item_changed(self, item):
        """Handles the price table item changed event."""
        print(f"Item changed at Row: {item.row()}, Column: {item.column()}")
        print(f"New Value: {item.text()}")

        try:
            new_value = item.text()  # Try converting to float, can be int or float
            column = item.column()
            row = item.row()
            print(f'Column: {column}')
        except ValueError:
            # If the conversion fails, show an error and exit
            CustomMessageBox.show_message('critical', 'Error', 'Invalid price value')
            print(f'Error: Invalid value for price: {item.text()}')
            return  # Exit early if the value is not a valid number

        # Get product id and header
        product_id = self.prices_tableWidget.item(row, 1)  # Get the product ID (assumes it's in column 1)
        header = self.prices_tableWidget.horizontalHeaderItem(column)

        if product_id:  # Check if product id exists
            product_id_value = product_id.text()

            # Update the price if the header matches
            if header and header.text() in ['Selling Price', 'Supplier Price']:
                # Confirm with the user before updating
                question = CustomMessageBox.show_message('question', f'Update {header.text()} value', 
                                                        f'Are you sure you want to update the {header.text()} value for product {product_id_value} to {new_value}?')
                if question == 1:  # User confirmed the update
                    try:
                        # Choose the field based on the header
                        field = 'price_per_unit' if header.text() == 'Selling Price' else 'supplier_price'
                        
                        # Prepare filter and update query
                        filter = {'product_id': product_id_value}
                        update = {'$set': {field: float(new_value)}}  # Update the price (as float)

                        # Perform the update in the database
                        self.connect_to_db('products_items').update_one(filter, update)

                        # Show success message
                        CustomMessageBox.show_message('information', 'Price Update', f'{header.text()} Updated Successfully!')

                        # Temporarily disconnect the signal to prevent re-triggering the function during reload
                        self.prices_tableWidget.itemChanged.disconnect(self.price_table_item_changed)

                        # Reload the table (refresh the data)
                        self.load_prices()

                        # Reconnect the signal after the reload
                        self.prices_tableWidget.itemChanged.connect(self.price_table_item_changed)

                    except Exception as e:
                        print(f'Error updating data: {e}')
            
    def load_price_history_table(self):
        """Loads price history table"""

        table = self.price_history_tableWidget
        table.setSortingEnabled(True)
        # table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers) # enable edit
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # disable edit
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table
        # table.itemChanged.connect(self.price_table_item_changed)

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
        header_dir = "D:/Inventory-System/app/resources/config/table/priceHistory_tableHeader.json"

        # settings directory
        settings_dir = "D:/Inventory-System/app/resources/config/settings.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)
                
        header = self.price_history_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)

        # for column in range(table.columnCount()):
        #     table.setColumnWidth(column, 145)

        # Set uniform row height for all rows
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 100

        header.setFixedHeight(40)
        header.setStretchLastSection(True)

        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

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
                    # if header == 'lastlogin':
                    #     try:
                    #         if value:
                    #             date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                    #             if self.current_time_format == "12hr":
                    #                 value = date_time.strftime("%Y-%m-%d %I:%M:%S %p")
                    #             else:
                    #                 value = date_time.strftime("%Y-%m-%d %H:%M:%S")
                    #     except Exception as e:
                    #         pass
                    #         # print(f"Error formatting date: {e}")
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # check if row index is even
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6"))) # change item's background color to #F6F6F6 when row index is even
                            
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
        result = list(self.connect_to_db('products_items').find(filter).sort("_id", -1))
        
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

        # Header JSON directory
        header_dir = "D:/Inventory-System/app/resources/config/table/prices_tableHeader.json"

        # Settings directory
        settings_dir = "D:/Inventory-System/app/resources/config/settings.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.prices_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setStretchLastSection(True)

        # for column in range(table.columnCount()):
        #     table.setColumnWidth(column, 145)

        # Set uniform row height for all rows
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

        header.setFixedHeight(40)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]
        
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
                    if header == 'sellingprice' or header == 'supplierprice':  # Modify this check as needed
                        table_item.setFlags(table_item.flags() | Qt.ItemFlag.ItemIsEditable)  # Make editable
                    else:
                        table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make non-editable

                    table.setItem(row, column, table_item)

        table.itemChanged.connect(self.price_table_item_changed)

        # hide the first column
        table.setColumnHidden(0, True)
        # Add navigation controls
        # self.update_navigation_controls(len(data), page, rows_per_page)

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    