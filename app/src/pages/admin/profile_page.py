from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import QStringConverter, Qt, pyqtSignal

from utils.Inventory_Monitor import InventoryMonitor
from utils.Hashpassword import HashPassword
from utils.Validation import Validator

import pymongo, json

from ui.employee.profilePage import Ui_Form as profile_page
from ui.employee.update_password import Ui_Form as update_pass_page
from ui.employee.update_profile import Ui_Form as update_profile_page
# from ui.NEW.employee.profile import Ui_Form as Ui_profile_page

class UpdateProfile(QWidget, update_profile_page):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.username = username
        self.load_data()

        # button connections
        self.update_pushButton.clicked.connect(lambda: self.update_btn_clicked())    
        self.cancel_pushButton.clicked.connect(lambda: self.close())

    def update_btn_clicked(self):
        """handle clicked event of update push button"""
        
        # Get data from form
        fname = self.fname_lineEdit.text().strip()
        lname = self.lname_lineEdit.text().strip()
        address = self.address_plainTextEdit.toPlainText().strip()
        new_username = self.username_lineEdit.text().strip()
        email = self.email_lineEdit.text().strip()
        role = self.role_comboBox.currentText()
        job = self.job_comboBox.currentText()

        # Prepare the data to be updated
        data = {
            'first_name': fname,
            'last_name': lname,
            'address': address,
            'username': new_username,
            'email': email,
            'user_type': role,
            'job': job,
        }

        print(f'New profile Data: {data}')

        # Define the filter for the document to update
        filter = {
            'username': self.username
        }

        try:
            # Perform the update operation
            self.connect_to_db('accounts').update_one(filter, {'$set': data})
            print("Profile updated successfully.")
            QMessageBox.information(self, "Success", "Profile updated successfully.")
            self.close()
        except Exception as e:
            print(f'Error: {e}')

    def get_data_db(self, username):
        """get data from database using username"""
        try:
            document = list(self.connect_to_db('accounts').find({'username': username}))
            return document
        except Exception as e:
            print(f'Error: {e}')

    def load_job_filter(self, current_job):
        job_dir = "app/resources/config/filters.json"

        # Open and load the JSON file
        with open(job_dir, 'r') as f:
            data = json.load(f)

        # Clear the combo box before adding items
        self.job_comboBox.clear()

        # Add the current job as the first item, if it exists in the job list
        found_current_job = False
        for job in data['job']:
            job_value = list(job.values())[0]
            if job_value == current_job:
                self.job_comboBox.addItem(job_value)
                found_current_job = True
                break

        # Add remaining items, skipping "Default", "Show All", and the current job
        for job in data['job']:
            job_value = list(job.values())[0]
            if job_value not in ["Default", "Show All"] and job_value != current_job:
                self.job_comboBox.addItem(job_value)

        # Handle case where current_job is not found in the job list
        if not found_current_job:
            self.job_comboBox.insertItem(0, current_job)

    def load_role_filter(self, current_role):
        job_dir = "app/resources/config/filters.json"

        # Open and load the JSON file
        with open(job_dir, 'r') as f:
            data = json.load(f)

        # Clear the combo box before adding items
        self.role_comboBox.clear()

        # Add the current job as the first item, if it exists in the job list
        found_current_job = False
        for job in data['role']:
            job_value = list(job.values())[0]
            if job_value == current_role:
                self.role_comboBox.addItem(job_value)
                found_current_job = True
                break

        # Add remaining items, skipping "Default", "Show All", and the current job
        for job in data['role']:
            job_value = list(job.values())[0]
            if job_value not in ["Default", "Show All"] and job_value != current_role:
                self.role_comboBox.addItem(job_value)

        # Handle case where current_job is not found in the job list
        if not found_current_job:
            self.role_comboBox.insertItem(0, current_role)

    def load_data(self):
        """load data to line edit"""
        try:
            data = self.get_data_db(self.username)
            print(f'Retreive data from database: {data}')

            for item in data:
                fname = item.get("first_name", "")
                lname = item.get("last_name", "")
                address = item.get("address", "")
                username = item.get("username", "")
                email = item.get("email", "")
                role = item.get("user_type", "")
                job = item.get("job", "")

                self.fname_lineEdit.setText(fname)
                self.lname_lineEdit.setText(lname)
                self.address_plainTextEdit.setPlainText(address)
                self.username_lineEdit.setText(username)
                self.email_lineEdit.setText(email)
                self.load_job_filter(job)
                self.load_role_filter(role)

        except Exception as e:
            print(f'Error: {e}')

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

