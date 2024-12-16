from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap

# from ui.main_window import Ui_MainWindow
from ui.final_ui.main_window import Ui_MainWindow

from pages.admin.activity_logs import Activity_Logs
from pages.admin.accountsPage import AccountsPage
# from accountsPage import UpdateThread
# from newEmployee_page import newEmployeePage
from pages.admin.dashboard_page import Dashboard
from pages.admin.itemsPage import ItemsPage
from pages.admin.newitemsPage import newItem_page as NewItem
from pymongo import MongoClient

from utils.Activity_logs import Activity_Logs as activity_logs
from utils.Graphics import AddGraphics

from pages.admin.settings_page import settingsPage
from pages.admin.new_account_page import NewAccountPage
from pages.admin.order_page import OrderPage
from pages.admin.backp_restore import BackupRestorePage
from pages.admin.archive_page import ArchivePage
from pages.admin.sales_report_page import SalesReportPage
from pages.admin.prices_page import PricesPage
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

        try:
            if username:
                self.username.setText(username) # set username in the dashboard
            else:
                self.username.setText("Unknown User") # set username in the dashboard
        except Exception as e:
            print(e)

        self.content_window_layout = QStackedLayout(self.content_widget)

        dashboard_section = Dashboard(username, self) # index 0
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

        # addItem_section = NewItem(self, username) # index 5
        # self.content_window_layout.addWidget(addItem_section)
        
        settings_section = settingsPage(self) # index 5
        self.content_window_layout.addWidget(settings_section)

        order_section = OrderPage(self) # index 6
        self.content_window_layout.addWidget(order_section)

        backupRestore_section = BackupRestorePage(self) # index 7
        self.content_window_layout.addWidget(backupRestore_section)

        archive_section = ArchivePage(self) # index 8
        self.content_window_layout.addWidget(archive_section)

        sales_section = SalesReportPage(self) # index 9
        self.content_window_layout.addWidget(sales_section)

        price_section = PricesPage(self) # index 10
        self.content_window_layout.addWidget(price_section)

        self.buttons = [
            self.dashboard_pushButton,
            self.activityLogs_pushButton,
            self.inventory_pushButton,
            self.accounts_pushButton,
            self.logout_pushButton,
            self.settings_pushButton,
            self.orders_pushButton,
            self.backupRestore_pushButton,
            self.archive_pushButton,
            self.salesReport_pushButton,
            self.prices_pushButton
        ]

        self.parent_widgets = [
            self.frame_4, 
            self.frame_10,
            self.frame_15,
            self.frame_6,
            self.frame_12,
            self.frame_7,
            self.frame_13,
            self.frame_14,
            self.frame_9,
            self.frame_5
        ]

        self.dashboard_pushButton.clicked.connect(lambda: self.button_clicked(self.dashboard_logo, self.frame_4, self.dashboard_pushButton, 0))
        self.activityLogs_pushButton.clicked.connect(lambda: self.button_clicked(self.activity_logs_logo, self.frame_10, self.activityLogs_pushButton, 1))
        self.accounts_pushButton.clicked.connect(lambda: self.button_clicked(self.accounts_logo, self.frame_15, self.accounts_pushButton, 2))
        self.inventory_pushButton.clicked.connect(lambda: self.button_clicked(self.inventory_logo, self.frame_6, self.inventory_pushButton, 4))
        self.logout_pushButton.clicked.connect(self.logout_btn_clicked)
        self.settings_pushButton.clicked.connect(lambda: self.button_clicked(self.settings_logo, self.frame_12, self.settings_pushButton, 5))
        self.orders_pushButton.clicked.connect(lambda: self.button_clicked(self.orders_logo, self.frame_7, self.orders_pushButton, 6))
        self.backupRestore_pushButton.clicked.connect(lambda: self.button_clicked(self.backup_restore_logo, self.frame_13, self.backupRestore_pushButton, 7))
        self.archive_pushButton.clicked.connect(lambda: self.button_clicked(self.archive_logo, self.frame_14, self.archive_pushButton, 8))
        self.salesReport_pushButton.clicked.connect(lambda: self.button_clicked(self.sales_report_logo, self.frame_9, self.salesReport_pushButton, 9))
        self.prices_pushButton.clicked.connect(lambda: self.button_clicked(self.prices_logo, self.frame_5, self.prices_pushButton, 10))

        self.reportsLogs_pushButton.clicked.connect(lambda: self.show_reports_and_logs_btn())
        self.systemSettings_pushButton.clicked.connect(lambda: self.show_system_settings_btn())

        # print(f'Current index: {self.get_current_index()}')

        self.get_current_index()

        # call function to hide button once
        self.hide_buttons()

        self.add_graphics()

    def add_graphics(self):
        """Add graphics to widgets (shadows, icons, others effects etc.)"""
        
        self.set_btn_icons()

        self.set_system_logo()

        graphics = AddGraphics()
        graphics.shadow_effect(self.frame, blur=10, x=-4, y=4, alpha=50)

    def set_system_logo(self):
        """Set System Logo in the main window with minimum and maximum height"""
        logo = QPixmap("app/resources/icons/system-icon.png")
        
        min_height = 150  # Minimum height
        max_height = 180  # Maximum height

        # Calculate the height of the QLabel
        current_height = self.logo.height()

        # Ensure the height stays within the defined range
        height_to_use = max(min_height, min(max_height, current_height))

        # Scale the pixmap to the computed height while maintaining aspect ratio
        scaled_logo = logo.scaledToHeight(height_to_use, Qt.TransformationMode.SmoothTransformation)

        # Set the scaled pixmap to the QLabel
        self.logo.setPixmap(scaled_logo)

        # Ensure the QLabel does not distort the pixmap
        self.logo.setScaledContents(True)

    def set_btn_icons(self):
        """Set icons for the buttons"""
        dashboard_icon = QPixmap("app/resources/icons/black-theme/dashboard.png")
        self.dashboard_logo.file_name = os.path.basename("app/resources/icons/black-theme/dashboard.png")
        self.dashboard_logo.setPixmap(dashboard_icon)
        self.dashboard_logo.setScaledContents(True)

        prices_icon = QPixmap("app/resources/icons/black-theme/price-tag.png")
        self.prices_logo.file_name = os.path.basename("app/resources/icons/black-theme/price-tag.png")
        self.prices_logo.setPixmap(prices_icon)
        self.prices_logo.setScaledContents(True)

        inventory_icon = QPixmap("app/resources/icons/black-theme/inventory.png")
        self.inventory_logo.file_name = os.path.basename("app/resources/icons/black-theme/inventory.png")
        self.inventory_logo.setPixmap(inventory_icon)
        self.inventory_logo.setScaledContents(True)

        orders_icon = QPixmap("app/resources/icons/black-theme/booking.png")
        self.orders_logo.file_name = os.path.basename("app/resources/icons/black-theme/booking.png")
        self.orders_logo.setPixmap(orders_icon)
        self.orders_logo.setScaledContents(True)

        reportsLogs_icon = QPixmap("app/resources/icons/black-theme/file.png")
        self.reports_logs_logo.file_name = os.path.basename("app/resources/icons/black-theme/file.png")
        self.reports_logs_logo.setPixmap(reportsLogs_icon)
        self.reports_logs_logo.setScaledContents(True)
        
        sales_icon = QPixmap("app/resources/icons/black-theme/sales.png")
        self.sales_report_logo.file_name = os.path.basename("app/resources/icons/black-theme/sales.png")
        self.sales_report_logo.setPixmap(sales_icon)
        self.sales_report_logo.setScaledContents(True)
        
        act_logs_icon = QPixmap("app/resources/icons/black-theme/restore.png")
        self.activity_logs_logo.file_name = os.path.basename("app/resources/icons/black-theme/restore.png")
        self.activity_logs_logo.setPixmap(act_logs_icon)
        self.activity_logs_logo.setScaledContents(True)
        
        system_udpate_icon = QPixmap("app/resources/icons/black-theme/system-update.png")
        self.system_settings_logo.file_name = os.path.basename("app/resources/icons/black-theme/system-update.png")
        self.system_settings_logo.setPixmap(system_udpate_icon)
        self.system_settings_logo.setScaledContents(True)
        
        setting_icon = QPixmap("app/resources/icons/black-theme/settings.png")
        self.settings_logo.file_name = os.path.basename("app/resources/icons/black-theme/settings.png")
        self.settings_logo.setPixmap(setting_icon)
        self.settings_logo.setScaledContents(True)

        backup_restore_icon = QPixmap("app/resources/icons/black-theme/database.png")
        self.backup_restore_logo.file_name = os.path.basename("app/resources/icons/black-theme/database.png")
        self.backup_restore_logo.setPixmap(backup_restore_icon)
        self.backup_restore_logo.setScaledContents(True)
        
        archive_icon = QPixmap("app/resources/icons/black-theme/archive.png")
        self.archive_logo.file_name = os.path.basename("app/resources/icons/black-theme/archive.png")
        self.archive_logo.setPixmap(archive_icon)
        self.archive_logo.setScaledContents(True)

        accounts_icon = QPixmap("app/resources/icons/black-theme/user.png")
        self.accounts_logo.file_name = os.path.basename("app/resources/icons/black-theme/user.png")
        self.accounts_logo.setPixmap(accounts_icon)
        self.accounts_logo.setScaledContents(True)
        
        logout_icon = QPixmap("app/resources/icons/black-theme/logout.png")
        self.logout_logo.file_name = os.path.basename("app/resources/icons/black-theme/logout.png")
        self.logout_logo.setPixmap(logout_icon)
        self.logout_logo.setScaledContents(True)

    def show_system_settings_btn(self):
        def show_buttons():
            self.frame_12.show() # settings button frame
            self.frame_13.show() # backup and restore button frame

        def hide_buttons():
            self.frame_12.hide()
            self.frame_13.hide()

        def check_buttons_visibility():
            if not self.frame_12.isVisible() or not self.frame_13.isVisible():
                show_buttons()  # Show the buttons if either is not visible
            else:
                hide_buttons()  # Hide the buttons if both are already visible

        check_buttons_visibility()

    def show_reports_and_logs_btn(self):
        def show_buttons():
            print('showing reports and logs buttons')
            self.frame_9.show()
            self.frame_10.show()

        def hide_buttons():
            print('hiding reports and logs buttons')
            self.frame_9.hide()
            self.frame_10.hide()

        def check_buttons_visibility():
            if not self.frame_9.isVisible() or not self.frame_10.isVisible():
                show_buttons()  # Show the buttons if either is not visible
            else:
                hide_buttons()  # Hide the buttons if both are already visible

        check_buttons_visibility()

    def hide_buttons(self):
        buttons = [
            self.frame_9, # sales report button frame
            self.frame_10, # activity logs button frame
            self.frame_12, # settings button frame
            self.frame_13 # backup restore button frame
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

    def button_clicked(self, icon_widget, parent_widget, button, index):
        self.reset_button_styles()
        self.reset_parent_widget()
        self.reset_icon()
        self.set_active_icon(icon_widget)
        self.set_active_button_style(button)
        self.set_active_frame_style(parent_widget)
        if index is not None:
            self.content_window_layout.setCurrentIndex(index)
            print(f'Current Index: {self.get_current_index()}')
            # self.current_index_update()
        else:
            print(f"{button.objectName()} button clicked.")

    def reset_button_styles(self):
        for button in self.buttons:
            button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
            QPushButton:hover { 
                background-color: #A8D5BA;
                color: #000;
            }	
        """)
    
    def reset_parent_widget(self):
        for widget in self.parent_widgets:
            widget.setStyleSheet("""
            QFrame{
                background-color: transparent;
            }
            QFrame:hover{
                background-color: #A8D5BA;
            }
            """)

    def reset_icon(self):
        self.set_btn_icons()

    def set_active_icon(self, icon_widget):
        # print(f"Icon widget's file name: {icon_widget.file_name}")
        file_name = icon_widget.file_name

        file_path = f"app/resources/icons/{file_name}"
        icon = QPixmap(file_path)
        icon_widget.file_name = os.path.basename(file_path)
        icon_widget.setPixmap(icon)
        icon_widget.setScaledContents(True)

    def set_active_frame_style(self, parent_widget):
        parent_widget.setStyleSheet("""
            QFrame{
                color: #fff;
                background-color: #228B22;
            }
        """)
            
    def set_active_button_style(self, button):
        button.setStyleSheet("""
            QPushButton{
                color: #fff;
                background-color: #228B22;
            }
        """)