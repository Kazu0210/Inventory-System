from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
import pymongo
# from ui.employee.profilePage import Ui_Form as profile_page
from ui.NEW.employee.profile import Ui_Form as Ui_profile_page

class ProfilePage(QWidget, Ui_profile_page):
    def __init__(self, username, dashboard_mainWindow=None):
        super().__init__()
        self.setupUi(self)
        self.dashboard_mainWindow = dashboard_mainWindow
        self.username = username  # Store the username for use in methods

        # button connections
        self.updateProfile_pushButton.clicked.connect(lambda: print('Update User Information button clicked'))
        self.updatePassword_pushButton.clicked.connect(lambda: print('Update Password button clicked'))

        self.setInformation()

    def setInformation(self):
        try:
            document = self.connect_to_db("accounts").find_one({'username': self.username})
        except Exception as e:
            print(f"Error: {e}")

        if document:
            # Update UI labels with document data
            self.fullname_label.setText(f"{document.get('last_name')}, {document.get('first_name')}")
            self.username_label.setText(document.get('username', ''))
            self.email_label.setText(document.get('email', ''))
            self.accountRole_label.setText(document.get('user_type'))
            self.accountStatus_label.setText(document.get('status'))
            self.accountID_label.setText(document.get('account_id', ''))
            self.address_label.setText(document.get('address', ''))
            self.lastLogin_label.setText(document.get('last_login', ''))
        else:
            QMessageBox.warning(self, "User Not Found", "The user information could not be found.")

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]