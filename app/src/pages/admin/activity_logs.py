from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from ui.activity_logs_page import Ui_Form as activityLogsPage

from PyQt6.QtCore import QTimer
from datetime import datetime

from utils.Inventory_Monitor import InventoryMonitor

import pymongo
import re
import json

class Activity_Logs(QWidget, activityLogsPage):
    def __init__(self, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow

        self.category_filter() # call category filter
        self.status_filter() # call status filter

        # Initialize Inventory Monitory
        self.logs_monitor = InventoryMonitor('logs')
        self.logs_monitor.start_listener_in_background()
        self.logs_monitor.data_changed_signal.connect(lambda: self.update_table())

        # settings json file directory
        self.settings_dir = 'app/resources/config/settings.json'

        self.update_all() # call update table once

        self.prev_pushButton.clicked.connect(lambda: self.update_table(self.current_page - 1, self.rows_per_page))
        self.next_pushButton.clicked.connect(lambda: self.update_table(self.current_page + 1, self.rows_per_page))

        # filter connections
        self.categories_combobox.currentTextChanged.connect(lambda: self.update_table())
        self.status_combobox.currentTextChanged.connect(lambda: self.update_table())
        
    def update_all(self):
        self.update_table() # update the activity logs table

    def category_filter(self):
        categories_dir = "app/resources/data/logs.json"
        with open(categories_dir, 'r') as f:
            data = json.load(f)

        # clear combo box
        self.categories_combobox.clear()

        for category in data['categories']:
            print(f"CATEGORY: {list(category.values())[0]}")
            self.categories_combobox.addItem(list(category.values())[0])

    def status_filter(self):
        status_dir = "app/resources/data/logs.json"
        with open(status_dir, 'r') as f:
            data = json.load(f)

        # clear combo box
        self.status_combobox.clear()

        for stat in data['status']:
            print(f"STATUS: {list(stat.values())[0]}")
            self.status_combobox.addItem(list(stat.values())[0])

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

    def update_table(self, page=0, rows_per_page=15):
        """Load prices current price on the prices table with pagination."""
        self.current_page = page  # Keep track of the current page
        self.rows_per_page = rows_per_page  # Number of rows per page
        table = self.tableWidget
        table.setSortingEnabled(True)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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
        header_dir = "app/resources/config/table/activity_logs_tableHeader.json"
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

        selected_category = self.categories_combobox.currentText()
        selected_status = self.status_combobox.currentText()

        if selected_category != "None":  # Add category to filter if selected
            filter["Category"] = selected_category

        elif selected_status != "None":  # Add status to filter if selected
            filter["status"] = selected_status

        # Get data from MongoDB
        data = list(self.connect_to_db('logs').find(filter).sort("_id", -1))
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
                    if header == 'totalvalue':
                        try:
                            if value:
                                formatted_value = f"₱ {value:,.2f}"
                                value = formatted_value
                        except Exception as e:
                            print(f"Error: {e}")
                    elif header == 'saledate':
                        try:
                            if value:
                                print(f'VALUEEEEEE: {value}')
                                
                                # Directly format the datetime object
                                value = value.strftime("%Y-%m-%d")
                                print(f"DATE ONLYYYY: {value}")  # Output: 2024-12-24
                        except Exception as e:
                            print(f'Error: {e}')
                    elif header == 'quantitysold':
                        print(f'Quantity sold: {value}')                                
                    elif header == 'productssold':
                        print(f'KLEPORD GWAPO')
                        print(f'value: {value}')
                        
                        # Ensure value is a list
                        if isinstance(value, list):
                            product_num = len(value)
                            print(f'Count: {product_num}')
                            
                            view_prod_pushButton = QPushButton('View Products')
                            view_prod_pushButton.clicked.connect(lambda _, v=value, r=row: self.handle_view_products_button(v, r))
                            # view_prod_pushButton.clicked.connect(lambda: self.handle_view_products_button())
                            view_prod_pushButton.setStyleSheet("""
                            color: #000;
                            border: 1px solid #000;
                            """)
                            self.tableWidget.setCellWidget(row, column, view_prod_pushButton)
                            continue
                        else:
                            value = "Invalid product data"
                    # Add the value to the table as a QTableWidgetItem
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # Check if row index is even for alternating row colors
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                    
                    table.setItem(row, column, table_item)
    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Activity_Logs(None)  # Pass 'None' if there's no `dashboard_mainWindow` for standalone testing
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())