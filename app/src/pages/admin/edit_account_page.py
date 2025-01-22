from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt
from src.ui.NEW.edit_account_page import Ui_Form as edit_account_page_Ui
from src.utils.Hashpassword import HashPassword
from src.utils.dir import ConfigPaths
import sys, pymongo, json, os

class editAccountPage(QWidget, edit_account_page_Ui):
    def __init__(self, account_id=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # initialize config patt
        self.directory = ConfigPaths()

        self.cancel_btn.clicked.connect(lambda: self.cancel_btn_clicked())
        self.save_btn.clicked.connect(lambda: self.save_btn_clicked())

        self.account_id = account_id
        print(f"ACCOUNT ID FROM EDIT ACCOUNT PAGE: {self.account_id}")

        self.collection = self.connect_to_db()

        self.set_text_on_form() # call function to set text on every field
        self.settings_dir = self.directory.get_path('filters')

        filter_filename = "filters.json" # directory file name
        self.update_combo_box(filter_filename)

    def get_data(self):
        data = {
            "account_id": self.accountID_label.text().strip(),
            "username": self.username_field.text().strip(),
            "email": self.email_field.text().strip(),
            "first_name": self.fname_field.text().strip(),
            "last_name": self.lname_field.text().strip(),
            "address": self.address_field.text().strip(),
            "password": self.password_field.text().strip(),
            "user_type": self.usertype_comboBox.currentText(),
            "job": self.job_comboBox.currentText(),
            "status": self.status_comboBox.currentText()
        }
        return data
    
    def save(self, data):
        try:
            self.collection.update_one({"account_id": self.account_id}, {"$set": data}) # save new data
            self.close()
            # NEED TO ADD ACTIVITY LOGS
        except:
            print("Error saving data to database")

    def save_btn_clicked(self):
        data = self.get_data() # get data from all the field
        print(f"DATA: {data}")       

        if not data["password"]:
            data.pop("password")
        else:
            hasher = HashPassword(data['password']) # HashPassword instance
            hashed_password = hasher.hash_password() # hashed password
            data['password'] = hashed_password # store hashed password

        self.save(data)

    def update_combo_box(self, filter_filename):
        self.add_comboBox_options(filter_filename, self.usertype_comboBox, "role")
        self.add_comboBox_options(filter_filename, self.job_comboBox, "job")
        self.add_comboBox_options(filter_filename, self.status_comboBox, "account_status")

    def add_comboBox_options(self, directory_name, comboBox_name, option_name):
        base_dir = os.path.abspath(os.getcwd())
        filter_dir = f"{base_dir}/../app/resources/config/{directory_name}"

        with open(filter_dir, 'r') as f:
            options = json.load(f)

        for option in options[option_name]:
            if list(option.values())[0] != "Show All":
                comboBox_name.addItem(list(option.values())[0])
            if list(option.values())[0] == "Show All":
                comboBox_name.addItem(" ")
                
    def update_comboBox(self):
        self.usertype_filter()

    def usertype_filter(self):
        with open(self.settings_dir, 'r') as f:
            data = json.load(f)

        self.usertype_comboBox.clear()
        for usertype in data['role']:
            self.usertype_comboBox.addItem(list(usertype.values())[0])

    def set_text_on_form(self):
        account_data = self.collection.find_one({"account_id": self.account_id})
        if account_data:
            self.accountID_label.setText(str(account_data["account_id"]))
            self.username_field.setText(str(account_data['username']))
            self.email_field.setText(str(account_data['email']))
            self.fname_field.setText(str(account_data['first_name']))
            self.lname_field.setText(str(account_data['last_name']))
            self.address_field.setText(str(account_data['address']))
            self.usertype_comboBox.addItem(str(account_data['user_type']))
            self.job_comboBox.addItem(str(account_data['job']))
            self.status_comboBox.addItem(str(account_data['status']))

    def connect_to_db(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = "accounts"
        return client[db][collection_name]

    def cancel_btn_clicked(self):
        self.close()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = editAccountPage(None)
    window.show()
    sys.exit(app.exec())