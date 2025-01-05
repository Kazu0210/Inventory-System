from PyQt6.QtWidgets import QWidget, QApplication, QStackedLayout, QFrame, QMessageBox
from PyQt6.QtCore import QTimer, Qt

from ui.NEW.new_account_page import Ui_Form as Ui_new_account_page

from utils.Generate_password import PasswordGenerator
from utils.Validation import Validator
from pages.admin.username_requirement_section import UsernameAccountRequirementPage
from pages.admin.emali_requirement_section import EmailAccountRequirementPage
from utils.Hashpassword import HashPassword
from utils.Activity_logs import Activity_Logs

import sys, json, time, random, pymongo, os

class NewAccountPage(QWidget, Ui_new_account_page):
    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        if username != None:
            self.account_username = username # logged in account's username

        self.validator = Validator() # validator class instance
        self.logger = Activity_Logs() # activity logs instance

        # set validation for fields
        self.validator.string_only_validator(self.fname_field)
        self.validator.string_only_validator(self.lname_field)

        filter_filename = "filters.json" # directory file name
        self.update_combo_box(filter_filename)
  
        # settings directory
        self.settings_dir = "app/resources/config/settings.json"
        with open(self.settings_dir, 'r') as f:
            setting = json.load(f)

        # generate account ID
        self.account_id = self.generate_account_id()
        print(f"Account ID: {self.account_id}")

        # set account ID on preview section
        self.accountID_preview.setText(self.account_id)

        
        self.username_minLength = setting["create_account_validation"][0]['username_min_lenght']
        self.username_maxLength = setting["create_account_validation"][1]['username_max_lenght']

        self.username_field.textChanged.connect(lambda: self.username_validation_labels())
        self.email_field.textChanged.connect(lambda: self.email_validation_label())

        self.generatePassword_checkBox.stateChanged.connect(self.generate_password) # generate password when checkbox state changed

        # update preview labels when done typing on text field
        self.username_field.textChanged.connect(lambda: self.update_preview(self.username_field, label_name=self.username_preview))
        self.email_field.textChanged.connect(lambda: self.update_preview(self.email_field, label_name=self.email_preview))
        self.role_comboBox.currentTextChanged.connect(lambda: self.update_preview(self.role_comboBox, label_name=self.role_preview))
        self.jobTitle_comboBox.currentTextChanged.connect(lambda: self.update_preview(self.jobTitle_comboBox, label_name=self.job_preview))
        self.status_comboBox.currentTextChanged.connect(lambda: self.update_preview(self.status_comboBox, label_name=self.status_preview))
        self.fname_field.textChanged.connect(lambda: self.update_preview(self.fname_field))
        self.lname_field.textChanged.connect(lambda: self.update_preview(self.lname_field))
        self.lname_field.textChanged.connect(lambda: self.get_full_name(fname=self.fname_field.text().strip(), lname=self.lname_field.text().strip()))
        self.address_field.textChanged.connect(lambda: self.update_preview(self.address_field, label_name=self.address_preview))
        
        # BUTTONS
        self.createAcc_btn.clicked.connect(lambda: self.create_account_btn_clicked())

        self.requirement_layout = QStackedLayout(self.frame_38)

        self.empty_section = QFrame()
        self.requirement_layout.addWidget(self.empty_section) # index 0

        self.username_account_requirement_section = UsernameAccountRequirementPage(self) # index 1
        self.requirement_layout.addWidget(self.username_account_requirement_section)

        self.email_account_requirement_section = EmailAccountRequirementPage(self) # index 2
        self.requirement_layout.addWidget(self.email_account_requirement_section)

        self.username_field.mousePressEvent = self.on_username_field_clicked        
        self.email_field.mousePressEvent = self.on_email_field_clicked

    def generate_account_id(self):
        date_component = time.strftime("%Y%m%d") # get current date
        random_number = random.randint(10, 99)
        account_id = f"{date_component}{random_number}"
        
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = client["LPGTrading_DB"]
        collection = db["accounts"]
        
        while collection.find_one({"account_id": account_id}) is not None:
            random_number = random.randint(10, 99)
            account_id = f"{date_component}{random_number}"
        
        return account_id

    def create_account_btn_clicked(self):
        fields = {
            "Username": self.username_field.text().strip(),
            "First Name": self.fname_field.text().strip(),
            "Last Name": self.lname_field.text().strip(),
            "Email": self.email_field.text().strip(),
            "Password": self.password_field.text().strip(),
            "Role": self.role_comboBox.currentText().strip(),
            "Job Title": self.jobTitle_comboBox.currentText().strip(),
            "Status": self.status_comboBox.currentText().strip(),
            "Address": self.address_field.text().strip()
        }

        username = self.username_field.text().strip()
        empty_fields = [label for label, value in fields.items() if value == ""]

        if username == "":
            print("Username field is empty.")
        elif empty_fields:
            print(f"The following fields are empty: {', '.join(empty_fields)}")
        else:
            username = fields['Username']
            fname = fields['First Name'].title()
            lname = fields['Last Name'].title()
            email = fields['Email']
            password = fields['Password']
            role = fields['Role']
            job_title = fields['Job Title']
            status = fields['Status']
            address = fields['Address']
            account_id = self.account_id

            username_validator = self.validator.validate_username(username)
            email_validator = self.validator.validate_email(email)

            validator_list = [
                username_validator,
                email_validator
            ]

            if all(validator_list):
                try:
                    self.create_account(username, password, email=email, first_name=fname, last_name=lname, role=role, job_title=job_title, status=status, address=address, account_id=account_id)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
            else:
                print("Invalid username or email address.")

    def clear_form(self):
        lineEdits = [
            self.username_field,
            self.email_field,
            self.password_field,
            self.fname_field,
            self.lname_field,
            self.address_field
        ]

        for field in lineEdits:
            field.clear()

    def create_account(self, username, raw_password, **kwargs):
        # username = kwargs.get("username")
        email = kwargs.get("email")
        account_id = kwargs.get("account_id")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        role = kwargs.get("role")
        job_title = kwargs.get("job_title")
        status = kwargs.get("status")
        address = kwargs.get("address")

        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = client["LPGTrading_DB"]
        collection = db["accounts"]
        
        hasher = HashPassword(raw_password) # hashpassword class instance
        hashed_password = hasher.hash_password() # get hashed password from hashpassword instance
        print(f"Hashed password: {hashed_password}")

        data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "account_id": account_id,
            "user_type": role,
            "job": job_title,
            "status": status,
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "last_login": ""
        }      
        print(data)

        collection.insert_one(data)

        # Record to Activity Logs
        self.logger.create_account(self.account_username, username)

        # Clear Create Account Form
        self.clear_form()

        QMessageBox.information(self, "Account Created", "Account created successfully")
        self.close()

    def highlight_empty_fields(self, fields):
        for field in fields:
            field_name = getattr(self, field.lower() + "_field")
            field_name.setStyleSheet("border: 1px solid red;")
            QTimer.singleShot(3000, lambda field_name=field_name: field_name.setStyleSheet("border: none;"))

    def get_full_name(self, **kwargs):
        fname = kwargs.get('fname')
        lname = kwargs.get('lname')
        
        print(f"First name: {fname}")
        print(f"Last name: {lname}")
        print(f"sorted: {lname}, {fname}")
        full_name = f"{lname}, {fname}"
        capitalized_fullName = full_name.title() # capitalize every first letter of the name
        print(capitalized_fullName)
        self.fullName_preview.setText(capitalized_fullName)
 
    def update_combo_box(self, filter_filename):
        self.add_comboBox_options(filter_filename, self.role_comboBox, "role")
        self.add_comboBox_options(filter_filename, self.jobTitle_comboBox, "job")
        self.add_comboBox_options(filter_filename, self.status_comboBox, "account_status")

    def on_username_field_clicked(self, event):
        print("username field clicked")
        self.requirement_layout.setCurrentIndex(1)

    def on_email_field_clicked(self, event):
        print("email field clickced")
        self.requirement_layout.setCurrentIndex(2)

    def email_validation_label(self):
        email = self.email_field.text().strip()
        email_validator = self.validator.validate_email(email)
        email_requirement_section = self.email_account_requirement_section
        if email_validator:
            self.set_label_color(email_requirement_section.invalid_email_label, "green")
            email_requirement_section.invalid_email_label.setText("Valid Email")
        else:
            self.set_label_color(email_requirement_section.invalid_email_label, "red")
            email_requirement_section.invalid_email_label.setText("Invalid Email")

    def username_validation_labels(self):
        username_text = self.username_field.text().strip()

        username_uniquness = self.validator.check_username_uniqueness(username_text)
        user_requirement_section = self.username_account_requirement_section
        
        if username_uniquness:
            self.set_label_color(user_requirement_section.uniqueUser_label, "green")
        else:
            self.set_label_color(user_requirement_section.uniqueUser_label, "red")

        check_length = self.validator.check_length(username_text, self.username_minLength, self.username_maxLength)
        self.username_field.setMaxLength(self.username_maxLength)
        if check_length:
            self.set_label_color(user_requirement_section.minLength_label, "green")
        else:
            self.set_label_color(user_requirement_section.minLength_label, "red")

        has_allowed_char = self.validator.allowed_characters(username_text)
        if has_allowed_char:
            self.set_label_color(user_requirement_section.constainsChar_label, "green")
        else:
            self.set_label_color(user_requirement_section.constainsChar_label, "red")

        starts_with_letter = self.validator.first_character_is_letter(username_text)
        if starts_with_letter:
            self.set_label_color(user_requirement_section.letterFirst_label, "green")
        else:
            self.set_label_color(user_requirement_section.letterFirst_label, "red")

        no_space = self.validator.no_spaces(username_text)
        if no_space:
            self.set_label_color(user_requirement_section.noSpace_label, "green")
        else:
            self.set_label_color(user_requirement_section.noSpace_label, "red")

    def set_label_color(self, label, color):
        label.setStyleSheet(f'color:{color};')

    def capitalize_first_letter(self, field):
        print("GUMANA")
        capitalized_text = field.text().title()
        print(f"CAPITALIZED TEXT: {capitalized_text}")
        field.setText(capitalized_text)

    def update_preview(self, field_name, **kwargs):
        label_name = kwargs.get("label_name")
        field_object_name = field_name.objectName()

        if field_object_name == "fname_field":
            self.capitalize_first_letter(field_name)
        if field_object_name == "lname_field":
            self.capitalize_first_letter(field_name)

        if hasattr(field_name, 'text'):
            text = field_name.text().strip()  # if field_name is a QlineEdit
        else:
            text = field_name.currentText().strip()  # if field_name is a QComboBox

        if 'label_name' in kwargs:
            label_name = kwargs.get("label_name")
            label_name.clear()
            label_name.setText(text)
        else:
            print(text)

    def generate_password(self):
        if self.generatePassword_checkBox.isChecked():
            generator = PasswordGenerator()
            generated_password = generator.password_generate(5)
            print(f'Password generated: {generated_password}')
            self.password_field.setText(generated_password)
        else:
            self.password_field.clear()

    def add_comboBox_options(self, directory_name, comboBox_name, option_name):
        filter_dir = f"app/resources/config/{directory_name}"

        with open(filter_dir, 'r') as f:
            options = json.load(f)

        for option in options[option_name]:
            if list(option.values())[0] != "Show All":
                comboBox_name.addItem(list(option.values())[0])
            if list(option.values())[0] == "Show All":
                comboBox_name.addItem(" ")