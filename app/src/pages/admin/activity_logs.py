from PyQt6.QtWidgets import *
from ui.activity_logs_page import Ui_Form as activityLogsPage
from PyQt6.QtCore import QTimer
from datetime import datetime
import pymongo
import re
import json

class Activity_Logs(QWidget, activityLogsPage):
    def __init__(self, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow

        self.collection = self.connect_to_db()

        self.category_filter() # call category filter
        self.status_filter() # call status filter
        
        # Create a timer to periodically update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(100)


        # settings json file directory
        self.settings_dir = 'app/resources/config/settings.json'
        
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

    def connect_to_db(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = "logs"
        return client[db][collection_name]

    def update_table(self):
        table = self.tableWidget
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table

        # header json directory
        header_dir = "app/resources/config/table/activity_logs_tableHeader.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        # set width of all the columns
        for column in range(table.columnCount()):
            table.setColumnWidth(column, 200)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

        category_filter = self.categories_combobox.currentText()
        status_filter = self.status_combobox.currentText()
        
        if category_filter == "None":
            filter_query = {}  # Define an empty filter query
        else:
            filter_query = {"Category": category_filter}

        if status_filter != "None":
            filter_query["status"] = status_filter

        data = list(self.collection.find(filter_query).sort("_id", -1))
        if not data:
            return  # Exit if the collection is empty
        
        with open(self.settings_dir, 'r') as f:
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
                        if header == 'datetime':
                            # value contains the date and time 
                            date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                            if self.current_time_format == "12hr":
                                value = date_time.strftime("%Y-%m-%d %I:%M:%S %p")
                            else:
                                value = date_time.strftime("%Y-%m-%d %H:%M:%S")


                        table.setItem(row, column, QTableWidgetItem(str(value)))
    
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