from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
import pymongo
from ui.employee.profilePage import Ui_Form as profile_page

class ProfilePage(QWidget, profile_page):
    def __init__(self, username, dashboard_mainWindow=None):
        super().__init__()
        self.setupUi(self)
        self.dashboard_mainWindow = dashboard_mainWindow
        self.username = username  # Store the username for use in methods

        # Connect to MongoDB
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)

        try:
            client.admin.command('ping')
            print("Connected to MongoDB successfully.")
        except pymongo.errors.ConnectionError as e:
            print(f"Connection error: {e}")
            QMessageBox.critical(self, "Connection Error", "Failed to connect to the database.")
            return

        db = client["LPGTrading_DB"]
        self.collection = db["accounts"]

        # Fetch and display the logged-in user's information
        self.display_user_info(username)

        # Disable editing by default
        self.set_editable(False)

        # Connect buttons to their respective functions
        self.edit_btn.clicked.connect(self.enable_edit_mode)
        self.save_btn.clicked.connect(self.save_user_info)

    def display_user_info(self, username):
        try:
            # Fetch the document for the logged-in user by username
            document = self.collection.find_one({'username': username})
        except Exception as e:
            print(f"Error querying document: {e}")
            QMessageBox.critical(self, "Error", "Failed to query user information from the database.")
            return

        if document:
            # Update UI labels with document data
            self.username_label.setText(document.get('username', ''))
            self.email_label.setText(document.get('email', ''))
            self.password_label.setText(document.get('password', ''))
            self.accountID_label.setText(document.get('account_id', ''))
            self.role_label.setText(document.get('role', ''))
            self.job_label.setText(document.get('job', ''))
            self.status_label.setText(document.get('status', ''))
            self.firstname_label.setText(document.get('first_name', ''))
            self.lastname_label.setText(document.get('last_name', ''))
            self.address_label.setText(document.get('address', ''))
        else:
            QMessageBox.warning(self, "User Not Found", "The user information could not be found.")

    def set_editable(self, editable):
        """Enable or disable the line edits for editing based on the editable flag."""
        self.username_line.setEnabled(editable)
        self.email_line.setEnabled(editable)
        self.accountID_line.setEnabled(editable)
        self.role_dropdown.setEnabled(editable)
        self.job_dropdown.setEnabled(editable)
        self.status_dropdown.setEnabled(editable)
        self.firstname_line.setEnabled(editable)
        self.lastname_line.setEnabled(editable)
        self.address_line.setEnabled(editable)
        self.save_btn.setEnabled(editable)  # Save button is only enabled in edit mode

    def enable_edit_mode(self):
        """Enable the edit mode when the Edit button is clicked."""
        self.set_editable(True)
        self.save_btn.setEnabled(True)  # Enable Save button
        # Transfer label text to line edits for editing
        self.username_line.setText(self.username_label.text())
        self.email_line.setText(self.email_label.text())
        self.accountID_line.setText(self.accountID_label.text())
        self.role_dropdown.setCurrentText(self.role_label.text())
        self.job_dropdown.setCurrentText(self.job_label.text())
        self.status_dropdown.setCurrentText(self.status_label.text())
        self.firstname_line.setText(self.firstname_label.text())
        self.lastname_line.setText(self.lastname_label.text())
        self.address_line.setText(self.address_label.text())

    def save_user_info(self):
        """Save the updated user information when the Save button is clicked."""
        updated_data = {
            'username': self.username_line.text().strip(),
            'email': self.email_line.text().strip(),
            'account_id': self.accountID_line.text().strip(),
            'role': self.role_dropdown.currentText().strip(),
            'job': self.job_dropdown.currentText().strip(),
            'status': self.status_dropdown.currentText().strip(),
            'first_name': self.firstname_line.text().strip(),
            'last_name': self.lastname_line.text().strip(),
            'address': self.address_line.text().strip()
        }

        # Remove any fields that are empty (optional)
        updated_data = {k: v for k, v in updated_data.items() if v}

        try:
            # Fetch the current user document for comparison
            current_document = self.collection.find_one({'username': self.username})
            if not current_document:
                QMessageBox.warning(self, "User Not Found", "The current user does not exist in the database.")
                return

            # Identify which fields are different
            changes = {k: v for k, v in updated_data.items() if current_document.get(k) != v}

            if not changes:
                QMessageBox.warning(self, "No Changes", "No changes were made to the user information.")
                return

            # Update the current user's document in the collection using the stored username
            result = self.collection.update_one({'username': self.username}, {'$set': changes})

            if result.modified_count > 0:
                QMessageBox.information(self, "Update Successful", "User information updated successfully.")

                # Automatically update the UI with the new values without refreshing
                self.username_label.setText(updated_data.get('username', ''))
                self.email_label.setText(updated_data.get('email', ''))
                self.accountID_label.setText(updated_data.get('account_id', ''))
                self.role_label.setText(updated_data.get('role', ''))
                self.job_label.setText(updated_data.get('job', ''))
                self.status_label.setText(updated_data.get('status', ''))
                self.firstname_label.setText(updated_data.get('first_name', ''))
                self.lastname_label.setText(updated_data.get('last_name', ''))
                self.address_label.setText(updated_data.get('address', ''))

                # Disable editing after saving
                self.set_editable(False)
            else:
                QMessageBox.warning(self, "No Changes", "No changes were made to the user information.")
        except Exception as e:
            print(f"Error updating document: {e}")
            QMessageBox.critical(self, "Update Error", "Failed to update user information in the database.")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    username = 'username' 
    Form = ProfilePage(username, None)
    Form.show()
    sys.exit(app.exec())
