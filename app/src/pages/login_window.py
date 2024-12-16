from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# from ui.with_design.login_mainWindow import Ui_login_mainWindow as login_mainWindow
from ui.final_ui.login_window import Ui_MainWindow as login_mainWindow

from utils.Hashpassword import HashPassword
from utils.Activity_logs import Activity_Logs
from employee_account.dashboard import employee_dashboard
from pages.admin.main_window import MainWindow
from utils.create_default_admin import createDefaultAdmin

from pages.employee.main_window import MainWindow as employee_mainWindow
import pymongo
import json

class loginWindow(QMainWindow, login_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.logs = Activity_Logs()
        self.login_pushButton.clicked.connect(self.LoginBtn_clicked)

        self.defaultAdmin = createDefaultAdmin()
        self.defaultAdmin

        self.set_system_logo()

    def set_system_logo(self):
        """Set System Logo in the main window with minimum and maximum height"""
        logo = QPixmap("app/resources/icons/system-icon.png")
        
        min_height = 180  # Minimum height
        max_height = 200  # Maximum height

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
        # check if the account is inactive
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
            self.logs.login_attempt_failed(f"Login failed: {username} account is inactive")
            QMessageBox.warning(
                self,
                "Login Attempt Failed",
                "Your account is inactive. Please contact the admin to reactivate your account.",
            )
        elif self.is_account_pending():
            self.logs.login_attempt_failed(f"Login failed: {username} account is pending")
            QMessageBox.warning(
                self,
                "Login Attempt Failed",
                "Your account is pending. Please contact the admin to activate your account.",
            )
        elif self.is_account_blocked():
            self.logs.login_attempt_failed(f"Login failed: {username} account is blocked")
            QMessageBox.warning(
                self,
                "Login Attempt Failed",
                "Your account is blocked. Please contact the admin to unblock your account.",
            )
        else:
            user_role = self.validate_credentials(username, password)
            if user_role:
                self.logs.login_attempt_success(username)
                self.close()

                if user_role == 'Admin':
                    print('User is an admin')
                    self.admin_dashboard = MainWindow(username)
                    self.admin_dashboard.show()

                elif user_role == 'Employee':
                    print('User is an employee')
                    self.employee_dashboard = employee_mainWindow(username)
                    self.employee_dashboard.show()
            else:
                self.logs.login_attempt_failed(username)
                QMessageBox.warning(
                    self,
                    "Login Attempt Failed",
                    "Invalid username or password. Please try again.",
                )

    def default_admin_login(self, username, password):
        print('logging in default admin account.')

        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = client["LPGTrading_DB"]
        collection = db["default_account"]

        document = collection.find_one({"username": username})
        if document:
            if document["password"] == password:
                self.main_window = MainWindow(username)
                self.main_window.show()
                self.close()
            else:
                admin_dialog = QDialog(self)
                admin_dialog.setWindowTitle("Default Admin")
                admin_dialog.setModal(True)

                admin_label = QLabel("Wrong password", admin_dialog)


    def validate_credentials(self, username, password):
        if not username or not password:
            return False
        
        if username == "admin":
            self.default_admin_login(username, password)
            return True

        collection = self.connect_to_db('accounts')

        document = collection.find_one({"username": username})

        if document:
            hashed_password = HashPassword(password)
            if hashed_password.verify_password(document['password']):
                print("Password correct")
                self.save_user_id(document['_id'])

                user_type = document.get('user_type')
                if user_type == "Admin":
                    return 'Admin'
                elif user_type == "Employee":
                    return 'Employee'
            else:
                print("Incorrect password")
        else:
            print("User not found in the database")
        return False

    def save_user_id(self, user_id):
        temp_data_dir = "app/resources/data/temp_user_data.json"
        data = {"_id": str(user_id)}

        try:
            with open(temp_data_dir, 'w') as file:
                json.dump(data, file, indent=4)
            print('_id saved successfully')
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saving user ID: {e}")
            
    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = client["LPGTrading_DB"]

        return db[collection_name]