class UpdatePassword(QWidget, update_pass_page):
    # signals
    update_password_signal = pyqtSignal(str)

    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        print(f'received username: {username}')

        # button connections
        self.update_pushButton.clicked.connect(lambda: self.save_new_password(username))
        self.cancel_pushButton.clicked.connect(lambda: self.close())

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

    def save_new_password(self, username):
        # Get the new password from the input field

        # check if password field is empty
        if not self.isPasswordEmpty():
            print(f'password field is not empty')
            raw_password = self.new_pass_lineEdit.text().strip()
            print(f"New password: {raw_password}")

            hasher = HashPassword(raw_password)
            hashed_password = hasher.hash_password()

            current_document = self.connect_to_db('accounts').find_one({'username': username})
            if not current_document:
                QMessageBox.warning(self, "User Not Found", "The current user does not exist in the database.")
                return
            
            try:
                # Fetch the current user document for comparison
                current_document = self.connect_to_db('accounts').find_one({'username': username})
                if not current_document:
                    QMessageBox.warning(self, "User Not Found", "The current user does not exist in the database.")
                    return

                # Update the current user's document in the collection using the stored username
                result = self.connect_to_db('accounts').update_one({'username': username}, {'$set': {'password': hashed_password}})

                if result.modified_count > 0:
                    QMessageBox.information(self, "Update Password Successful", "Password updated successfully.")
    
                    self.new_pass_lineEdit.clear() # clear password field
                    self.close() # hide form
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

    def isPasswordEmpty(self):
        if self.new_pass_lineEdit.text().strip():
            return False
        else:
            return True
        
    def cancel_password_clicked(self):
        if self.isPasswordEmpty():
            print('password field is empty')
            self.new_pass_lineEdit.clear() # clear password field
            self.close() # hide update password form
        else:
            print('password field is not empty')
            reply = QMessageBox.question(
                self,
                'Update Password',
                'Are you sure you want to cancel the update password process?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.new_pass_lineEdit.clear() # clear password field
                self.close() # hide update password form
            else:
                print('update password process not cancelled')

class ProfilePage(QWidget, profile_page):
    def __init__(self, username, dashboard_mainWindow=None):
        super().__init__()
        self.setupUi(self)
        self.dashboard_mainWindow = dashboard_mainWindow
        self.username = username  # Store the username for use in methods

        # button connections
        self.changePass_pushButton.clicked.connect(lambda: self.show_update_pass_form())
        self.update_profile_pushButton.clicked.connect(lambda: self.update_profile_clicked())
        # self.updateProfile_pushButton.clicked.connect(lambda: self.show_update_profile_form()) # show update profile form
        # self.password_btn.clicked.connect(lambda: self.show_update_pass_form()) # show password form
        # self.cancel_update_pushButton.clicked.connect(lambda: self.hide_update_profile_form()) # cancel update profile info
        # self.cancel_password_pushButton.clicked.connect(lambda: self.cancel_password_clicked()) # cancel create password
        # self.updatePass_pushButton.clicked.connect(lambda: self.save_new_password()) # save new password
        # self.update_pushButton.clicked.connect(lambda: self.save_user_info()) # save new user info

        self.display_user_info()
        # self.hide_update_profile_form()
        self.hide_update_pass_form()

        # Initialize Monitor for account collection
        monitor = InventoryMonitor('accounts')
        monitor.start_listener_in_background()
        monitor.data_changed_signal.connect(self.display_user_info)

        # Set validator instance
        validator = Validator()

    def update_profile_clicked(self):
        """Handle click event for update profile button"""
        print('update profile button clicked')
        self.update_profile = UpdateProfile(self.username)
        self.update_profile.show()

    def show_update_pass_form(self):
        self.update_pass = UpdatePassword(self.username)
        self.update_pass.show()

    def hide_update_pass_form(self):
        # self.update_pass_form.hide()
        pass

    def isFormClear(self):
        # lineEdits = [
        #     self.firstname_line,
        #     self.lastname_line,
        #     self.email_line,
        #     self.address_line,
        #     self.username_line
        # ]
        # for lineEdit in lineEdits:
        #     if lineEdit.text():
        #         return False
        # return True
        pass
    
    def clearForm(self):
        # lineEdits = [
        #     self.firstname_line,
        #     self.lastname_line,
        #     self.email_line,
        #     self.address_line,
        #     self.username_line
        # ]
        # for lineEdit in lineEdits:
        #     lineEdit.clear()
        pass

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
                # self.updateProfile_form.hide()
                self.clearForm()
            else:
                # save new information
                self.save_user_info()
                self.clearForm()
        else:
            # if none hide form
            # self.updateProfile_form.hide()
            pass

    def show_update_profile_form(self):
        self.fill_update_form()
        # self.updateProfile_form.show()

    def display_user_info(self):
        try:
            document = self.connect_to_db("accounts").find_one({'username': self.username})

            fname = document.get('first_name', '')
            lname = document.get('last_name', '')
            role = document.get('user_type', '')
            job = document.get('job', '')
            status = document.get('status', '')
            address = document.get('address', '')
            username = document.get('username', '')
            email = document.get('email', '')
            account_id = document.get('account_id', '')
        except Exception as e:
            print(f"Error: {e}")

        try:
            if document:
                # Update UI labels with document data
                self.full_name_label.setText(f"{lname}, {fname}")
                self.role_job_label.setText(f"{role}| {job}")
                self.status_label.setText(status)

                self.fname_label.setText(fname)
                self.lname_label.setText(lname)
                self.address_label.setText(address)

                self.username_label.setText(username)
                self.email_label.setText(email)
                self.accountid_label.setText(account_id)
                self.role_label.setText(role)
                self.job_label.setText(job)
            else:
                QMessageBox.warning(self, "User Not Found", "The user information could not be found.")
        except Exception as e:
            print(f'Error: {e}')

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
            pass
            # self.username_lineEdit.setText(document.get('username'))
            # self.fname_lineEdit.setText(document.get('first_name'))
            # self.lname_lineEdit.setText(document.get('last_name'))
            # self.email_lineEdit.setText(document.get('email'))
            # self.address_lineEdit.setText(document.get('address'))
        else:
            # QMessageBox.warning(self, "User Not Found", "The user information could not be found.")
            pass
    
    def save_user_info(self):
        """Save the updated user information when the Save button is clicked."""
        # updated_data = {
        #     'username': self.username_lineEdit.text().strip(),
        #     'email': self.email_lineEdit.text().strip(),
        #     'first_name': self.fname_lineEdit.text().strip(),
        #     'last_name': self.lname_lineEdit.text().strip(),
        #     'address': self.address_lineEdit.text().strip()
        # }

        # Remove any fields that are empty (optional)
        try:
            updated_data = {k: v for k, v in updated_data.items() if v}
        except Exception as e:
            print(f'Error: {e}')
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
            # self.username = self.username_lineEdit.text().strip() # update value of self.username

            if result.modified_count > 0:
                QMessageBox.information(self, "Update Successful", "User information updated successfully.")
 
                self.clearForm() # clear form
                self.hide_update_profile_form() # hide form
            else:
                QMessageBox.warning(self, "No Changes", "No changes were made to the user information.")
        except Exception as e:
            print(f"Error updating document: {e}")
            QMessageBox.critical(self, "Update Error", "Failed to update user information in the database.")