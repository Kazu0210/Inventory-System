from PyQt6.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QApplication, QAbstractItemView, QFrame
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QIntValidator

# from ui.NEW.orders_page import Ui_orderPage_Form
from ui.final_ui.orders_page import Ui_Form as Ui_orderPage_Form
from ui.final_ui.recent_order_item import Ui_Frame as Ui_recentOrderItem
from ui.final_ui.cart_item import Ui_Frame as Ui_cart_item
# from pages.admin.new_order_page import NewOrderPage
from pages.admin.new_order_page import AddOrderForm

from utils.Inventory_Monitor import InventoryMonitor
import pymongo, json, re
from pymongo import DESCENDING
from datetime import datetime

class RecentOrderItem(QFrame, Ui_orderPage_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class CartItem(QFrame, Ui_cart_item):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class OrderPage(QWidget, Ui_orderPage_Form):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        
        self.labels = []

        self.update_total_orders()
            
        self.load_payment_status_options()
            
        self.load_order_status_options()
        self.load_cylinder_status_options()

        # Initialize the form with the provided order_id
        self.order_id = self.generate_order_id()

        # Connect signals to slots for automatic calculation
        self.quantity_box.valueChanged.connect(self.calculate_total_amount)  # When quantity changes
        self.price_input.textChanged.connect(self.calculate_total_amount)  # When price changes
        self.productName_comboBox.currentTextChanged.connect(self.update_cylinder_size) # Change cylinder size when name changes
        self.cylindersize_box.currentTextChanged.connect(lambda: self.update_price()) # Change price

        # Connect "Add Item" button click event to the save_form method
        self.addItem_btn.clicked.connect(self.save_form)

        self.add_product_name()
        self.reset_quantity_box()

        # Initialize Inventory Monitor
        self.product_monitor = InventoryMonitor('products_items')
        self.product_monitor.start_listener_in_background()
        self.product_monitor.data_changed_signal.connect(lambda: self.add_product_name())

        self.orders_monitor = InventoryMonitor('orders')
        self.orders_monitor.start_listener_in_background()
        self.orders_monitor.data_changed_signal.connect(lambda: self.update_total_orders())

        self.cart_monitor = InventoryMonitor('cart')
        self.cart_monitor.start_listener_in_background()
        self.cart_monitor.data_changed_signal.connect(lambda: self.update_cart_widgets())

        self.set_current_date()

        self.display_recent_orders()

        self.update_cart_item_quantity()

        self.update_cart()

    def update_cart_widgets(self):
        """Update all the widgets that connected to the cart db"""
        self.update_cart()
        self.update_cart_item_quantity()

    def update_cart(self):
        """Update items in the cart."""

        # Get the layout of orders_scrollAreaWidgetContents
        layout = self.orders_scrollAreaWidgetContents.layout()
        if layout is None:
            return  # Exit if there is no layout

        # Clear all existing widgets from the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Retrieve data from the database
        cart_data = list(self.connect_to_db('cart').find({}))

        for item in cart_data:
            # Create a new CartItem instance for each item
            cart_item = CartItem()

            # Validator for quantity
            num_only = QIntValidator(0, 9999) # accept numbers only
            cart_item.quantity_lineEdit.setMaxLength(5)
            cart_item.quantity_lineEdit.setValidator(num_only)

            cart_item.cylinder_size_label.setText(item["cylinder_size"])
            cart_item.product_name_label.setText(item["product_name"])
            cart_item.quantity_lineEdit.setText(f'{str(item["quantity"])}')
            cart_item.unit_price_label.setText(f'₱ {item["price"]:,.2f}')
            cart_item.total_price_label.setText(f'₱ {item["total_amount"]:,.2f}')

            # Connect the remove button to the delete function
            cart_item.remove_pushButton.clicked.connect(lambda _, id=item["_id"]: self.remove_from_cart(id))
            cart_item.update_pushButton.clicked.connect(lambda _, id=item["_id"]: self.show_update_form(id))
            cart_item.decrement_pushButton.clicked.connect(lambda _, id=item['_id']: self.decrement_quantity(id))
            cart_item.increment_pushButton.clicked.connect(lambda _, id=item['_id']: self.increment_quantity(id))
            cart_item.quantity_lineEdit.returnPressed.connect(
                lambda: self.update_new_quantity(item['_id'], int(cart_item.quantity_lineEdit.text()))
            )


            # Add the CartItem widget to the layout
            layout.addWidget(cart_item)

    def update_new_quantity(self, _id, new_quantity):
        """Update the quantity of an item in cart when typed on line edit"""
        print(f'enter button clicked')
        print(f'_id: {_id}')
        print(f'new quantity: {new_quantity}')

    def get_new_total_value(self, new_quantity, price):
        """Calculate and returns the total value"""
        print(f'New quantity: {new_quantity}')
        print(f'Price: {price}')
        total_value = int(new_quantity) * int(price)
        print(f'Total Value: {total_value}')

        return int(total_value)

    def increment_quantity(self, id):
        try:
            # Connect to the cart collection and update the quantity
            cart_data = self.connect_to_db('cart').find_one({"_id": id})
            if cart_data:
                current_quantity = cart_data.get("quantity", 0)
                new_quantity = current_quantity + 1
                price = cart_data.get("price", 0)

                total_value = self.get_new_total_value(new_quantity, price)

                self.connect_to_db('cart').update_one({"_id": id}, {"$set": {"quantity": new_quantity, "total_amount": total_value}})
                print(f"Quantity of item with ID {id} incremented to {new_quantity}.")
            else:
                print(f"Item with ID {id} not found in the cart.")
        except Exception as e:
            print(f"Error incrementing quantity: {e}")

    def decrement_quantity(self, id):
        try:
            # Connect to the cart collection and update the quantity
            cart_data = self.connect_to_db('cart').find_one({"_id": id})
            if cart_data:
                current_quantity = cart_data.get("quantity", 0)
                if current_quantity > 0:  # Allow decrementing to 0
                    new_quantity = current_quantity - 1

                    price = cart_data.get("price", 0)

                    total_value = self.get_new_total_value(new_quantity, price)
                    
                    self.connect_to_db('cart').update_one({"_id": id}, {"$set": {"quantity": new_quantity, "total_amount": total_value}})
                    print(f"Quantity of item with ID {id} decremented to {new_quantity}.")

                    if new_quantity == 0:
                        self.connect_to_db('cart').delete_one({"_id": id})
                        print(f"Item with ID {id} removed from the cart as quantity reached 0.")
                else:
                    print(f"Quantity of item with ID {id} is already at the minimum (0).")

            else:
                print(f"Item with ID {id} not found in the cart.")
        except Exception as e:
            print(f"Error decrementing quantity: {e}")

    def remove_from_cart(self, item_id):
        """Remove an item from the cart database and update the cart."""
        try:
            # Connect to the cart collection and delete the item
            self.connect_to_db('cart').delete_one({"_id": item_id})
            print(f"Item with ID {item_id} removed from the cart.")

            # Update the cart UI
            self.update_cart()
        except Exception as e:
            print(f"Error removing item from the cart: {e}")

    def count_cart_item(self):
        """Count how many item are in the cart"""
        quantity = self.connect_to_db("cart").count_documents({})
        return quantity

    def update_cart_item_quantity(self):
        """Update the quantity of items in the cart"""
        quantity = self.count_cart_item()
        self.orders_quantity_label.setText(str(quantity))

    def display_recent_orders(self):
        """Show all the 5 recent orders in the current day"""
        orders = self.get_recent_order()

        for label in self.labels:
            self.recent_orders_scrollAreaWidgetContents.removeWidget(label)
            label.deleteLater()
        self.labels.clear()

        layout = self.recent_orders_scrollAreaWidgetContents.layout()

        # If the layout exists, iterate through all the items and remove them
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                
                # If the item is a widget, remove it
                if widget:
                    widget.deleteLater()  # This deletes the widget and removes it from the layout

    def get_recent_order(self):
        """Get the 5 recent orders placed today."""
        try:
            # Get today's date in string format: "YYYY-MM-DD"
            today_date = datetime.now().strftime("%Y-%m-%d")

            # Query to find orders where order_date equals today's date
            query = {
                "order_date": today_date
            }

            # Get the 5 most recent orders
            recent_orders = list(self.connect_to_db("orders").find(query).sort("_id", DESCENDING).limit(5))
            return recent_orders

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def set_current_date(self):
        """Set order date label"""
        self.order_date_label.setText(self.get_current_date())

    def get_current_date(self):
        """Returns current date for the order"""
        return datetime.now().strftime("%Y-%m-%d")
        

    def get_product_id(self, product_name, cylinder_size):
        product_data = self.connect_to_db('products_items').find_one({"product_name": product_name, "cylinder_size": cylinder_size})
        if product_data:
            print(f'Product ID: {product_data}')
            return product_data.get("product_id", None)
        else:
            return None

    def generate_sales_id(self):
        new_sales_id = str(self.connect_to_db('sales').estimated_document_count() + 1).zfill(4)
        return f"SALES{new_sales_id}"

    def record_sales(self):
        try:
            # Collect the input data
            product_name = self.productName_comboBox.currentText()
            quantity = self.quantity_box.value()
            price = float(self.price_input.text().strip() or "0.0")
            total_amount = float(self.amount_input.text() or "0.0")
            customer_name = self.name_input.text().strip()
            cylinder_size = self.cylindersize_box.currentText()
            payment_status = self.payment_box.currentText()
            self.order_id
            remarks = self.note_input.toPlainText()
            # Get the date string from QDate
            # date_string = self.order_input.selectedDate().toString("yyyy-MM-dd")

            date_string = datetime.now().strftime("%Y-%m-%d")

            # Convert the string to a datetime object (if you need a full datetime with time)
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")  # Parse the date string to datetime

            # If you need a time component (defaulting to midnight), you can use:
            date_obj = datetime.combine(date_obj, datetime.now().time())

            # Prepare data for saving
            sales_data = {
                "sales_id": self.generate_sales_id(),
                "date": date_obj,
                "customer_name": customer_name,
                "product_id": self.product_id,
                "product_name": product_name,
                "cylinder_size": cylinder_size,
                "quantity": quantity,
                "payment_status": payment_status,
                "price": price,
                "total_amount": total_amount,
                "order_id": self.order_id,
                "remarks": remarks
            }

            # Insert or update the sales data in the database
            self.connect_to_db('sales').insert_one(sales_data)

            # # Insert or update the orders data in the database
            # self.connect_to_db('orders').insert_one(sales_data)

            # Show confirmation message
            # QMessageBox.information(self, "Sales Recorded", "Sales recorded successfully!")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for price and total amount.")
        except Exception as e:
            print(f"An error occurred while recording sales: {e}")
            QMessageBox.critical(self, "Database Error", f"An error occurred while recording sales: {e}")

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

        self.product_id = self.get_product_id(product_name, cylinder_size)

        print(f"Current Product's Product ID: {self.product_id}")

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
        new_order_id = str(self.connect_to_db("orders").estimated_document_count() + 1).zfill(3)
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
            order_date = self.order_date_label.text()
            order_status = self.status_box.currentText()
            delivery_address = self.delivery_address_plainTextEdit.toPlainText()
            payment_status = self.payment_box.currentText()
            contact_info = self.contact_info.text().strip()
            order_note = self.note_input.toPlainText()
            total_amount = float(self.amount_input.text() or "0.0")

            order_data = {
                "product_name": product_name,
                "cylinder_size": self.cylindersize_box.currentText(),
                "quantity": quantity,
                "price": price, 
                "total_amount": total_amount
            }

            # Connect to the database
            db = self.connect_to_db("cart")

            # Check if a record with the same product name and cylinder size exists
            existing_item = db.find_one({
                "product_name": product_name,
                "cylinder_size": order_data["cylinder_size"]
            })

            if existing_item:
                # If the item exists, update its quantity, price, and total amount
                new_quantity = existing_item["quantity"] + quantity
                new_total_amount = new_quantity * price
                db.update_one(
                    {"_id": existing_item["_id"]},
                    {"$set": {
                        "quantity": new_quantity,
                        "price": price,  # Assuming price can change
                        "total_amount": new_total_amount
                    }}
                )
                QMessageBox.information(self, "Data Updated", "Order updated successfully!")
            else:
                # If the item does not exist, insert it as a new order
                db.insert_one(order_data)
                QMessageBox.information(self, "Data Submitted", "New order added successfully!")

            # Record the order in the sales
            self.record_sales()

            # Reduce inventory quantity and update total value
            self.reduce_quantity()
            self.update_total_value()

            # Clear the form
            self.clear_new_order_form()

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for price and total amount.")
        except Exception as e:
            print(f"An error occurred while saving the order: {e}")
            QMessageBox.critical(self, "Database Error", f"An error occurred while saving the order: {e}")


    def clear_new_order_form(self):
        """Clears the new order form"""
        self.name_input.clear()
        self.delivery_address_plainTextEdit.clear()
        self.contact_info.clear()
        self.note_input.clear()

    def get_total_orders_today(self):
        """
        Retrieves the total number of orders created today from the MongoDB database.
        """
        try:
            # Get today's date in string format: "YYYY-MM-DD"
            today_date = datetime.now().strftime("%Y-%m-%d")

            # Query to find orders where order_date equals today's date
            query = {
                "order_date": today_date
            }

            # Get the total count of orders
            total_orders = self.connect_to_db("orders").count_documents(query)
            return total_orders

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def update_total_orders(self):
        """Update total orders label"""
        total_orders_today = self.get_total_orders_today()
        self.total_orders_label.setText(str(total_orders_today))

    def run_monitor(self, object_to_update):
        # Initialize Inventory Monitor
        self.order_monitor = InventoryMonitor('orders')
        self.order_monitor.start_listener_in_background()
        self.order_monitor.data_changed_signal.connect(object_to_update)
  

    def createOrder(self):
        print(f'Create order button clicked')
        # self.new_order_page = NewOrderPage()
        # self.new_order_page.show(
        self.new_order_page = AddOrderForm(None)
        self.new_order_page.show()

    def update_table(self):
            table = self.orders_tableWidget
            table.setRowCount(0)  # Clear the table

            header_dir = "app/resources/config/table/order_tableHeader.json"

            # Read header labels from the JSON file
            with open(header_dir, 'r') as f:
                header_labels = json.load(f)

            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            # Clean the header labels
            self.header_labels = [self.clean_header(header) for header in header_labels]

            # filter_query = {}
            # order_filter = self.orderStatus.currentText()
            # paymentStatus_filter = self.paymentStatus.currentText()

            # if order_filter != "Show All":
            #     filter_query['order_status'] = order_filter

            # if paymentStatus_filter != "Show All":
            #     filter_query['payment_status'] = paymentStatus_filter

            data = list(self.connect_to_db("orders").find().sort("_id", -1))
            # data = list(self.collection.find(filter_query).sort("_id", -1))
            if not data:
                return  # Exit if the collection is empty

            # Populate table with data
            for row, item in enumerate(data):
                table.setRowCount(row + 1)
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)
                    if value is not None:
                        table.setItem(row, column, QTableWidgetItem(str(value)))

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    
    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]