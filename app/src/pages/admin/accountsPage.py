import pymongo
from PyQt6.QtWidgets import *
from ui.NEW.accounts_page import Ui_Form as accounts_page
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QWaitCondition, QMutex, QTimer
from PyQt6.QtGui import QBrush, QColor
from utils.Hashpassword import HashPassword
from utils.Activity_logs import Activity_Logs
from pages.admin.edit_account_page import editAccountPage

from utils.Inventory_Monitor import InventoryMonitor
from datetime import datetime
import re
import json
import os


class AccountsPage(QWidget, accounts_page):
    def __init__(self, username, dashboard_mainWindow=None):
        super().__init__()
        self.setupUi(self)
        self.dashboard_mainWindow = dashboard_mainWindow

        # initialize inventory monitor for change in database
        self.inventory_monitor = InventoryMonitor("accounts")
        self.inventory_monitor.start_listener_in_background()

        # username of the account logged in
        self.account_username = username

        self.createAccount_btn.clicked.connect(self.create_account)

        self.collection = self.connect_to_db('accounts')
        self.archive_collection = self.connect_to_db('account_archive')

        self.selected_row = None

        # create a timer to periodically update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(100)

        self.tableWidget.itemSelectionChanged.connect(self.on_row_clicked)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

        # create the dialog instance variable
        self.new_job_dialog = None
        
        self._accounts_table = self.tableWidget

        # update all the filter only once
        self.update_filters()

        print(self.generate_account_id(self.collection))

        self.hide_buttons()

        self.current_logged_in()

    def current_logged_in(self):
        # get the current logged in user's account id
        print(f'Getting current logged in account')
        logged_in_account = self.account_username
        print(f'Current logged in account: {logged_in_account}')
        
        return logged_in_account

    def get_account_total(self):
        # get total number of account and set text label
        self.total_accounts = str(self.collection.count_documents({}))
        self.total_account_label.setText(self.total_accounts)

    def update_filters(self):
        self.add_job_filter()
        self.add_account_status_filter()

    def update_all(self):
        self.update_table()
        self.get_account_total()

    def add_account_status_filter(self):
        filter_dir = "app/resources/config/filters.json"

        with open(filter_dir, 'r') as f:
            data = json.load(f)

        self.account_status_filter.clear()
        for status in data['account_status']:
            self.account_status_filter.addItem(list(status.values())[0])

    def add_job_filter(self):
        job_dir = "app/resources/config/filters.json"

        with open(job_dir, 'r') as f:
            data = json.load(f)

        self.job_filter.clear()

        for job in data['job']:
            self.job_filter.addItem(list(job.values())[0])

    def get_accounts_table(self):
        return self._accounts_table

    def create_account(self):
        if self.dashboard_mainWindow:
            self.dashboard_mainWindow.content_window_layout.setCurrentIndex(3)

    def on_item_clicked(self, item):
        row = self.tableWidget.row(item)
        self.tableWidget.selectRow(row)

    def hide_buttons(self):
        # hide buttons when no item or product is selected
        self.edit_btn.hide()
        self.archive_pushButton.hide()

    def show_buttons(self):
        # show buttons when an item or product is clicked
        self.edit_btn.show()
        self.archive_pushButton.show()

    def on_row_clicked(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        self.show_buttons()
        if selected_rows:
            self.timer.stop()

            row_index = selected_rows[0].row()
            print(f"Row {row_index} clicked")

            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_index, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")

            account_header_dir = "app/resources/config/table/accounts_tableHeader.json"

            with open(account_header_dir, 'r') as f:
                data = json.load(f)

            # try:
            #     if 'Username' in data:
            #         username_header_index = data.index("Username")
            #     else:
            #         print("Username column doesn't exist")
            # except Exception as e:
            #     print(f"An error occurred: {e}")

            try:
                if 'Account ID' in data:
                    account_id_header_index = data.index("Account ID")
                else:
                    print("Account ID column doesn't exist")
            except Exception as e:
                print(f"An error occurred: {e}")

            document = self.collection.find_one({'account_id': row_data[account_id_header_index]}) # get all data by username on the database
            # print(f"USERNAME: {row_data[username_header_index]}")
            print(f"ACCOUNT ID: {row_data[account_id_header_index]}")
            object_id = document['_id'] # get _id of username

            # get all the index from the database using the objectId
            self.username = document['username']
            self.accountID = document['account_id']
            self.password = document['password']
            self.fname = document['first_name']
            self.lname = document['last_name']
            self.email = document['email']
            self.address = document['address']
            self.user_type = document['user_type']
            self.job = document['job']
            self.account_status = document['status']
            self.last_login = document['last_login']
            print(f"CLICKED ACCOUNT ID {self.accountID}")

            self.selected_row = row_index
            
            print(f'selected row index: {self.selected_row}')
            
            # add the data to the account information section
            self.accountID_label.setText(self.accountID)
            self.username_label.setText(self.username)
            self.pass_label.setText("*******")
            # self.username_label.setText(self.username)
            self.fname_label.setText(self.fname)
            self.lname_label.setText(self.lname)
            self.email_label.setText(self.email)
            self.address_label.setText(self.address)
            self.usertype_label.setText(self.user_type)
            self.job_label.setText(self.job)
            self.account_status_label.setText(self.account_status)
            self.last_login_label.setText(self.last_login)

            # Update the object_id variable
            self.object_id = object_id

            # Connect the edit button
            if not hasattr(self, 'edit_btn_connected'):
                if self.accountID is not None:
                    self.edit_btn.clicked.connect(lambda: self.show_editAccountPage(self.accountID))
                    self.edit_btn_connected = True
                else:
                    print("Account ID is None")     

            if not hasattr(self, 'archive_btn_clicked'):
                if self.accountID is not None:
                    self.archive_pushButton.clicked.connect(lambda: self.add_to_archive(self.accountID))
                    self.archive_btn_clicked = True
                else:
                    print("Account ID is None")
        else:
            self.selected_row = None
            self.hide_buttons()
            self.accountID_label.setText("")
            self.address_label.setText("")
            self.username_label.setText("")
            self.fname_label.setText("")
            self.lname_label.setText("")
            self.pass_label.setText("")
            self.job_label.setText("")
            self.usertype_label.setText("")
            self.account_status_label.setText("")
            self.email_label.setText("")
            self.last_login_label.setText("")
            print("No row is selected")
            self.timer.start()

    def add_to_archive(self, account_id):
        os.system('cls')

        if not self.object_id:
            print('Object ID is empty')
            return
        
        print(f'Received account id: {account_id}')

        data = list(self.collection.find({"account_id": account_id}, {"_id": 0}))
        print(f'Data collected using the Account id: {account_id}: {data}')
        
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        print('archive button clicked')
        reply = QMessageBox.question(
            self, 
            "Archive Confirmation", 
            "Are you certain you want to add this account to the archive?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print('Clicked yes')

            # Get the ObjectId of the account to be deleted
            self.collection.delete_one({'_id': self.object_id})

            # Remove the row from the table
            row_index = selected_rows[0].row()
            self.tableWidget.removeRow(row_index)

            print(f"DATA NA KELANGAN KOOO: {data}")
            # data.pop('_id')

            print(f'BAGONG DATA: {data}')

            try:
                # If data is a list, iterate over each dictionary
                if isinstance(data, list):
                    for item in data:
                        item['status'] = "Inactive"
                        self.archive_collection.insert_one(item)
                else:
                    # If data is a single dictionary, update it directly
                    data['status'] = "Inactive"
                    self.archive_collection.insert_one(data)
            except Exception as e:
                print(f"Error adding to archive: {e}")

            # Update the selected_row variable
            self.selected_row = None

            # Clear the account information section
            self.username_label.setText("")
            self.fname_label.setText("")
            self.lname_label.setText("")
            self.pass_label.setText("")
            self.job_label.setText("")
            self.usertype_label.setText("")
        
        self.timer.start()

    def on_job_field_changed(self, index):
        if index == self.job_field.count() - 1:
            if not self.new_job_dialog:
                self.new_job_dialog = QDialog(self)
                self.new_job_dialog.setWindowTitle("Add new Job")
                self.new_job_dialog.setModal(True)
                new_job_layout = QVBoxLayout()
                self.new_job_dialog.setLayout(new_job_layout)
                
                new_job_title_label = QLabel("New Job Title:")
                self.new_job_title_field = QLineEdit()
                new_job_layout.addWidget(new_job_title_label)
                new_job_layout.addWidget(self.new_job_title_field) 

                save_button = QPushButton("Add Job Title")
                new_job_layout.addWidget(save_button)

                save_button.clicked.connect(lambda: self.save_new_job_title(self.new_job_title_field.text()))

            self.new_job_dialog.show()

    def save_new_job_title(self, new_job_title):
        print(f'New Job title: {new_job_title}')

        with open('app/resources/data/job_titles.json', 'r') as f:
            job_titles = json.load(f)   

        job_titles.append(new_job_title)

        with open('app/resources/data/job_titles.json', 'w') as f:
            json.dump(job_titles, f)

        # Update the job_field combobox
        self.job_field.addItem(new_job_title)
        self.job_field.setCurrentIndex(self.job_field.count() - 1)

        self.new_job_dialog.accept()

    def show_editAccountPage(self, account_id):
        # if not hasattr(self, 'edit_account_page'):
        #     self.edit_account_page = editAccountPage(account_id)
        # self.edit_account_page.show()
        print(f"ACCOUNT ID FROM ACCOUNTS PAGE: {account_id}")
        self.edit_account_page = editAccountPage(account_id)
        self.edit_account_page.show()

    def edit_account(self):
        print(f'Edit account button clicked.')
        print(f'Username: {self.username}')

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Account")
        dialog.setModal(True)

        layout = QVBoxLayout()
        dialog.setLayout(layout)

        username_label = QLabel("Username:")
        username_field = QLineEdit(self.username)
        layout.addWidget(username_label)
        layout.addWidget(username_field)

        fname_label = QLabel("First Name:")
        fname_field = QLineEdit(self.fname)
        layout.addWidget(fname_label)
        layout.addWidget(fname_field)

        lname_label = QLabel("Last Name:")
        lname_field = QLineEdit(self.lname)
        layout.addWidget(lname_label)
        layout.addWidget(lname_field)

        pass_label = QLabel("Password:")
        pass_field = QLineEdit(self.password)
        layout.addWidget(pass_label)
        layout.addWidget(pass_field)

        job_label = QLabel("Job:")
        self.job_field = QComboBox()
        self.job_field.addItem(self.job)

        # Load job titles from JSON file
        with open('app/resources/data/job_titles.json', 'r') as f:
            job_titles = json.load(f)
        
        # Add job titles to the combobox
        for job_title in job_titles:
            self.job_field.addItem(job_title)

        self.job_field.insertItem(self.job_field.count(), "Add")
        layout.addWidget(job_label)
        layout.addWidget(self.job_field)

        add_job_title_option = self.job_field.count() - 1
        print(f"Last index {add_job_title_option}")

        self.job_field.currentIndexChanged.connect(self.on_job_field_changed)

        usertype_label = QLabel("User Type:")
        usertype_field = QLineEdit(self.user_type)
        layout.addWidget(usertype_label)
        layout.addWidget(usertype_field)

        with open("app/resources/config/filters.json") as f: # get all account status filter from json file
            data = json.load(f)

        

        status_label = QLabel("Account Status:")
        status_field = QComboBox()

        for stat in data['account_status']:
            print(f"ACCOUNT STATUS FILTERS: {list(stat.values())[0]}")
            status_field.addItem(list(stat.values())[0])

        layout.addWidget(status_label)
        layout.addWidget(status_field)

        save_button = QPushButton("Save Changes")
        layout.addWidget(save_button)
        

        save_button.clicked.connect(lambda: self.save_changes(dialog, self.selected_row, username_field, fname_field, lname_field, pass_field, self.job_field, usertype_field, status_field))

        dialog.exec()
        self.selected_row = None
        print(f'Seleted row: {self.selected_row}')

    def save_changes(self, dialog, row_index, username_field, fname_field, lname_field, pass_field, job_field, usertype_field, status_field):
        status_currentText = status_field.currentText()
        print(f"status: {status_currentText}")

        # Get the new data for the account
        new_username = username_field.text().strip()
        new_fname = fname_field.text().strip()
        new_lname = lname_field.text().strip()
        new_pass = pass_field.text().strip()
        new_job = job_field.currentText()
        new_usertype = usertype_field.text().strip()
        new_status = status_currentText

        hasher = HashPassword(new_pass)
        hashed_password = hasher.hash_password()
        print(f"hashed password: {hashed_password}")

        print(f'new status: {new_status}')

        # save to activity logs
        logs = Activity_Logs()
        logs.edit_account(self.account_username, self.username)

        # Update the account in the database
        self.collection.update_one({"_id": self.object_id}, {"$set": {"username": new_username, "first_name": new_fname, "last_name": new_lname, "password": hashed_password, "job": new_job, "user_type": new_usertype, "status": new_status}})

        # Update the row in the table
        if row_index is not None:
            self.tableWidget.setItem(row_index, 3, QTableWidgetItem(new_username))
            self.tableWidget.setItem(row_index, 1, QTableWidgetItem(new_fname))
            self.tableWidget.setItem(row_index, 2, QTableWidgetItem(new_lname))
            self.tableWidget.setItem(row_index, 4, QTableWidgetItem(hashed_password))
            self.tableWidget.setItem(row_index, 5, QTableWidgetItem(new_job))
            self.tableWidget.setItem(row_index, 6, QTableWidgetItem(new_usertype))
            self.tableWidget.setItem(row_index, 7, QTableWidgetItem(new_status))

        # Close the dialog
        dialog.accept()
        self.timer.start()


    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

    def update_table(self):
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
        filter_query = {}
        job_filter = self.job_filter.currentText()
        account_status_filter = self.account_status_filter.currentText()

        if job_filter != "Show All":
            filter_query['job'] = job_filter

        if account_status_filter != "Show All":
            filter_query['status'] = account_status_filter

        # Get data from MongoDB
        data = list(self.collection.find(filter_query).sort("_id", -1))
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
                        try:
                            if value:
                                date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

                                if self.current_time_format == "12hr":
                                    value = date_time.strftime("%Y-%m-%d %I:%M:%S %p")
                                else:
                                    value = date_time.strftime("%Y-%m-%d %H:%M:%S")
                        except Exception as e:
                            pass
                            # print(f"Error formatting date: {e}")

                    if value == self.current_logged_in():
                        print(f"Current logged-in account is: {self.current_logged_in()}")
                        name = value

                        value = f"{name} (Logged in)"
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
    
    def generate_account_id(self, collection):
        import datetime
        id = int(datetime.date.today().strftime("%Y%m%d"))
        counter = 1
        while True:
            account_id = f"{id:08d}{counter:03d}"
            if not collection.find_one({"account_id": account_id}):
                return account_id
            counter += 1