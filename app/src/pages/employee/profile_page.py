from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QStringConverter

from utils.Inventory_Monitor import InventoryMonitor
from utils.Hashpassword import HashPassword
from utils.Validation import Validator

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
        self.updateProfile_pushButton.clicked.connect(lambda: self.show_update_profile_form()) # show update profile form
        self.updatePassword_pushButton.clicked.connect(lambda: self.show_update_pass_form()) # show password form
        self.cancel_update_pushButton.clicked.connect(lambda: self.hide_update_profile_form()) # cancel update profile info
        self.cancel_password_pushButton.clicked.connect(lambda: self.cancel_password_clicked()) # cancel create password
        self.updatePass_pushButton.clicked.connect(lambda: self.save_new_password()) # save new password
        self.update_pushButton.clicked.connect(lambda: self.save_user_info()) # save new user info

        self.display_user_info()
        self.hide_update_profile_form()
        self.hide_update_pass_form()

        # Initialize Monitor for account collection
        monitor = InventoryMonitor('accounts')
        monitor.start_listener_in_background()
        monitor.data_changed_signal.connect(self.display_user_info)

        # Set validator instance
        validator = Validator()
    
    def save_new_password(self):
        # Get the new password from the input field

        # check if password field is empty
        if not self.isPasswordEmpty():
            print(f'password field is not empty')
            raw_password = self.password_lineEdit.text().strip()
            print(f"New password: {raw_password}")

            hasher = HashPassword(raw_password)
            hashed_password = hasher.hash_password()

            current_document = self.connect_to_db('accounts').find_one({'username': self.username})
            if not current_document:
                QMessageBox.warning(self, "User Not Found", "The current user does not exist in the database.")
                return
            
            try:
                # Fetch the current user document for comparison
                current_document = self.connect_to_db('accounts').find_one({'username': self.username})
                if not current_document:
                    QMessageBox.warning(self, "User Not Found", "The current user does not exist in the database.")
                    return

                # Update the current user's document in the collection using the stored username
                result = self.connect_to_db('accounts').update_one({'username': self.username}, {'$set': {'password': hashed_password}})

                if result.modified_count > 0:
                    QMessageBox.information(self, "Update Password Successful", "Password updated successfully.")
    
                    self.password_lineEdit.clear() # clear password field
                    self.hide_update_pass_form() # hide form
                else:
                    QMessageBox.warning(self, "No Changes", "No changes were made to the user information.")
            except Exception as e:
                print(f"Error updating document: {e}")
                QMessageBox.critical(self, "Update Error", "Failed to update password in the database.")

        else:
            QMessageBox.warning(
                self,
                "Update Password",
                "Password field is empty. Please enter a new password.",
            )

    def show_update_pass_form(self):
        self.update_pass_form.show()

    def isPasswordEmpty(self):
        if self.password_lineEdit.text().strip():
            return False
        else:
            return True
        
    def cancel_password_clicked(self):
        if self.isPasswordEmpty():
            print('password field is empty')
            self.password_lineEdit.clear() # clear password field
            self.hide_update_pass_form() # hide update password form
        else:
            print('password field is not empty')
            reply = QMessageBox.question(
                self,
                'Update Password',
                'Are you sure you want to cancel the update password process?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.password_lineEdit.clear() # clear password field
                self.hide_update_pass_form() # hide update password form
            else:
                print('update password process not cancelled')

    def hide_update_pass_form(self):
        self.update_pass_form.hide()

    def isFormClear(self):
        lineEdits = [
            self.fname_lineEdit,
            self.lname_lineEdit,
            self.email_lineEdit,
            self.address_lineEdit,
            self.username_lineEdit
        ]
        for lineEdit in lineEdits:
            if lineEdit.text():
                return False
        return True
    
    def clearForm(self):
        lineEdits = [
            self.fname_lineEdit,
            self.lname_lineEdit,
            self.email_lineEdit,
            self.address_lineEdit,
            self.username_lineEdit
        ]
        for lineEdit in lineEdits:
            lineEdit.clear()

    def hide_update_profile_form(self):
        # check if form contains input ask to save changes
        if not self.isFormClear():
            reply = QMessageBox.question(
                self, 
                'Save Changes', 
                'Do you want to save changes before closing?', 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            
            # hide form if the user clicked NO
            if reply == QMessageBox.StandardButton.No:
                self.updateProfile_form.hide()
                self.clearForm()
            else:
                # save new information
                self.save_user_info()
                self.clearForm()
        else:
            # if none hide form
            self.updateProfile_form.hide()

    def show_update_profile_form(self):
        self.fill_update_form()
        self.updateProfile_form.show()

    def display_user_info(self):
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
    
    def fill_update_form(self):
        try:
            document = self.connect_to_db("accounts").find_one({'username': self.username})
        except Exception as e:
            print(f"Error: {e}")
        if document:
            self.username_lineEdit.setText(document.get('username'))
            self.fname_lineEdit.setText(document.get('first_name'))
            self.lname_lineEdit.setText(document.get('last_name'))
            self.email_lineEdit.setText(document.get('email'))
            self.address_lineEdit.setText(document.get('address'))
        else:
            QMessageBox.warning(self, "User Not Found", "The user information could not be found.")
    
    def save_user_info(self):
        """Save the updated user information when the Save button is clicked."""
        updated_data = {
            'username': self.username_lineEdit.text().strip(),
            'email': self.email_lineEdit.text().strip(),
            'first_name': self.fname_lineEdit.text().strip(),
            'last_name': self.lname_lineEdit.text().strip(),
            'address': self.address_lineEdit.text().strip()
        }

        # Remove any fields that are empty (optional)
        updated_data = {k: v for k, v in updated_data.items() if v}

        try:
            # Fetch the current user document for comparison
            current_document = self.connect_to_db('accounts').find_one({'username': self.username})
            if not current_document:
                QMessageBox.warning(self, "User Not Found", "The current user does not exist in the database.")
                return

            # Identify which fields are different
            changes = {k: v for k, v in updated_data.items() if current_document.get(k) != v}

            if not changes:
                QMessageBox.warning(self, "No Changes", "No changes were made to the user information.")
                return

            # Update the current user's document in the collection using the stored username
            result = self.connect_to_db('accounts').update_one({'username': self.username}, {'$set': changes})
            self.username = self.username_lineEdit.text().strip() # update value of self.username

            if result.modified_count > 0:
                QMessageBox.information(self, "Update Successful", "User information updated successfully.")
 
                self.clearForm() # clear form
                self.hide_update_profile_form() # hide form
            else:
                QMessageBox.warning(self, "No Changes", "No changes were made to the user information.")
        except Exception as e:
            print(f"Error updating document: {e}")
            QMessageBox.critical(self, "Update Error", "Failed to update user information in the database.")