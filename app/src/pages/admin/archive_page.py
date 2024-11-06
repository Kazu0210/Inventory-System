from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor
from datetime import datetime

from ui.NEW.archive_page import Ui_Form as Ui_archive

from utils.Inventory_Monitor import InventoryMonitor

import json, os, pymongo, re


class ArchivePage(QWidget, Ui_archive):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # buttons connecion
        self.accounts_pushButton.clicked.connect(lambda: self.accounsBtnClicked())
        
        # Initialize collection monitor
        self.accounts_monitor = InventoryMonitor('account_archive')
        self.accounts_monitor.start_listener_in_background()

        self.accounts_monitor.data_changed_signal.connect(lambda: self.handle_signal())

    def handle_signal(self):
        print('GUMANAAAAAAAAAAAA')
        print('Loading table')
        self.loadTable()

    def loadAccounts(self):
        table = self.tableWidget
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table
        
        # header json directory
        header_dir = "app/resources/config/table/accounts_tableHeader.json"

        # settings directory
        settings_dir = "app/resources/config/settings.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

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
        data = list(self.connect_to_db('account_archive').find().sort("_id", -1))
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
                    if header == 'lastlogin':
                        if value:
                            date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                            if self.current_time_format == "12hr":
                                value = date_time.strftime("%Y-%m-%d %I:%M:%S %p")
                            else:
                                value = date_time.strftime("%Y-%m-%d %H:%M:%S")
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # check if row index is even
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6"))) # change item's background color to #F6F6F6 when row index is even
                    table.setItem(row, column, table_item)

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    
    def loadTable(self, collection_name):
        print(f'Collection name: {collection_name}')

        if collection_name == "account_archive":
            print('accounts archive')
            self.loadAccounts()

    def accounsBtnClicked(self):
        os.system('cls')
        print(f'Accounts button clicked')
        
        self.loadTable('account_archive')

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]