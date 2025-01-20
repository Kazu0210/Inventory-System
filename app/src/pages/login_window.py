from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

from src.ui.login_window import Ui_MainWindow as login_mainWindow

from src.utils.Hashpassword import HashPassword
from src.utils.Activity_logs import Activity_Logs
from src.utils.Logs import Logs
from src.custom_widgets.message_box import CustomMessageBox
from src.utils.create_default_admin import createDefaultAdmin
from src.utils.dir import ConfigPaths

from src.pages.admin.main_window import MainWindow
from src.pages.splash_screen import SplashScreen

from src.pages.employee.main_window import MainWindow as employee_mainWindow

import pymongo

class loginWindow(QMainWindow, login_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logs = Logs() # activity logs
        self.dirs = ConfigPaths() # initialize config paths
        self.login_pushButton.clicked.connect(self.LoginBtn_clicked)
        self.defaultAdmin = createDefaultAdmin() # create default admin account
        self.set_system_logo()

    def set_button_icon(self, button, icon_path):
        icon = QPixmap(icon_path)
        button.setIcon(QIcon(icon))

    def set_system_logo(self):
        """Set System Logo in the main window with minimum and maximum height"""
        logo = QPixmap(self.dirs.get_path('system_icon'))
        min_height = 180  # Minimum height
        max_height = 200  # Maximum height
        current_height = self.logo.height()
        height_to_use = max(min_height, min(max_height, current_height))
        scaled_logo = logo.scaledToHeight(height_to_use, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(scaled_logo)
        self.logo.setScaledContents(True)

    def LoginBtn_clicked(self):
        self.login_attempt()
        self.username_lineEdit.clear()
        self.password_lineEdit.clear()

    def is_account_pending(self):
        username = self.username_lineEdit.text().strip()
        data = self.connect_to_db('accounts').find_one({"username": username})
        try:
            if data['status'] == 'Pending':
                return True
            else:
                return False  
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_account_inactive(self):
        # check if the account is inactive
        username = self.username_lineEdit.text().strip()
        data = self.connect_to_db('accounts').find_one({"username": username})

        try:
            if data['status'] == 'Inactive':
                return True
            else:
                return False  
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_account_blocked(self):
        username = self.username_lineEdit.text().strip()
        data = self.connect_to_db('accounts').find_one({"username": username})
        try:
            if data['status'] == 'Blocked':
                return True
            else:
                return False  
        except Exception as e:
            print(f"An error occurred: {e}")

    def login_attempt(self):
        username = self.username_lineEdit.text().strip()
        password = self.password_lineEdit.text().strip()
        if self.is_account_inactive():
            self.logs.record_log(username=username,event="account_inactive")
            CustomMessageBox.show_message('warning','Login Attempt Failed',"Your account is inactive. Please contact the admin to reactivate your account.")
        elif self.is_account_pending():
            self.logs.record_log(username=username,event="account_pending")
            CustomMessageBox.show_message('warning','Login Attempt Failed',"Your account is pending. Please contact the admin to activate your account.")
        elif self.is_account_blocked():
            self.logs.record_log(username=username,event="account_blocked")
            CustomMessageBox.show_message('warning','Login Attempt Failed',"Your account is blocked. Please contact the admin to unblock your account.")
        else:
            user_role = self.validate_credentials(username,password)
            if user_role:
                self.logs.record_log(username=username,event="user_login_success")
                if user_role == 'Admin':
                    self.admin_dashboard = MainWindow(username)
                    self.admin_dashboard.show()
                    self.close()
                elif user_role == 'Employee':
                    self.employee_dashboard = employee_mainWindow(username)
                    self.employee_dashboard.show()
                    self.close()
            else:
                self.logs.record_log(username=username,event='login_failed')
                CustomMessageBox.show_message('warning','Login Attempt Failed',"Invalid username or password. Please try again.")   

    def default_admin_login(self, username, password):
        document = self.connect_to_db('default_account').find_one({"username": username})
        if document:
            if document["password"] == password:
                self.logs.record_log(username=username, event='default_admin_login_success')
                self.main_window = MainWindow(username)
                self.main_window.show()
                self.close()
            else:
                self.logs.record_log(username=username, event="default_admin_login_failed")
                admin_dialog = QDialog(self)
                admin_dialog.setWindowTitle("Default Admin")
                admin_dialog.setModal(True)

    def validate_credentials(self,username,password):
        if not username or not password:
            return False

        if username=="admin":
            self.default_admin_login(username,password)
            return True

        collection=self.connect_to_db('accounts')
        document=collection.find_one({"username":username})

        if document:
            hashed_password=HashPassword(password)
            if hashed_password.verify_password(document['password']):
                user_type=document.get('user_type')
                if user_type=="Admin":
                    return 'Admin'
                elif user_type=="Employee":
                    return 'Employee'
            else:
                print("Incorrect password")
        else:
            print("User not found in the database")
        return False
                
    def connect_to_db(self,collection_name):
        connection_string="mongodb://localhost:27017/"
        client=pymongo.MongoClient(connection_string)
        db=client["LPGTrading_DB"]
        return db[collection_name]