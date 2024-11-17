from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
from ui.main_window import Ui_MainWindow
from pages.admin.activity_logs import Activity_Logs
from pages.admin.accountsPage import AccountsPage
# from accountsPage import UpdateThread
# from newEmployee_page import newEmployeePage
from pages.admin.dashboard_page import Dashboard
from pages.admin.itemsPage import ItemsPage
from pages.admin.newitemsPage import newItem_page as NewItem
from pymongo import MongoClient
from utils.Activity_logs import Activity_Logs as activity_logs
from pages.admin.settings_page import settingsPage
from pages.admin.new_account_page import NewAccountPage
from pages.admin.order_page import OrderPage
from pages.admin.backp_restore import BackupRestorePage
from pages.admin.archive_page import ArchivePage
from pages.admin.sales_report_page import SalesReportPage
import re
import json
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # activity logs
        self.logs = activity_logs()

        # logged in account username
        self.account_username = username

        client = MongoClient('mongodb://localhost:27017/')
        db = client['LPGTrading_DB']
        self.collection = db['accounts']  

        if username:
            self.username.setText(username) # set username in the dashboard
        else:
            self.username.setText("Unknown User") # set username in the dashboard

        self.content_window_layout = QStackedLayout(self.content_widget)

        dashboard_section = Dashboard(self) # index 0
        self.content_window_layout.addWidget(dashboard_section)

        # empty_widget = QWidget()
        # self.content_window_layout.insertWidget(0, empty_widget)

        activityLogs_section = Activity_Logs(self) # index 1
        self.content_window_layout.addWidget(activityLogs_section)

        self.accounts_section = AccountsPage(username, self) # index 2
        self.content_window_layout.addWidget(self.accounts_section)

        self.new_account_section = NewAccountPage(username, self) # index 3
        self.content_window_layout.addWidget(self.new_account_section)

        inventory_section = ItemsPage(username, self) # index 4
        self.content_window_layout.addWidget(inventory_section)

        addItem_section = NewItem(self, username) # index 5
        self.content_window_layout.addWidget(addItem_section)
        
        settings_section = settingsPage(self) # index 6
        self.content_window_layout.addWidget(settings_section)

        order_section = OrderPage(self) # index 7
        self.content_window_layout.addWidget(order_section)

        backupRestore_section = BackupRestorePage(self) # index 8
        self.content_window_layout.addWidget(backupRestore_section)

        archive_section = ArchivePage(self) # index 9
        self.content_window_layout.addWidget(archive_section)

        sales_section = SalesReportPage(self) # index 10
        self.content_window_layout.addWidget(sales_section)

        self.buttons = [
            self.dashboard_btn,
            self.activitylogs_btn,
            self.inventory_btn,
            self.accounts_btn,
            self.logout_btn,
            self.settings_btn,
            self.orders_btn,
            self.backup_btn,
            self.archive_pushButton,
            self.salesReport_pushButton
        ]

        self.dashboard_btn.clicked.connect(lambda: self.button_clicked(self.dashboard_btn, 0))
        self.activitylogs_btn.clicked.connect(lambda: self.button_clicked(self.activitylogs_btn, 1))
        self.accounts_btn.clicked.connect(lambda: self.button_clicked(self.accounts_btn, 2))
        self.inventory_btn.clicked.connect(lambda: self.button_clicked(self.inventory_btn, 4))
        self.logout_btn.clicked.connect(self.logout_btn_clicked)
        self.settings_btn.clicked.connect(lambda: self.button_clicked(self.settings_btn, 6))
        self.orders_btn.clicked.connect(lambda: self.button_clicked(self.orders_btn, 7))
        self.backup_btn.clicked.connect(lambda: self.button_clicked(self.backup_btn, 8))
        self.archive_pushButton.clicked.connect(lambda: self.button_clicked(self.archive_pushButton, 9))
        self.salesReport_pushButton.clicked.connect(lambda: self.button_clicked(self.salesReport_pushButton, 10))

        self.reportsLogs_pushButton.clicked.connect(lambda: self.show_reports_and_logs_btn())
        self.systemSettings_pushButton.clicked.connect(lambda: self.show_system_settings_btn())

        # print(f'Current index: {self.get_current_index()}')

        self.get_current_index()

        # call function to hide button once
        self.hide_buttons()

    def show_system_settings_btn(self):
        def show_buttons():
            self.settings_btn.show()
            self.backup_btn.show()

        def hide_buttons():
            self.settings_btn.hide()
            self.backup_btn.hide()

        def check_buttons_visibility():
            if not self.settings_btn.isVisible() or not self.backup_btn.isVisible():
                show_buttons()  # Show the buttons if either is not visible
            else:
                hide_buttons()  # Hide the buttons if both are already visible

        check_buttons_visibility()

    def show_reports_and_logs_btn(self):
        def show_buttons():
            print('showing reports and logs buttons')
            self.salesReport_pushButton.show()
            self.activitylogs_btn.show()

        def hide_buttons():
            print('hiding reports and logs buttons')
            self.salesReport_pushButton.hide()
            self.activitylogs_btn.hide()

        def check_buttons_visibility():
            if not self.salesReport_pushButton.isVisible() or not self.activitylogs_btn.isVisible():
                show_buttons()  # Show the buttons if either is not visible
            else:
                hide_buttons()  # Hide the buttons if both are already visible

        check_buttons_visibility()

    def hide_buttons(self):
        buttons = [
            self.salesReport_pushButton,
            self.activitylogs_btn,
            self.settings_btn,
            self.backup_btn
        ]
        for button in buttons:
            button.hide()

    def logout_btn_clicked(self):
        print("Application is closed")
        try:
            temp_data_dir = "app/resources/data/temp_user_data.json"
            if os.path.exists(temp_data_dir):
                with open(temp_data_dir, 'r') as file:
                    data = json.load(file)
                key = list(data.keys())[0]
                _id = data[key]

                print(f'Key: {key}, _id: {_id}')
                self.logs.logout(self.account_username)
                self.account_username = None

                data = {"_id": str("")}
                with open(temp_data_dir, 'w') as file:
                    json.dump(data, file, indent=4)

                self.close()
            else:
                QMessageBox.warning(self, "Error", "File not found")
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Invalid JSON in file")

    def get_current_index(self):
        return self.content_window_layout.currentIndex()
    
    def current_index_update(self):
        if self.get_current_index() == 1:
            self.frame_7.hide()
            self.comboBox.hide()
        if self.get_current_index() == 2:
            self.comboBox.hide()

            search_bar = self.searchbar
            search_bar.setPlaceholderText("Search username here")
            
            search_bar.textChanged.connect(self.search_bar_text_changed)
            
        else:
            self.frame_7.show()
            self.comboBox.show()
            self.searchbar.setPlaceholderText("Type here...")

    def search_bar_text_changed(self, text):
        print(f"Search bar text changed to: {text}")
        # pause thread update
        if text:  # if search text is not empty
            self.accounts_section.timer.timeout.connect(self.accounts_section.update_all)
            self.accounts_section.timer.stop()
            # clear table
            self.accounts_section.tableWidget.setRowCount(0)

            search_results = self.collection.find({
                "$or": [
                    {"username": {"$regex": "^" + text, "$options": "i"}}
                    # {"first_name": {"$regex": "^" + text, "$options": "i"}},
                    # {"last_name": {"$regex": "^" + text, "$options": "i"}}
                ]
            })

            if search_results:
                # convert the search results to a list
                results_list = list(search_results)

                # automatically print the result when the text is changed
                for result in results_list:
                    print(f"Username: {result['username']}, First Name: {result['first_name']}, Last Name: {result['last_name']}, Job: {result['job']}, User Type: {result['user_type']}, account status: {result['status']}")

                table = self.accounts_section.tableWidget
                column_count = table.columnCount()

                header_labels = []
                for i in range(column_count):
                    item = table.horizontalHeaderItem(i)
                    if item is not None:
                        header_labels.append(item.text())
                header_labels = [self.clean_key(label) for label in header_labels]

                keys = set()
                for item in results_list:
                    keys.update(self.clean_key(key) for key in item.keys())

                # Find the maximum number of keys across all documents
                max_column_count = max(len(item.keys()) for item in results_list) if results_list else 0

                # Set table dimensions
                table.setRowCount(len(results_list))
                table.setColumnCount(max_column_count)

                # Populate table with data
                for row, item in enumerate(results_list):
                    for column, key in enumerate(header_labels):
                        original_keys = [k for k in item.keys() if self.clean_key(k) == key]
                        original_key = original_keys[0] if original_keys else None
                        value = item.get(original_key)
                        table.setItem(row, column, QTableWidgetItem(str(value)))
            else:
                # If no results, keep the table headers and clear the rows
                table = self.accounts_section.tableWidget
                table.setRowCount(0)
        else:  # if search text is empty, populate table with original data
            self.accounts_section.timer.timeout.connect(self.accounts_section.update_all)
            self.accounts_section.timer.start()
            self.accounts_section.update_table()
            
    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def button_clicked(self, button, index):
        self.reset_button_styles()
        self.set_active_button_style(button)
        if index is not None:
            self.content_window_layout.setCurrentIndex(index)
            print(f'Current Index: {self.get_current_index()}')
            self.current_index_update()
        else:
            print(f"{button.objectName()} button clicked.")

    def reset_button_styles(self):
        for button in self.buttons:
            button.setStyleSheet("""
            QPushButton {
                color: #9E9BB9;
                border: none;
                padding: 10px 0;
                    font: 10pt "Inter";
                text-align:left;
            }
            QPushButton:hover { 
                color: #0D044E;
                border: none;
                padding: 10px 0;
                    font: 10pt "Inter";
            }	
        """)
            
    def set_active_button_style(self, button):
        button.setStyleSheet("""
            QPushButton{
                color: #0D044E;
                border: none;
                padding: 10px 0;
                    font: 10pt "Inter";
            }          
        """)