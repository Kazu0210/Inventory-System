from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QApplication, QDialog,QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QDoubleValidator
from ui.newitemsPage import Ui_Form as NewItemsPage
from utils.Activity_logs import Activity_Logs as activity_logs_util
import datetime
import pymongo
import sys
import json

class newItem_page(QWidget, NewItemsPage):
    def __init__(self, itempage, account_username):
        super().__init__()
        self.setupUi(self)
        self.itempage = itempage

        # logged in account's username
        self.account_username = account_username

        # activity logs class
        self.logs = activity_logs_util()

        timeStamp = self.timestamp
        timeStamp.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        add_btn = self.pushButton
        add_btn.clicked.connect(lambda: self.getProduct())

        # get item categories
        with open('app/resources/data/item_categories.json', 'r') as f:
            categories = json.load(f)

        # add categories
        for category in categories:
            self.cylinder_size.addItem(f"{category} KG")
            

        with open('app/resources/data/item_status.json', 'r') as f:
            status = json.load(f)
        for stat in status:
            self.status.addItem(stat)

        self.cylinder_size.insertItem(self.cylinder_size.count(), "Add")

        add_category_option = self.cylinder_size.count() - 1
        print(f"Last index {add_category_option}")

        self.cylinder_size.currentIndexChanged.connect(self.on_category_changed)

        # create the dialog instance variable
        self.new_job_dialog = None

    def on_category_changed(self, index):
        if index == self.cylinder_size.count() - 1:
            if not self.new_job_dialog:
                self.new_job_dialog = QDialog(self) 
                self.new_job_dialog.setWindowTitle("Add new Category")
                self.new_job_dialog.setModal(True)
                new_job_layout = QVBoxLayout()
                self.new_job_dialog.setLayout(new_job_layout)
                
                new_category_label = QLabel("New Category:")
                self.new_category_field = QLineEdit()
                self.new_category_field.setValidator(QDoubleValidator(0.0, 100.0, 2))
                new_job_layout.addWidget(new_category_label)
                new_job_layout.addWidget(self.new_category_field) 

                save_button = QPushButton("Add Category")
                new_job_layout.addWidget(save_button)

                save_button.clicked.connect(lambda: self.save_new_category(self.new_category_field.text()))

            self.new_job_dialog.show()

    def save_new_category(self, new_category):
        print(f"New categoy added: {new_category}")
        new_category_capitalized = new_category.capitalize()

        job_titles_dir = "app/resources/data/item_categories.json"
        with open(job_titles_dir, 'r') as f:
            titles = json.load(f)

        titles.append(new_category_capitalized)

        with open(job_titles_dir, 'w') as f:
            json.dump(titles, f, indent=4)

        self.logs.added_item_category(self.account_username, new_category_capitalized)

        # add the new category to the qcomboBox
        self.cylinder_size.insertItem(self.cylinder_size.count() - 1,  f"{new_category_capitalized} KG")

        self.new_job_dialog.close()

    def getProduct(self):
        new_product_name = self.product_name.text().strip()
        new_cylinder_size  = self.cylinder_size.currentText()
        new_quantity = self.quantity.text().strip()
        new_price = self.price.text().strip()
        new_product_status = self.status.currentText()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.insert_to_DB(new_product_name, new_cylinder_size, new_quantity, new_price, new_product_status, timestamp)

        self.itempage.content_window_layout.setCurrentIndex(4)

    def insert_to_DB(self, new_product_name, new_cylinder_size, new_quantity, new_price, new_product_status, timestamp):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = client["LPGTrading_DB"]
        collection = db["products_items"]

        # Check if the product already exists in the database
        existing_product = collection.find_one({
            "product_name": new_product_name,
            "cylinder_size": new_cylinder_size,
            "price_per_unit": int(new_price),
            "status": new_product_status
        })

        if existing_product:
            # If the product exists, update the quantity
            existing_quantity = existing_product["quantity_in_stock"]
            new_total_quantity = existing_quantity + int(new_quantity)
            collection.update_one({
                "product_name": new_product_name,
                "cylinder_size": new_cylinder_size,
                "price_per_unit": int(new_price),
                "status": new_product_status
            }, {"$set": {"quantity_in_stock": new_total_quantity}})
            print(f"Product: {new_product_name} quantity updated successfully.")
        else:
            # If the product does not exist, insert a new document
            data = {
                "product_name": new_product_name,
                "cylinder_size": new_cylinder_size,
                "quantity_in_stock": int(new_quantity),
                "price_per_unit": int(new_price),
                "status": new_product_status,
                "timestamp": timestamp,
            }
            result = collection.insert_one(data)
            print(f"Product: {new_product_name} created successfully. ID: {result.inserted_id}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = newItem_page(None)  # Pass None as the main_window argument
    window.show()
    sys.exit(app.exec())