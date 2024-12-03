from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor
from ui.NEW.prices_page import Ui_Form as Ui_price_page

from utils.Inventory_Monitor import InventoryMonitor

import json, pymongo, datetime, re, os

class PricesPage(QWidget, Ui_price_page):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        self.load_all()

        # create floating frame for search bar results
        self.result_frame = self.search_result_frame
        self.result_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.result_frame.hide()

        result_frame_layout = QVBoxLayout(self.result_frame)

        # Initialize Inventory Monitor for prices table
        self.prices_monitor = InventoryMonitor("prices")
        self.prices_monitor.start_listener_in_background()
        self.prices_monitor.data_changed_signal.connect(lambda: self.load_prices())

        # Initialize Inventory Monitor for prices history table
        self.prices_monitor = InventoryMonitor("price_history")
        self.prices_monitor.start_listener_in_background()
        self.prices_monitor.data_changed_signal.connect(lambda: self.load_price_history_table())

        # button connections
        self.price_history_pushButton.clicked.connect(lambda: self.show_price_history())
        self.prev_pushButton.clicked.connect(lambda: self.load_prices(self.current_page - 1, self.rows_per_page))
        self.next_pushButton.clicked.connect(lambda: self.load_prices(self.current_page + 1, self.rows_per_page))

        # call function that hide all widgets once
        self.hide_widgets()

        # connection for search bar
        self.searchBar_lineEdit.textChanged.connect(self.handle_search_bar)

        # set max lenght for search bar to 50 characters
        self.searchBar_lineEdit.setMaxLength(50)

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

    def handle_search_bar(self, text):
        try:
            # Clear the console for better debugging
            os.system('cls')
            print(f'Text Changed: {text}')

            # Call the search function and collect data
            collected_data = self.find_product_by_name_or_id(text)
            print(f'Data type: {type(collected_data)}')

            # Check if data is found
            if collected_data:
                self.result_frame.show()  # Show the frame if there is data
                for data in collected_data:
                    print(f"Product Name: {data.get('product_name', 'N/A')}")
                    print(f"Product ID: {data.get('product_id', 'N/A')}")
            else:
                print("No matching products found.")
                self.result_frame.hide()  # Hide the frame if no data is found

        except IndexError as e:
            # Log and handle an IndexError
            os.system('cls')
            print(f'Error: Index out of range - {e}')
            self.result_frame.hide()  # Hide the frame in case of an error

        except Exception as e:
            # Handle unexpected errors
            print(f"Unexpected error occurred: {e}")
            self.result_frame.hide()  # Ensure the frame is hidden in case of an error

    def show_price_history(self):
        """Run when price history button is clicked"""
        self.price_history_tableWidget.show()
        self.price_history_pushButton.setText("Hide Price History")

        self.price_history_pushButton.clicked.connect(lambda: self.hide_price_history())

    def hide_price_history(self):
        """Run when hide price history button is clicked"""
        self.price_history_tableWidget.hide()
        self.price_history_pushButton.setText("Show Price History")
        self.price_history_pushButton.clicked.connect(lambda: self.show_price_history())

    def load_price_history_table(self):
        """Loads price history table"""

        table = self.price_history_tableWidget
        table.setSortingEnabled(True)
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table

        # header json directory
        header_dir = "app/resources/config/table/priceHistory_tableHeader.json"

        # settings directory
        settings_dir = "app/resources/config/settings.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)
                
        header = self.prices_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)

        for column in range(table.columnCount()):
            table.setColumnWidth(column, 200)

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
        self.price_history_tableWidget.hide()

    def load_all(self):
        """Load all the widgets that need to be updated once or multiple times"""
        self.load_prices()
        self.load_price_history_table()
        
    def update_navigation_controls(self, total_items, current_page, rows_per_page):
        """Update the pagination navigation controls."""
        total_pages = (total_items - 1) // rows_per_page + 1

        # Enable/Disable navigation buttons
        self.prev_pushButton.setEnabled(current_page > 0)
        self.next_pushButton.setEnabled(current_page < total_pages - 1)

        # Update page label
        # self.page_label.setText(f"Page: {current_page + 1}/{total_pages}")

    def load_prices(self, page=0, rows_per_page=10):
        """Load prices current price on the prices table with pagination."""
        self.current_page = page  # Keep track of the current page
        self.rows_per_page = rows_per_page  # Number of rows per page

        table = self.prices_tableWidget
        table.setSortingEnabled(True)
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table

        # Header JSON directory
        header_dir = "app/resources/config/table/prices_tableHeader.json"

        # Settings directory
        settings_dir = "app/resources/config/settings.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.prices_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)

        for column in range(table.columnCount()):
            table.setColumnWidth(column, 200)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

        # Get data from MongoDB
        data = list(self.connect_to_db('prices').find({}).sort("_id", -1))
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
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # Check if row index is even
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                    table.setItem(row, column, table_item)

        # Add navigation controls
        self.update_navigation_controls(len(data), page, rows_per_page)


    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    