from PyQt6.QtWidgets import *
from ui.with_design.login_mainWindow import Ui_login_mainWindow as login_mainWindow
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
        self.login_btn.clicked.connect(self.LoginBtn_clicked)

        self.defaultAdmin = createDefaultAdmin()
        self.defaultAdmin

    def LoginBtn_clicked(self):
        self.login_attempt()
        self.username.clear()
        self.password.clear()

    def login_attempt(self):
        username = self.username.text().strip()
        password = self.password.text().strip()

        user_role = self.validate_credentials(username, password)
        if user_role:
            self.logs.login_attempt_success(username)
            self.close()

            if user_role == 'Admin':
                print('User is an admin')
                self.main_window = MainWindow(username)
                self.main_window.show()
            elif user_role == 'Employee':
                print('User is an employee')
                self.employee_dashboard = employee_mainWindow(username)
                self.employee_dashboard.show()
        else:
            self.logs.login_attempt_failed(username)
            self.show_login_fail_dialog()

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

    def show_login_fail_dialog(self):
        login_fail_dialog = QDialog(self)
        login_fail_dialog.setWindowTitle("Login Failed")
        login_fail_dialog.setModal(True)

        label = QLabel("Invalid username or password", login_fail_dialog)
        login_fail_dialog.exec()

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = client["LPGTrading_DB"]
        collection = db[collection_name]

        client.close()

        return collection