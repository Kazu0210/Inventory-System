from PyQt6.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QApplication, QAbstractItemView, QFrame, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QIntValidator, QIcon, QBrush, QColor

# from ui.NEW.orders_page import Ui_orderPage_Form
from ui.final_ui.orders_page import Ui_Form as Ui_orderPage_Form
from ui.final_ui.recent_order_item import Ui_Frame as Ui_recentOrderItem
from ui.final_ui.cart_item import Ui_Frame as Ui_cart_item
from ui.final_ui.ordered_products_item import Ui_Frame as Ui_ordered_products_item
from ui.final_ui.ordered_products_table_item import Ui_Frame as Ui_ordered_products_table_item
# from pages.admin.new_order_page import NewOrderPage
# from pages.admin.new_order_page import AddOrderForm

from utils.Inventory_Monitor import InventoryMonitor
import pymongo, json, re, os
from pymongo import DESCENDING
from datetime import datetime

class RecentOrderItem(QFrame, Ui_recentOrderItem):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class CartItem(QFrame, Ui_cart_item):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class OrderedProductsItem(QFrame, Ui_ordered_products_item):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class OrderedProductsTableItem(QFrame, Ui_ordered_products_table_item):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class OrderPage(QWidget, Ui_orderPage_Form):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        
        self.labels = []
            
        self.load_payment_status_options()
            
        self.load_order_status_options()
        self.load_cylinder_status_options()

        self.update_total_orders()

        self.hide_back_button()

        # Initialize the form with the provided order_id
        self.order_id = self.generate_order_id()

        # Connect signals to slots for automatic calculation
        self.quantity_box.valueChanged.connect(self.calculate_total_amount)  # When quantity changes
        self.price_input.textChanged.connect(self.calculate_total_amount)  # When price changes
        self.productName_comboBox.currentTextChanged.connect(self.update_cylinder_size) # Change cylinder size when name changes
        self.cylindersize_box.currentTextChanged.connect(lambda: self.update_price()) # Change price

        # Button connections
        self.addItem_btn.clicked.connect(self.save_form)
        self.finalize_order_pushButton.clicked.connect(lambda: self.confirm_button_clicked())
        self.back_pushButton.clicked.connect(lambda: self.handle_back_button())

        self.add_product_name()
        self.reset_quantity_box()

        # Initialize Inventory Monitor
        self.product_monitor = InventoryMonitor('products_items')
        self.product_monitor.start_listener_in_background()
        self.product_monitor.data_changed_signal.connect(lambda: self.update_cart_widgets())

        self.orders_monitor = InventoryMonitor('orders')
        self.orders_monitor.start_listener_in_background()
        self.orders_monitor.data_changed_signal.connect(lambda: self.update_order_widgets())

        self.cart_monitor = InventoryMonitor('cart')
        self.cart_monitor.start_listener_in_background()
        self.cart_monitor.data_changed_signal.connect(lambda: self.update_cart_widgets())

        self.set_current_date()

        self.update_cart_item_quantity()

        self.update_cart()

        self.display_recent_orders()
        self.load_orders_table()

    def load_orders_table(self, page=0, rows_per_page=10):
        """Load prices current price on the prices table with pagination."""
        self.current_page = page  # Keep track of the current page
        self.rows_per_page = rows_per_page  # Number of rows per page

        table = self.orders_tableWidget
        table.setSortingEnabled(True)
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table

        table.setStyleSheet("""
        QTableWidget{
        border-radius: 5px;
        background-color: #fff;
        color: #000;
        }
        QHeaderView:Section{
        background-color: #228B22;
        color: #fff;               
        font: bold 12pt "Noto Sans";
        }
        QTableWidget::item {
            border: none;  /* Remove border from each item */
            padding: 5px;  /* Optional: Adjust padding to make the items look nicer */
        }
            QScrollBar:vertical {
                border: none;
                background: #0C959B;
                width: 13px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #002E2C;
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #0C959B;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #555;
                border-radius: 7px;
                min-width: 30px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #f0f0f0;
            }
        """)

        # Header JSON directory
        header_dir = "app/resources/config/table/order_tableHeader.json"

        # Settings directory
        settings_dir = "app/resources/config/settings.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.orders_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)

        for column in range(table.columnCount()):
            table.setColumnWidth(column, 145)

        # Set uniform row height for all rows
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

        header.setFixedHeight(50)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]
        
        # query filter
        # filter = {}

        # if self.searchBar_lineEdit != "":
        #     filter = {"$or": [
        #         {"product_name": {"$regex": self.searchBar_lineEdit.text(), "$options": "i"}},  # Case-insensitive match
        #         {"product_id": {"$regex": self.searchBar_lineEdit.text(), "$options": "i"}}
        #     ]}

        # Get data from MongoDB
        data = list(self.connect_to_db('orders').find({}).sort("_id", -1))
        if not data:
            return  # Exit if the collection is empty

        with open(settings_dir, 'r') as f:
            settings = json.load(f)
            self.current_time_format = settings['time_date'][0]['time_format']

        # Pagination logic
        start_row = page * rows_per_page
        end_row = start_row + rows_per_page
        paginated_data = data[start_row:end_row]

        # Populate table with paginated data
        for row, item in enumerate(paginated_data):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)
                if value is not None:

                    if header == 'totalvalue':
                        try:
                            if value:
                                formatted_value = f"₱ {value:,.2f}"
                                value = formatted_value

                        except Exception as e:
                            print(f"Error: {e}")

                        # Inside the `for column, header in enumerate(self.header_labels):` loop
                    elif header == 'products':
                        # Ensure value is a list
                        if isinstance(value, list):
                            view_prod_pushButton = QPushButton('View Products')
                            view_prod_pushButton.clicked.connect(lambda _, v=value, r=row: self.handle_view_products_button(v, r))
                            # view_prod_pushButton.clicked.connect(lambda: self.handle_view_products_button())
                            view_prod_pushButton.setStyleSheet("""
                            color: #000;
                            border: 1px solid #000;
                            """)
                            self.orders_tableWidget.setCellWidget(row, column, view_prod_pushButton)

                            continue
                        else:
                            value = "Invalid product data"
                    elif header == 'paymentstatus':
                        # Retrieve the order_id for the current row (assuming order_id is in column 0)
                        order_id = self.orders_tableWidget.item(row, 0).text() if self.orders_tableWidget.item(row, 0) else None

                        try:
                            payment_stat = QComboBox()
                            payment_stat.setStyleSheet("""
                                QComboBox {
                                    background-color: white;
                                    color: black;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: white;
                                }
                            """)
                            
                            # Ensure the correct order_id is captured in the lambda
                            payment_stat.currentTextChanged.connect(
                                lambda text, oid=order_id, v=value, r=row: self.handle_payment(v, r, text, oid)
                            )

                            self.orders_tableWidget.setCellWidget(row, column, payment_stat)
                            payment_stat_dir = "app/resources/config/filters.json"

                            # Open and load the JSON file
                            with open(payment_stat_dir, 'r') as f:
                                data = json.load(f)

                            # Populate the combobox with values
                            payment_stat.clear()
                            found_current_status = False
                            for job in data['payment_status']:
                                job_value = list(job.values())[0]
                                if job_value == value:
                                    payment_stat.addItem(job_value)
                                    found_current_status = True
                                    break

                            for job in data['payment_status']:
                                job_value = list(job.values())[0]
                                if job_value not in ["Default", "Show All"] and job_value != value:
                                    payment_stat.addItem(job_value)

                            if not found_current_status:
                                payment_stat.insertItem(0, value)

                            payment_stat.addItem(str(value))
                        except Exception as e:
                            print(f"Error loading payment status: {e}")
                        continue
                    elif header == 'orderstatus':
                        # Retrieve the order_id for the current row (assuming order_id is in column 0)
                        order_id = self.orders_tableWidget.item(row, 0).text() if self.orders_tableWidget.item(row, 0) else None

                        try:
                            order_stat = QComboBox()
                            order_stat.setStyleSheet("""
                                QComboBox {
                                    background-color: white;
                                    color: black;
                                }
                                QComboBox QAbstractItemView {
                                    background-color: white;
                                }
                            """)
                            
                            # Ensure the correct order_id is captured in the lambda
                            order_stat.currentTextChanged.connect(
                                lambda text, oid=order_id, v=value, r=row: self.handle_order_status(v, r, text, oid)
                            )

                            self.orders_tableWidget.setCellWidget(row, column, order_stat)
                            order_stat_dir = "app/resources/config/filters.json"

                            # Open and load the JSON file
                            with open(order_stat_dir, 'r') as f:
                                data = json.load(f)

                            # Populate the combobox with values
                            order_stat.clear()
                            found_current_status = False
                            for job in data['order_status']:
                                job_value = list(job.values())[0]
                                if job_value == value:
                                    order_stat.addItem(job_value)
                                    found_current_status = True
                                    break

                            for job in data['order_status']:
                                job_value = list(job.values())[0]
                                if job_value not in ["Default", "Show All"] and job_value != value:
                                    order_stat.addItem(job_value)

                            if not found_current_status:
                                order_stat.insertItem(0, value)

                            order_stat.addItem(str(value))
                        except Exception as e:
                            print(f"Error loading order status: {e}")
                        continue

                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # Check if row index is even
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                    table.setItem(row, column, table_item)

        # Add navigation controls
        # self.update_navigation_controls(len(data), page, rows_per_page)

    def handle_order_status(self, pending_status, row, text, order_id):
        """handle payment button clicked"""
        print(f"row: {row}")
        print(f"Pending Status: {pending_status}")
        print(f'New text: {text}')
        print(f'Order id: {order_id}')

        if text != pending_status:
            print(f'Not the same')
            msg_box = QMessageBox.question(self, 
                                  "Confirm Action",
                                  "Are you sure you want to perform this action?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if msg_box == QMessageBox.StandardButton.Yes:
                filter = {
                    'order_id': order_id
                }
                self.connect_to_db('orders').update_one(filter, {'$set': {'order_status': text}})

                QMessageBox.information(self, "Success", "Order status updated successfully")
            else:
                print('User selected no')

    def handle_payment(self, pending_status, row, text, order_id):
        """handle payment button clicked"""
        print(f"row: {row}")
        print(f"Pending Status: {pending_status}")
        print(f'New text: {text}')
        print(f'Order id: {order_id}')

        if text != pending_status:
            print(f'Not the same')
            msg_box = QMessageBox.question(self, 
                                  "Confirm Action",
                                  "Are you sure you want to perform this action?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            
            if msg_box == QMessageBox.StandardButton.Yes:
                filter = {
                    'order_id': order_id
                }
                self.connect_to_db('orders').update_one(filter, {'$set': {'payment_status': text}})

                QMessageBox.information(self, "Success", "Payment status updated successfully")
            else:
                print('User selected no')

    def load_view_products_table(self, products, page=0, rows_per_page=10):
        """Load the view products table with the products sold"""
        self.current_page = page  # Keep track of the current page
        self.rows_per_page = rows_per_page  # Number of rows per page
        table = self.orders_tableWidget
        table.setSortingEnabled(True)
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table
        table.setStyleSheet("""
        QTableWidget{
        border-radius: 5px;
        background-color: #fff;
        color: #000;
        }
        QHeaderView:Section{
        background-color: #228B22;
        color: #fff;               
        font: bold 12pt "Noto Sans";
        }
        QTableWidget::item {
            border: none;  /* Remove border from each item */
            padding: 5px;  /* Optional: Adjust padding to make the items look nicer */
        }
            QScrollBar:vertical {
                border: none;
                background: #0C959B;
                width: 13px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #002E2C;
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #0C959B;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 14px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #555;
                border-radius: 7px;
                min-width: 30px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #f0f0f0;
            }
        """)
        # Header JSON directory
        header_dir = "app/resources/config/table/view_products_tableHeader.json"
        # Settings directory
        settings_dir = "app/resources/config/settings.json"
        with open(header_dir, 'r') as f:
            header_labels = json.load(f)
        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)
        header = self.orders_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)

        for column in range(table.columnCount()):
            table.setColumnWidth(column, 145)

        # Set uniform row height for all rows
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50
        header.setFixedHeight(50)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

        # if self.search_lineEdit.text().strip():  # Check if the input is not empty and strip any whitespace
        #     filter = {
        #         "product_name": {"$regex": self.search_lineEdit.text(), "$options": "i"}  # Case-insensitive match
        #     }

        # Get data from MongoDB
        # data = list(self.connect_to_db('sales').find(filter).sort("_id", -1))
        data = list(products)
        if not data:
            return  # Exit if the collection is empty
        
        with open(settings_dir, 'r') as f:
            settings = json.load(f)
            self.current_time_format = settings['time_date'][0]['time_format']
        # Pagination logic
        start_row = page * rows_per_page
        end_row = start_row + rows_per_page
        paginated_data = data[start_row:end_row]
        # Populate table with paginated data
        for row, item in enumerate(paginated_data):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)
                if value is not None:
                    if header == 'price':
                        try:
                            if value:
                                formatted_value = f"₱ {value:,.2f}"
                                value = formatted_value
                        except Exception as e:
                            print(f"Error: {e}")
                    elif header == 'totalamount':  
                        try:
                            if value:
                                formatted_value = f"₱ {value:,.2f}"
                                value = formatted_value
                        except Exception as e:
                            print(f"Error: {e}")
                    # Add the value to the table as a QTableWidgetItem
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # Check if row index is even for alternating row colors
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                    
                    table.setItem(row, column, table_item)

    def handle_view_products_button(self, products, row):
        """Handle the 'View Products' button click event"""
        self.clear_orders_table()
        self.show_back_button()

        print(f"Button clicked for row: {row}")
        print(f"Products: {products}")

        self.load_view_products_table(products)

    def handle_back_button(self):
        """Handle the 'Back' button click event"""
        self.load_orders_table()
        self.hide_back_button()

    def hide_back_button(self):
        """Hide back button"""
        self.frame_36.hide()
    
    def show_back_button(self):
        """Show back button"""
        self.frame_36.show()
    
    def clear_orders_table(self):
        """Clear orders table including the header"""
        table = self.orders_tableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setColumnCount(0)

    def view_order_clicked(self):
        """Handles click event of view orders push button"""
        print("View order push button clicked")
    
    def display_recent_orders(self):
        """Show all the 5 recent orders in the current day"""
        # Remove existing labels
        for label in self.labels:
            self.recent_orders_scrollAreaWidgetContents.removeWidget(label)
            label.deleteLater()
        self.labels.clear()

        # Get or set a layout for the widget
        layout = self.recent_orders_scrollAreaWidgetContents.layout()
        if layout is None:
            layout = QVBoxLayout(self.recent_orders_scrollAreaWidgetContents)
            self.recent_orders_scrollAreaWidgetContents.setLayout(layout)

        # Clear the layout by removing all items
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Fetch and display recent orders
        order_data = self.get_recent_order()
        print(f'Recent orders: {order_data}')
        for order in order_data:
            order_item = RecentOrderItem()  # Create the widget for each order
            order_item.order_id_label.setText(order.get("order_id"))
            order_item.customer_name_label.setText(order.get("customer_name", "N/A"))
            order_item.date_label.setText(order.get("order_date"))
            order_item.time_label.setText(order.get("time", "N/A"))
            order_item.total_val_label.setText(f"₱ {order.get('total_value'):,.2f}")
            order_item.status_label.setText(order.get("order_status"))
            order_item.payment_label.setText(order.get("payment_status"))
            layout.addWidget(order_item)  # Add the widget to the layout

            products = order.get('products')

            for product in products:
                print(f"Recent order's Product: {product}")
                print(f"Product ID: {product.get('product_name', 'N/A')}")

                # Get or set layout for ordered_prod_frame
                products_frame_layout = order_item.ordered_prod_frame.layout()
                if products_frame_layout is None:
                    products_frame_layout = QVBoxLayout(order_item.ordered_prod_frame)
                    order_item.ordered_prod_frame.setLayout(products_frame_layout)

                # Create and configure OrderedProductsItem
                product_item = OrderedProductsItem()

                product_item.prod_name_label.setText(product.get('product_name', 'Unknown Product'))
                product_item.cylinder_size_label.setText(product.get('cylinder_size', '0'))
                product_item.quantity_label.setText(f"x{str(product.get('quantity', '0'))}")

                products_frame_layout.addWidget(product_item)

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
            recent_orders = list(self.connect_to_db("orders").find({}).sort("_id", DESCENDING).limit(5))
            return recent_orders

        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        
    def confirm_button_clicked(self):
        """Handles the click event of the "Confirm Order" button"""
        try:
            # Get cart data
            data = self.get_cart_data()
            order_id = data.get('order_id', 'N/A')
        except Exception as e:
            print(f"Error: {e}")

        # Check if cart is empty
        if data is None:
            return  # Do not proceed if the cart is empty

        try:
            # Save data to orders database
            self.connect_to_db('orders').insert_one(data)
            
            self.record_sales(order_id)
            
            # Clear the cart after processing the order
            self.connect_to_db('cart').delete_many({})

            QMessageBox.information(self, "Order Confirmation", "Order has been successfully placed.")
        except Exception as e:
            print(f'Error saving order: {e}')
            QMessageBox.critical(self, "Order Confirmation", "Failed to place order.")
        
    def get_cart_data(self):
        """Returns the cart data and updates inventory"""
        # Check if the cart is empty
        cart_count = self.connect_to_db('cart').count_documents({})

        if cart_count == 0:
            # Show a message if the cart is empty
            QMessageBox.information(self, "Select an item first!", "Please select an item from the list before proceeding.")
            return None  # Or return a suitable response if necessary

        # Aggregate to calculate the total value
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalSum": {"$sum": "$total_amount"}
                }
            }
        ]
        result = list(self.connect_to_db('cart').aggregate(pipeline))

        # Extract form details
        order_id = self.generate_order_id()
        date = self.get_current_date()

        current_time = datetime.now()
        time = current_time.strftime("%I:%M%p").lower()

        customer_name = self.customer_name_lineEdit.text()
        delivery_address = self.delivery_address_plainTextEdit.toPlainText()
        contact = self.contact_info.text()
        products = list(self.connect_to_db('cart').find({}, {'_id': 0}))  # Cart products
        total_value = result[0].get('totalSum', 0) if result else 0
        payment_stat = self.payment_box.currentText()
        order_stat = self.status_box.currentText()
        remarks = self.note_input.toPlainText()

        print(f'Customer name: {customer_name}')

        # Reduce quantity in the products collection
        for product in products:
            product_name = product.get("product_name")  # Ensure 'product_name' exists
            cylinder_size = product.get("cylinder_size")  # Ensure 'cylinder_size' exists
            cart_quantity = product.get("quantity", 0)  # Get quantity in the cart

            # Update the 'products_items' collection by matching product_name and cylinder_size
            self.connect_to_db('products_items').update_one(
                {
                    "product_name": product_name,  # Match by product name
                    "cylinder_size": cylinder_size  # Match by cylinder size
                },
                {
                    "$inc": {"quantity_in_stock": -cart_quantity}  # Reduce the stock quantity
                }
            )

        # Prepare order data
        data = {
            'order_id': order_id,
            'order_date': date,
            'time': time,
            'customer_name': customer_name,
            'delivery_address': delivery_address,
            'contact': contact,
            'products': products,
            'total_value': total_value,
            'payment_status': payment_stat,
            'order_status': order_stat,
            'remarks': remarks
        }

        # Clear the cart after processing the order
        # self.connect_to_db('cart').delete_many({})

        return data
    
    def update_order_widgets(self):
        """Update all the widgets that connected to the products items db"""
        self.add_product_name()
        self.update_cart()
        self.display_recent_orders()
        self.update_total_orders()
        self.load_orders_table()

    def update_cart_widgets(self):
        """Update all the widgets that connected to the cart db"""
        self.update_cart()
        self.update_cart_item_quantity()

    def set_remove_icon(self, button_object):
        """Set remove icon for each cart item"""
        remove_icon = QIcon("app/resources/icons/black-theme/trash-bin.png")
        button_object.setIcon(remove_icon)

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
            current_stock = self.connect_to_db('products_items').find_one(
                {
                    'product_name': item['product_name'],
                    'cylinder_size': item['cylinder_size']
                },
                {
                    'quantity_in_stock': 1,
                    '_id': 0
                }
            )
            current_stock_value = current_stock.get('quantity_in_stock', 0) if current_stock else 0

            # Create a new CartItem instance for each item
            cart_item = CartItem()

            # Set validator for quantity based on current stock
            num_only = QIntValidator(0, current_stock_value)  # Accept numbers only within stock range
            cart_item.quantity_lineEdit.setMaxLength(5)
            cart_item.quantity_lineEdit.setValidator(num_only)

            cart_item.cylinder_size_label.setText(item["cylinder_size"])
            cart_item.product_name_label.setText(item["product_name"])
            cart_item.quantity_lineEdit.setText(f'{str(item["quantity"])}')
            cart_item.unit_price_label.setText(f'₱ {item["price"]:,.2f}')
            cart_item.total_price_label.setText(f'₱ {item["total_amount"]:,.2f}')
            cart_item.available_quantity_label.setText(f'{current_stock_value} pieces available')
            self.set_remove_icon(cart_item.remove_pushButton)


            # Connect the remove button to the delete function
            cart_item.remove_pushButton.clicked.connect(lambda _, id=item["_id"]: self.remove_from_cart(id))

            # Connect decrement button to decrement quantity
            cart_item.decrement_pushButton.clicked.connect(lambda _, id=item['_id']: self.decrement_quantity(id))

            # Connect increment button to increment quantity
            cart_item.increment_pushButton.clicked.connect(lambda _, id=item['_id']: self.increment_quantity(id))

            # Limit quantity based on stock when updating
            cart_item.quantity_lineEdit.returnPressed.connect(
                lambda qty_edit=cart_item.quantity_lineEdit, id=item['_id'], stock=current_stock_value:
                self.update_new_quantity(id, min(int(qty_edit.text()), stock))
            )

            # Add the CartItem widget to the layout
            layout.addWidget(cart_item)

    def update_new_quantity(self, _id, new_quantity):
        """Update the quantity of an item in cart when typed on line edit"""
        print(f'enter button clicked')
        print(f'_id: {_id}')
        print(f'new quantity: {new_quantity}')

    def get_new_total_value(self, new_quantity, price):
        print(f'Price: {price}')
        total_value = int(new_quantity) * int(price)

        return int(total_value)

    def increment_quantity(self, id):
        try:
            # Connect to the cart collection and fetch the item
            cart_data = self.connect_to_db('cart').find_one({"_id": id})
            if not cart_data:
                print(f"Item with ID {id} not found in the cart.")
                return

            # Retrieve current quantity and stock details
            current_quantity = cart_data.get("quantity", 0)
            product_name = cart_data.get("product_name", "")
            cylinder_size = cart_data.get("cylinder_size", "")
            price = cart_data.get("price", 0)

            # Fetch the current stock from the products_items collection
            stock_data = self.connect_to_db('products_items').find_one(
                {"product_name": product_name, "cylinder_size": cylinder_size},
                {"quantity_in_stock": 1, "_id": 0}
            )
            current_stock_value = stock_data.get("quantity_in_stock", 0) if stock_data else 0

            # Check if the quantity can be incremented
            if current_quantity < current_stock_value:
                new_quantity = current_quantity + 1
                total_value = self.get_new_total_value(new_quantity, price)

                # Update the quantity and total amount in the cart collection
                self.connect_to_db('cart').update_one(
                    {"_id": id},
                    {"$set": {"quantity": new_quantity, "total_amount": total_value}}
                )

                # Log the increment action
                print(f"Quantity of item with ID {id} incremented to {new_quantity}.")
            else:
                print(f"Cannot increment quantity for item with ID {id}. Maximum stock reached ({current_stock_value}).")
                QMessageBox.warning(self, "Maximum Stock Reached", "You have reached the maximum stock available for this item.")
        except Exception as e:
            print(f"Error incrementing quantity: {e}")

    def decrement_quantity(self, id):
        try:
            # Connect to the cart collection and fetch the item
            cart_data = self.connect_to_db('cart').find_one({"_id": id})
            if not cart_data:
                print(f"Item with ID {id} not found in the cart.")
                return

            # Retrieve current quantity and product details
            current_quantity = cart_data.get("quantity", 0)
            product_name = cart_data.get("product_name", "")
            cylinder_size = cart_data.get("cylinder_size", "")
            price = cart_data.get("price", 0)

            if current_quantity > 0:  # Allow decrementing to 0
                new_quantity = current_quantity - 1
                total_value = self.get_new_total_value(new_quantity, price)

                # Ask for confirmation if the item quantity is being reduced to 0
                if new_quantity == 0:
                    reply = QMessageBox.question(self, 'Confirm Removal',
                                                f"Are you sure you want to remove the item '{product_name}' (Cylinder Size: {cylinder_size}) from the cart?",
                                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    
                    if reply == QMessageBox.StandardButton.Yes:
                        # Remove item from cart without returning quantity to stock
                        self.connect_to_db('cart').delete_one({"_id": id})
                        print(f"Item with ID {id} removed from the cart as quantity reached 0.")
                    else:
                        # If the user cancels, print a message (optional)
                        print(f"Removal of item with ID {id} was cancelled.")
                else:
                    # Update the cart with new quantity and total
                    self.connect_to_db('cart').update_one(
                        {"_id": id},
                        {"$set": {"quantity": new_quantity, "total_amount": total_value}}
                    )
                    print(f"Quantity of item with ID {id} decremented to {new_quantity}.")

            else:
                print(f"Quantity of item with ID {id} is already at the minimum (0).")

        except Exception as e:
            print(f"Error decrementing quantity: {e}")

    def remove_from_cart(self, item_id):
        """Remove an item from the cart database and update the cart."""
        try:
            # Connect to the cart collection and fetch the item details before deletion
            cart_data = self.connect_to_db('cart').find_one({"_id": item_id})
            if not cart_data:
                print(f"Item with ID {item_id} not found in the cart.")
                return

            product_name = cart_data.get("product_name", "")
            cylinder_size = cart_data.get("cylinder_size", "")
            quantity = cart_data.get("quantity", 0)

            # Delete the item from the cart
            self.connect_to_db('cart').delete_one({"_id": item_id})
            print(f"Item with ID {item_id} removed from the cart.")

            # Do not return the quantity to stock anymore

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

    def record_sales(self, order_id):
        try:
            # Collect the input data
            product_name = self.productName_comboBox.currentText()
            quantity = self.quantity_box.value()
            price = float(self.price_input.text().strip() or "0.0")
            total_amount = float(self.amount_input.text() or "0.0")
            customer_name = self.customer_name_lineEdit.text().strip()
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
            # sales_data = {
            #     "sales_id": self.generate_sales_id(),
            #     "date": date_obj,
            #     "customer_name": customer_name,
            #     "product_id": self.product_id,
            #     "product_name": product_name,
            #     "cylinder_size": cylinder_size,
            #     "quantity": quantity,
            #     "payment_status": payment_status,
            #     "price": price,
            #     "total_amount": total_amount,
            #     "order_id": self.order_id,
            #     "remarks": remarks
            # }

            products_sold = list(self.connect_to_db('cart').find({}, {"_id": 0}))

            orders = self.connect_to_db('orders').find({}, {"_id": 0})
            
            pipeline = [
                {
                    "$group": {  # Group all documents
                        "_id": None,  # No grouping key; process all documents together
                        "total_quantity": {"$sum": "$quantity"}  # Sum up the `quantity` field
                    }
                }
            ]
            result = list(self.connect_to_db('cart').aggregate(pipeline))

            if result:
                total_quantity = result[0]["total_quantity"]
                print(f"Total Quantity: {total_quantity}")
            else:
                print("No data found.")

            # get total value

            pipeline = [
                {
                    "$group": {  # Group all documents
                        "_id": None,  # No grouping key; process all documents together
                        "total_amount": {"$sum": "$total_amount"}  # Sum up the `quantity` field
                    }
                }
            ]
            result = list(self.connect_to_db('cart').aggregate(pipeline))
            if result:
                total_value = result[0]["total_amount"]
                print(f"Total Quantity: {total_value}")
            else:
                print("No data found.")


            sales_data = {
                'sale_id': self.generate_sales_id(),
                'customer_name': customer_name,
                'sale_date': date_obj,
                'products_sold': products_sold,
                'quantity_sold': total_quantity,
                'total_value': total_value,
                'order_id': order_id
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
        self.product_quantity_available_label.setText(f"{available_quantity}")
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
            customer_name = self.customer_name_lineEdit.text().strip()
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
                "product_id": self.get_product_id(self.productName_comboBox.currentText(), self.cylindersize_box.currentText()),
                "product_name": product_name,
                "cylinder_size": self.cylindersize_box.currentText(),
                "quantity": quantity,
                "price": price, 
                "total_amount": total_amount
            }

            # Check if a record with the same product name and cylinder size exists
            existing_item = self.connect_to_db('cart').find_one({
                "product_name": product_name,
                "cylinder_size": order_data["cylinder_size"]
            })

            if existing_item:
                # If the item exists, update its quantity, price, and total amount
                new_quantity = existing_item["quantity"] + quantity
                new_total_amount = new_quantity * price
                self.connect_to_db('cart').update_one(
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
                self.connect_to_db('cart').insert_one(order_data)
                QMessageBox.information(self, "Data Submitted", "New order added successfully!")

            # Update total value (no stock reduction)
            self.update_total_value()
        except Exception as e:
            print(f"Error saving form: {e}")

    def clear_new_order_form(self):
        """Clears the new order form"""
        self.customer_name_lineEdit.clear()
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