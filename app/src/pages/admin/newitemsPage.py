from PyQt6.QtWidgets import QWidget, QAbstractItemView, QCheckBox, QTableWidgetItem, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator

# from src.ui.final_ui.add_product import Ui_Form as Ui_addItemPage
from src.ui.new_brand_page import Ui_Form as Ui_addItemPage
from src.utils.Activity_logs import Activity_Logs as activity_logs_util
from src.custom_widgets.message_box import CustomMessageBox


import datetime, pymongo, sys, json, datetime, random

class newItem_page(QWidget, Ui_addItemPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # logged in account's username

        # activity logs class
        self.logs = activity_logs_util()

        self.settings_dir = "D:/Inventory-System/app/resources/config/filters.json" # settings.json directory

        # self.fill_form()

        self.confirm_pushButton.clicked.connect(lambda: self.confirm_button_clicked())
        self.cancel_pushButton.clicked.connect(lambda: self.cancel_clicked())

        self.load_product_selection_table()
        self.load_status_comboBox()

        self.load_validations()

    def load_validations(self):
        """load validations for qlineedits"""
        self.brand_lineEdit.setMaxLength(30)
        self.supplier_lineEdit.setMaxLength(20)

    def confirm_button_clicked(self):
        """handles the confirm button click event"""
        self.save_table_data()

    def save_table_data(self):
        # Collect data from checked checkboxes
        checked_rows = []
        for row in range(self.product_selection_tableWidget.rowCount()):
            # Get the checkbox widget from the first column
            checkbox_widget = self.product_selection_tableWidget.cellWidget(row, 0)
            if checkbox_widget and checkbox_widget.isChecked():
                row_data = {}
                # Get quantity and price values
                quantity_widget = self.product_selection_tableWidget.cellWidget(row, 1)
                price_widget = self.product_selection_tableWidget.cellWidget(row, 2)
                row_data['Row'] = row
                row_data['Size'] = checkbox_widget.text()  # Text of the checkbox
                row_data['Quantity'] = quantity_widget.text() if quantity_widget else ""
                row_data['Price'] = price_widget.text() if price_widget else ""

                # Check if Quantity and Price are empty
                if not row_data['Quantity'] or not row_data['Price']:
                    self.show_error_message(f"Quantity and Price are required for size {row_data['Size']}.")
                    return  # Stop and return if validation fails

                checked_rows.append(row_data)

        # Print only checked rows
        print("Checked Rows Data:", checked_rows)

        # Validate other fields
        brand = self.brand_lineEdit.text().strip()
        supplier = self.supplier_lineEdit.text().strip()
        description = self.description_plainTextEdit.toPlainText().strip()
        status = self.status_comboBox.currentText().strip()
        low_stock_threshold = self.low_stock_threshold_spinBox.value()

        # Check if any required field is empty (except description)
        if not brand or not supplier:
            self.show_error_message("Brand, Supplier, and Status are required fields.")
            return

        # If everything is valid, proceed to save the data
        print("All fields are valid. Proceeding to save.")

        print(f'Count: {len(checked_rows)}')

        for data in checked_rows:
            size = data['Size']
            quantity = int(data['Quantity'])
            price = int(data['Price'])
            product_id = self.generate_id()
            total_value = float(quantity) * float(price)

            if self.is_productExist(brand, size, supplier):
                self.show_error_message(f"Product {brand} {size} {supplier} already exists.")
            else:
                data = {
                    'product_id': product_id,
                    'product_name': brand,
                    'cylinder_size': size,
                    'quantity_in_stock': quantity,
                    'price_per_unit': price,
                    'supplier': supplier,
                    'last_restocked_date': "",
                    'description': description,
                    'total_value': total_value,
                    'inventory_status': status,
                    'minimum_stock_level': low_stock_threshold,
                    'stock_level': 'In Stock',
                    'supplier_price': 0
                }

                self.connect_to_db('products_items').insert_one(data)

        CustomMessageBox.show_message('information', 'Product saved', 'Product saved successfully')
        self.close()

    def show_error_message(self, message):
        CustomMessageBox.show_message('critical', 'Error', f'{message}')

    def load_status_comboBox(self):
        """load the status comboBox"""
        filter_dir = 'D:/Inventory-System/app/resources/config/filters.json'
        try:
            with open(filter_dir, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {filter_dir}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in header file.")

        status = [list(status.values())[0] for status in data["item_status"]]
        
        for stats in status:
            if stats != 'Show All':
                self.status_comboBox.addItem(stats)

    def load_product_selection_table(self):
        """load the product selection table"""
        table = self.product_selection_tableWidget
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
        font: bold 10pt "Noto Sans";
        }
        QTableWidget::item {
            border: none;  /* Remove border from each item */
            padding: 5px;  /* Optional: Adjust padding to make the items look nicer */
        }
        QTableWidget::item:selected {
            color: #000;  /* Change text color */
            background-color: #E7E7E7;  /* Optional: Change background color */
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

        # Load header JSON
        header_dir = "D:/Inventory-System/app/resources/config/table/product_selection_tableHeader.json"
        try:
            with open(header_dir, 'r') as f:
                header_labels = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {header_dir}")
            exit()
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in header file.")
            exit()

        # Set table headers
        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        # Configure the table header
        header = table.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setStretchLastSection(True)

        # Set uniform row height
        table.verticalHeader().setDefaultSectionSize(40)

        # Customize header height
        header.setFixedHeight(20)

        # Disable direct editing in cells
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Set smooth scrolling
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Load filter JSON
        filters_dir = "D:/Inventory-System/app/resources/config/filters.json"
        try:
            with open(filters_dir, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found at {filters_dir}")
            exit()
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in filter file.")
            exit()

        # Extract cylinder sizes and dynamically set rows
        cylinder_size = [list(size.values())[0] for size in data["cylinder_size"]]
        row_count = len([size for size in cylinder_size if size != "Show All"])
        table.setRowCount(row_count)

        # Add checkboxes to the first column
        row = 0
        for size in cylinder_size:
            if size != "Show All":
                validator = QIntValidator()

                # Create and add a checkbox
                checkbox = QCheckBox(f"{size}")
                checkbox.setChecked(False)
                table.setCellWidget(row, 0, checkbox)

                # Add a placeholder item for proper row height
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Non-editable
                table.setItem(row, 0, item)

                quantity_lineEdit = QLineEdit()
                quantity_lineEdit.setValidator(validator)
                quantity_lineEdit.setMaxLength(4)
                table.setCellWidget(row, 1, quantity_lineEdit)

                price_lineEdit = QLineEdit()
                price_lineEdit.setValidator(validator)
                price_lineEdit.setMaxLength(4)
                table.setCellWidget(row, 2, price_lineEdit)

                row += 1

    # def get_stock_level(self, stock_quantity: int, stock_threshold: int):
    #     """Return stock level (in stock, low stock, out of stock)"""
        
    #     if stock_quantity == 0:
    #         return "Out of Stock"
    #     elif stock_quantity < stock_threshold:
    #         return "Low Stock"
    #     else:
    #         return "In Stock"

    # def save(self, data):
    #     try:
    #         # Check for required keys in the data dictionary
    #         required_keys = ['item_id', 'product_name', 'category', 'quantity', 'price', 'supplier', 'description', 'status']
    #         for key in required_keys:
    #             if key not in data:
    #                 raise KeyError(f"Missing key: {key}")

    #         # Get the current date and calculate total value
    #         current_date = datetime.datetime.now().strftime('%d-%m-%Y')
    #         total_value = int(data['price']) * int(data['quantity'])

    #     except ValueError as e:
    #         print(f"Error: Invalid data type. {e}")
    #         return  # Exit the function if there's a ValueError
    #     except KeyError as e:
    #         print(f"Error: Missing key in data. {e}")
    #         return  # Exit the function if there's a KeyError
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    #         return  # Exit the function for any other exceptions

    #     new_data = {
    #         "product_id": data['item_id'],
    #         "product_name": data['product_name'],
    #         "cylinder_size": data['category'],
    #         "quantity_in_stock": int(data['quantity']),
    #         "price_per_unit": int(data['price']),
    #         "supplier": data['supplier'],
    #         "last_restocked_date": current_date,
    #         "description": data['description'],
    #         "total_value": total_value,
    #         "inventory_status": data['status'],
    #         "minimum_stock_level": data['low_stock_threshold'],
    #         "stock_level": self.get_stock_level(int(data['quantity']), int(data['low_stock_threshold']))
    #     }

    #     try:
    #         self.connect_to_db('products_items').insert_one(new_data)  # Save new data to collection of products
    #         self.save_to_prices_db(new_data) # save new product to collection of prices
    #         self.close()
    #         #  zself.itempage.content_window_layout.setCurrentIndex(4)
    #         # NEED TO ADD ACTIVITY LOGS
    #         CustomMessageBox.show_message('information', 'New Product', 'Product Saved Successfully.')
            
    #     except Exception as e:
    #         print(f"Error saving data to database: {e}")

    # def save_to_prices_db(self, data):
    #     """Save new product data to collection of prices"""
    #     try:
    #         # generate price id
    #         price_id = self.generate_price_id()
    #         price_data = {
    #             "price_id": price_id,
    #             "product_id": data['product_id'],
    #             "product_name": data['product_name'],
    #             "cylinder_size": data['cylinder_size'],
    #             "selling_price": data['price_per_unit'],
    #             "supplier_price" : data.get('supplier_price', None),
    #             "remarks": ""
    #         }
    #         self.connect_to_db("prices").insert_one(price_data)

    #     except Exception as e:
    #         print(f"Error saving data to prices database: {e}")

    # def generate_price_id(self):
    #         """Generates price id"""
    #         # Get the current year
    #         current_year = datetime.datetime.now().strftime("%Y")

    #         # Generate a random 3-digit number
    #         random_number = random.randint(100, 999)
            
    #         # Format the price_id
    #         price_id = f"P{current_year}{random_number}"

    #         return price_id

    def is_productExist(self, product_name, size, supplier):

        query = {
            "product_name": product_name,
            "cylinder_size": size,
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
    
    # def clearForm(self):
    #     for field in [self.prod_name_lineEdit, self.quantity_spinBox, self.price_lineEdit, self.supplier_lineEdit, self.desc_plainTextEdit]:
    #         field.clear()
    
    # def productExistNotif(self):
    #     self.prod_name_lineEdit.setText("Product Already Exist")
    #     self.prod_name_lineEdit.setStyleSheet("color: red")
    #     self.prod_name_lineEdit.setReadOnly(True)
    #     QTimer.singleShot(2000, lambda: self.prod_name_lineEdit.setStyleSheet("color: black"))
    #     QTimer.singleShot(2000, lambda: self.prod_name_lineEdit.setReadOnly(False))
    #     QTimer.singleShot(2000, lambda: self.clearForm())

    # def addItemBtn_clicked(self):
    #     print("add item button clicked")

    #     data = self.get_data()

    #     if self.is_data_empty():
    #         CustomMessageBox.show_message('information', 'Empty Fields', 'All fields are empty. Please fill out the form.')

    #     if not self.is_productExist():
    #         self.save(data)
    #         self.clearForm()
    #     else:
    #         self.productExistNotif()

    # def is_data_empty(self):
    #     fields = {
    #         "product_name": self.prod_name_lineEdit.text(),
    #         "supplier": self.supplier_lineEdit.text(),
    #         "price": self.price_lineEdit.text(),
    #         "quantity": self.quantity_spinBox.text(),
    #         "low_stock_threshold": self.low_stock_threshold_spinBox.text()
    #     }
        
    #     for key, value in fields.items():
    #         if key == "quantity" or key == "low_stock_threshold":
    #             # Check if quantity and low stock threshold are not zero
    #             if int(value) != 0:
    #                 return False
    #         elif value.strip():  
    #             # Check if other fields are not empty or whitespace
    #             return False
                
    #     return True  # Return True if all fields are empty or numeric fields are 0

    # def get_data(self):
    #     data = {
    #         "item_id": self.generate_id(),
    #         "product_name": self.prod_name_lineEdit.text(),
    #         "supplier": self.supplier_lineEdit.text(),
    #         "price": self.price_lineEdit.text(),
    #         "category": self.category_comboBox.currentText(),
    #         "status": self.status_comboBox.currentText(),
    #         "quantity": self.quantity_spinBox.text(),
    #         "description": self.desc_plainTextEdit.toPlainText(),
    #         "low_stock_threshold": int(self.low_stock_threshold_spinBox.text())
    #     }
    #     return data

    # def fill_form(self):
    #     # self.generate_id()
    #     self.validate_productID()
    #     self.update_comboBox()
    #     self.numberOnly()
    #     self.limitSupplierName()
    #     self.limitProductName()
        
    # def update_comboBox(self):
    #     self.cylinderSize_filter()
    #     self.itemStatus_filter()

    # def limitProductName(self):
    #     self.prod_name_lineEdit.setMaxLength(50)
    #     regex = QRegularExpression(r"^[a-zA-Z\s]+$")
    #     validator = QRegularExpressionValidator(regex)
    #     self.prod_name_lineEdit.setValidator(validator)

    # def limitSupplierName(self):
    #     self.supplier_lineEdit.setMaxLength(50) # set max lenght to 50 characters
        
    # def numberOnly(self):
    #     regex = QRegularExpression(r"^\d{1,4}(\.\d{1,3})?$")  # 1 to 4 digits before decimal, 1 to 3 digits after
    #     validator = QRegularExpressionValidator(regex)
    #     self.price_lineEdit.setValidator(validator)

    # def itemStatus_filter(self):
    #     with open(self.settings_dir, 'r') as f:
    #         data = json.load(f)

    #     self.status_comboBox.clear()
    #     for stat in data['item_status']:
    #         if list(stat.values())[0] != "":
    #             self.status_comboBox.addItem(list(stat.keys())[0])

    # def cylinderSize_filter(self):
    #     with open(self.settings_dir, 'r') as f:
    #         data = json.load(f)

    #     self.category_comboBox.clear()
    #     for category in data['cylinder_size']:

    #         value = list(category.values())[0]

    #         if value == "Show All":
    #             continue
    #         if value != "":
    #             self.category_comboBox.addItem(list(category.keys())[0])

    # def validate_productID(self):
    #     custom_id = self.generate_id()
    #     custom_id2 = self.generate_id()

    #     print(f"CUSTOM ID: {custom_id}")
    #     # print(f"CUSTOM ID 2: {custom_id2}")
    #     if not self.is_idExist(custom_id):
    #         self.productID_label.setText(custom_id)

    # def is_idExist(self, custom_id):
        # item_id = custom_id
        # filter = {
        #     "product_id": item_id
        # }
        # data = self.connect_to_db('products_items').find_one(filter)
        # if not self.connect_to_db('products_items').find_one(data):
        #     return True
        # else:
        #     return False
        
    def generate_id(self):
        """generate product id"""
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

    # def close_event(self, event):
    #     """Detect if the X button is clicked to close the form"""
    #     print("X button clicked")
    #     event.accept()
    #     self.close()

    def cancel_clicked(self):
        """Run when cancel button clicked"""
        self.close()