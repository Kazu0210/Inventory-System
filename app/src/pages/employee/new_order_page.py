from PyQt6.QtWidgets import QFrame, QMessageBox

from ui.employee.add_order_item import Ui_Frame as Ui_add_form

import pymongo, json


class AddOrderForm(QFrame, Ui_add_form):
    def __init__(self, order_id=None):
        super().__init__()
        self.setupUi(self)
        
        # Initialize the database connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
        self.db = self.client["LPGTrading_DB"]  # Replace with your database name
        self.collection = self.db["orders"]  # Replace with your collection name
        
        self.load_payment_status_options()
        self.load_order_status_options()
        self.load_cylinder_status_options()

        # Initialize the form with the provided order_id
        self.order_id = order_id if order_id else self.generate_order_id()

        # Connect signals to slots for automatic calculation
        self.quantity_box.valueChanged.connect(self.calculate_total_amount)  # When quantity changes
        self.price_input.textChanged.connect(self.calculate_total_amount)  # When price changes
        self.productName_comboBox.currentTextChanged.connect(self.update_cylinder_size) # Change cylinder size when name changes
        self.cylindersize_box.currentTextChanged.connect(lambda: self.update_price()) # Change price

        # Connect "Add Item" button click event to the save_form method
        self.addItem_btn.clicked.connect(self.save_form)

        self.add_product_name()
        self.reset_quantity_box()
    
    # def limit_quantity(self, min_value, max_value):
    #     try:
    #         quantity = self.quantity_box.value()
    #         print(f'CURRENT QUANTITY: {quantity}')
    #         if quantity < min_value:
    #             self.quantity_box.setMinimum(min_value)
    #         elif quantity > max_value:
    #             self.quantity_box.setMaximum(max_value)
    #     except Exception as e:
    #         print(f"An error occurred while limiting the quantity: {e}")
    #         QMessageBox.critical(self, "Input Error", f"An error occurred while limiting the quantity: {e}")

    def get_quantity_in_stock(self, product_name, cylinder_size):
        product_data = self.connect_to_db('products_items').find_one({"product_name": product_name, "cylinder_size": cylinder_size})
        if product_data:
            return product_data.get("quantity_in_stock", 0)
        else:
            return 0

    def update_price(self):
        product_name = self.productName_comboBox.currentText()
        cylinder_size = self.cylindersize_box.currentText()

        cylinder_price = self.get_product_price(product_name, cylinder_size)
        print(f'Price: {cylinder_price}')
        self.price_input.setText(str(cylinder_price))

        # change the available quantity in stock
        available_quantity = int(self.get_quantity_in_stock(product_name, cylinder_size))
        print(f'avail quantity: {available_quantity}')
        # available quantity as the maximum quantity on the spinBox
        self.quantity_box.setMaximum(available_quantity)

    def get_product_price(self, product_name, cylinder_size):
        product_data = self.connect_to_db('products_items').find_one({"product_name": product_name, "cylinder_size": cylinder_size})
        if product_data:
            return product_data.get("price_per_unit", 0.0)
        else:
            return 0.0

    def update_cylinder_size(self):
        # Get the selected product name
        current_product_name = self.productName_comboBox.currentText()
        print(f'product name: {current_product_name}')

        print(f'Available cylinder sizes: {self.get_available_cylinder_sizes(current_product_name)}')

        self.cylindersize_box.clear()
        available_cylinder_sizes = self.get_available_cylinder_sizes(self.productName_comboBox.currentText())
        for size in available_cylinder_sizes:
            self.cylindersize_box.addItem(size)

    def get_available_cylinder_sizes(self, product_name):
        product_data = self.connect_to_db('products_items').find({"product_name": product_name})
        cylinder_sizes = [product['cylinder_size'] for product in product_data]
        return list(set(cylinder_sizes))

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    def reset_quantity_box(self):
        self.quantity_box.setValue(1)

    def add_product_name(self):
        # fill the comboBox for product name
        product_name = self.connect_to_db('products_items').find({}, {"product_name": 1, "_id": 0}) # get all the product names on the db only

        product_name_list = [product['product_name'] for product in product_name]
        self.productName_comboBox.addItems(list(set(product_name_list))) # add names to the comboBox
        
    def generate_order_id(self):
        new_order_id = str(self.collection.estimated_document_count() + 1).zfill(3)
        return f"ORD{new_order_id}"  # ORD00001

    def load_payment_status_options(self):
        try:
            filter_dir = "app/resources/config/filters_box.json"

            with open(filter_dir, 'r') as f:
                data = json.load(f)

            self.payment_box.clear()
            for status in data['payment_status']:

                self.payment_box.addItem(list(status.values())[0])
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading payment status options: {e}")
            QMessageBox.warning(self, "Error", "Could not load payment status options.")
    
    def load_cylinder_status_options(self):
        try:
            filter_dir = "app/resources/config/filters_box.json"

            with open(filter_dir, 'r') as f:
                data = json.load(f)

            self.cylindersize_box.clear()
            for status in data['cylinder_size']:

                self.cylindersize_box.addItem(list(status.values())[0])
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading cylinder status options: {e}")
            QMessageBox.warning(self, "Error", "Could not load cylinder status options.")

    def load_order_status_options(self):
        try:
            filter_dir = "app/resources/config/filters_box.json"

            with open(filter_dir, 'r') as f:
                data = json.load(f)

            self.status_box.clear()
            for status in data['order_status']:

                self.status_box.addItem(list(status.values())[0])
                
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading order status options: {e}")
            QMessageBox.warning(self, "Error", "Could not load order status options.")

    def load_order_data(self, order_data):
        self.cylindersize_box.setCurrentText(order_data.get("cylinder_size", ""))
        self.quantity_box.setValue(order_data.get("quantity", 1))
        self.price_input.setText(str(order_data.get("price", 0.0)))
        self.amount_input.setText(str(order_data.get("total_amount", 0.0)))
        self.status_box.setCurrentText(order_data.get("order_status", ""))
        self.delivery_address_input.setPlainText(order_data.get("delivery_address", ""))
        self.payment_box.setCurrentText(order_data.get("payment_status", ""))
        self.contact_info.setText(order_data.get("contact_info", ""))
        self.note_input.setText(order_data.get("order_note", ""))

    def calculate_total_amount(self):
        """Calculate and update the total amount based on quantity and price."""
        try:
            quantity = self.quantity_box.value()
            price = float(self.price_input.text() or "0.0")  # Handle empty input gracefully
            total_amount = quantity * price
            self.amount_input.setText(f"{total_amount:.2f}")
        except ValueError:
            self.amount_input.setText("0.00")
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for price.")

    def update_total_value(self):
        try:
            product_name = self.productName_comboBox.currentText()
            quantity = self.quantity_box.value()
            price = float(self.price_input.text() or "0.0")
            total_amount = quantity * price
            self.amount_input.setText(f"{total_amount:.2f}")
            product_data = self.connect_to_db('products_items').find_one({"product_name": product_name})
            if product_data:
                current_total_value = product_data.get("total_value", 0)
                new_total_value = current_total_value + total_amount
                self.connect_to_db('products_items').update_one({"product_name": product_name}, {"$set": {"total_value": new_total_value}})
        except Exception as e:
            print(f"An error occurred while updating the total value: {e}")
            QMessageBox.critical(self, "Database Error", f"An error occurred while updating the total value: {e}")

    def reduce_quantity(self):
        try:
            product_name = self.productName_comboBox.currentText()
            quantity = self.quantity_box.value()
            product_data = self.connect_to_db('products_items').find_one({"product_name": product_name, "cylinder_size": self.cylindersize_box.currentText()})
            print(f'Collected product data: {product_data}')
            if product_data:
                current_quantity = product_data.get("quantity_in_stock", 0)
                new_quantity = int(current_quantity) - int(quantity)
                self.connect_to_db('products_items').update_one({"product_name": product_name}, {"$set": {"quantity_in_stock": new_quantity}})
        except Exception as e:
            print(f"An error occurred while reducing the quantity: {e}")
            QMessageBox.critical(self, "Database Error", f"An error occurred while reducing the quantity: {e}")

    def save_form(self):
        """Save the order data after validating the input."""
        try:
            # Collect the input data
            product_name = self.productName_comboBox.currentText()
            customer_name = self.name_input.text().strip()
            quantity = self.quantity_box.value()
            price = float(self.price_input.text().strip() or "0.0")
            order_date = self.order_input.selectedDate().toString("yyyy-MM-dd")
            order_status = self.status_box.currentText()
            delivery_address = self.delivery_address_input.toPlainText().strip()
            payment_status = self.payment_box.currentText()
            contact_info = self.contact_info.text().strip()
            order_note = self.note_input.text().strip()
            total_amount = float(self.amount_input.text() or "0.0")

            # Prepare data for saving
            order_data = {
                "order_id": self.order_id,
                "customer_name": customer_name,
                "order_date": order_date,
                "product_name": product_name,
                "cylinder_size": self.cylindersize_box.currentText(),
                "quantity": quantity,
                "price": price,
                "total_amount": total_amount,
                "order_status": order_status,
                "delivery_address": delivery_address,
                "payment_status": payment_status,
                "contact_info": contact_info,
                "order_note": order_note
            }
            self.reduce_quantity()
            self.update_total_value()

            # Insert or update the order data in the database
            self.collection.insert_one(order_data)


            # Show confirmation message
            QMessageBox.information(self, "Form Submitted", "New order added successfully!")
            self.close()
        
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for price and total amount.")
        except Exception as e:
            print(f"An error occurred while saving the order: {e}")
            QMessageBox.critical(self, "Database Error", f"An error occurred while saving the order: {e}")