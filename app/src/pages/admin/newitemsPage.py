from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, QTimer, Qt
# from ui.newitemsPage import Ui_Form as NewItemsPage
# from ui.addItem_page import Ui_Form as Ui_addItemPage
from ui.final_ui.add_product import Ui_Form as Ui_addItemPage
from utils.Activity_logs import Activity_Logs as activity_logs_util
import datetime, pymongo, sys, json, datetime, random

class newItem_page(QWidget, Ui_addItemPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # logged in account's username

        # activity logs class
        self.logs = activity_logs_util()

        self.settings_dir = "app/resources/config/filters.json" # settings.json directory

        self.fill_form()

        self.add_product_pushButton.clicked.connect(lambda: self.addItemBtn_clicked())
        self.cancel_pushButton.clicked.connect(lambda: self.cancel_clicked())

    def save(self, data):
        try:
            # Check for required keys in the data dictionary
            required_keys = ['item_id', 'product_name', 'category', 'quantity', 'price', 'supplier', 'description', 'status']
            for key in required_keys:
                if key not in data:
                    raise KeyError(f"Missing key: {key}")

            # Get the current date and calculate total value
            current_date = datetime.datetime.now().strftime('%d-%m-%Y')
            total_value = int(data['price']) * int(data['quantity'])

        except ValueError as e:
            print(f"Error: Invalid data type. {e}")
            return  # Exit the function if there's a ValueError
        except KeyError as e:
            print(f"Error: Missing key in data. {e}")
            return  # Exit the function if there's a KeyError
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return  # Exit the function for any other exceptions

        new_data = {
            "product_id": data['item_id'],
            "product_name": data['product_name'],
            "cylinder_size": data['category'],
            "quantity_in_stock": int(data['quantity']),
            "price_per_unit": int(data['price']),
            "supplier": data['supplier'],
            "last_restocked_date": current_date,
            "description": data['description'],
            "total_value": total_value,
            "inventory_status": data['status'],
            "minimum_stock_level": 5
        }

        try:
            self.connect_to_db('products_items').insert_one(new_data)  # Save new data to collection of products
            self.save_to_prices_db(new_data) # save new product to collection of prices
            self.close()
            #  zself.itempage.content_window_layout.setCurrentIndex(4)
            # NEED TO ADD ACTIVITY LOGS
        except Exception as e:
            print(f"Error saving data to database: {e}")

    def save_to_prices_db(self, data):
        """Save new product data to collection of prices"""
        try:
            # generate price id
            price_id = self.generate_price_id()
            price_data = {
                "price_id": price_id,
                "product_id": data['product_id'],
                "product_name": data['product_name'],
                "cylinder_size": data['cylinder_size'],
                "selling_price": data['price_per_unit'],
                "supplier_price" : data.get('supplier_price', None),
                "remarks": ""
            }
            self.connect_to_db("prices").insert_one(price_data)

        except Exception as e:
            print(f"Error saving data to prices database: {e}")

    def generate_price_id(self):
            """Generates price id"""
            # Get the current year
            current_year = datetime.datetime.now().strftime("%Y")

            # Generate a random 3-digit number
            random_number = random.randint(100, 999)
            
            # Format the price_id
            price_id = f"P{current_year}{random_number}"

            return price_id

    def is_productExist(self):
        product_name = self.prod_name_lineEdit.text()
        cylinder_size = self.category_comboBox.currentText()
        supplier = self.supplier_lineEdit.text()

        query = {
            "product_name": product_name,
            "cylinder_size": cylinder_size,
            "supplier": supplier
        }

        # check if all in the query is present in the database

        if self.connect_to_db("products_items").find_one(query):
            return True
        else:
            return False

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    def clearForm(self):
        for field in [self.prod_name_lineEdit, self.quantity_spinBox, self.price_lineEdit, self.supplier_lineEdit, self.desc_plainTextEdit]:
            field.clear()
    
    def productExistNotif(self):
        self.prod_name_lineEdit.setText("Product Already Exist")
        self.prod_name_lineEdit.setStyleSheet("color: red")
        self.prod_name_lineEdit.setReadOnly(True)
        QTimer.singleShot(2000, lambda: self.prod_name_lineEdit.setStyleSheet("color: black"))
        QTimer.singleShot(2000, lambda: self.prod_name_lineEdit.setReadOnly(False))
        QTimer.singleShot(2000, lambda: self.clearForm())

    def addItemBtn_clicked(self):
        print("add item button clicked")

        data = self.get_data()

        if self.is_data_empty():
            QMessageBox.information(
                self,
                "Empty Fields",
                "All fields are empty. Please fill out the form."
            )
        else:
            QMessageBox.information(
                self,
                "Fields Filled",
                "At least one field has been filled."
            )

        if not self.is_productExist():
            self.save(data)
            self.clearForm()
        else:
            self.productExistNotif()

    def is_data_empty(self):
        fields = {
            "product_name": self.prod_name_lineEdit.text(),
            "supplier": self.supplier_lineEdit.text(),
            "price": self.price_lineEdit.text(),
            "quantity": self.quantity_spinBox.text(),
            "description": self.desc_plainTextEdit.toPlainText(),
            "low_stock_threshold": self.low_stock_threshold_spinBox.text()
        }
        
        for key, value in fields.items():
            if key == "quantity" or key == "low_stock_threshold":
                # Check if quantity and low stock threshold are not zero
                if int(value) != 0:
                    return False
            elif value.strip():  
                # Check if other fields are not empty or whitespace
                return False
                
        return True  # Return True if all fields are empty or numeric fields are 0

    def get_data(self):
        data = {
            "item_id": self.productID_label.text(),
            "product_name": self.prod_name_lineEdit.text(),
            "supplier": self.supplier_lineEdit.text(),
            "price": self.price_lineEdit.text(),
            "category": self.category_comboBox.currentText(),
            "status": self.status_comboBox.currentText(),
            "quantity": self.quantity_spinBox.text(),
            "description": self.desc_plainTextEdit.toPlainText()
        }
        return data

    def fill_form(self):
        # self.generate_id()
        self.validate_productID()
        self.update_comboBox()
        self.numberOnly()
        self.limitSupplierName()
        self.limitProductName()
        
    def update_comboBox(self):
        self.cylinderSize_filter()
        self.itemStatus_filter()

    def limitProductName(self):
        self.prod_name_lineEdit.setMaxLength(50)
        regex = QRegularExpression(r"^[a-zA-Z\s]+$")
        validator = QRegularExpressionValidator(regex)
        self.prod_name_lineEdit.setValidator(validator)

    def limitSupplierName(self):
        self.supplier_lineEdit.setMaxLength(50) # set max lenght to 50 characters
        
    def numberOnly(self):
        regex = QRegularExpression(r"^\d{1,4}(\.\d{1,3})?$")  # 1 to 4 digits before decimal, 1 to 3 digits after
        validator = QRegularExpressionValidator(regex)
        self.price_lineEdit.setValidator(validator)

    def itemStatus_filter(self):
        with open(self.settings_dir, 'r') as f:
            data = json.load(f)

        self.status_comboBox.clear()
        for stat in data['item_status']:
            if list(stat.values())[0] != "":
                self.status_comboBox.addItem(list(stat.keys())[0])

    def cylinderSize_filter(self):
        with open(self.settings_dir, 'r') as f:
            data = json.load(f)

        self.category_comboBox.clear()
        for category in data['cylinder_size']:

            value = list(category.values())[0]

            if value == "Show All":
                continue
            if value != "":
                self.category_comboBox.addItem(list(category.keys())[0])

    def validate_productID(self):
        custom_id = self.generate_id()
        custom_id2 = self.generate_id()

        print(f"CUSTOM ID: {custom_id}")
        # print(f"CUSTOM ID 2: {custom_id2}")
        if not self.is_idExist(custom_id):
            self.productID_label.setText(custom_id)

    def is_idExist(self, custom_id):
        item_id = custom_id
        filter = {
            "product_id": item_id
        }
        data = self.connect_to_db('products_items').find_one(filter)
        if not self.connect_to_db('products_items').find_one(data):
            return True
        else:
            return False
        
    def generate_id(self):
            current_date = datetime.datetime.now()
            random_number = str(datetime.datetime.now().microsecond)[:2]
            day = f"{current_date.strftime('%d')}"
            yr = current_date.strftime('%y')

            custom_id = f'LPG{day}{yr}{random_number}'
            # print(f'CUSTOM ID: {custom_id}')
            return custom_id

            # print(f'IS ID EXIST? : {self.is_idExist(custom_id)}')

            # if self.is_idExist:
            #     self.itemID_label.setText(custom_id)

    def close_event(self, event):
        """Detect if the X button is clicked to close the form"""
        print("X button clicked")
        event.accept()
        self.close()

    def cancel_clicked(self):
        """Run when cancel button clicked"""
        self.close()