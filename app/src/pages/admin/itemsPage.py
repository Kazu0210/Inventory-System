from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QCheckBox, QAbstractItemView, QFileDialog, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from fpdf import FPDF

from src.pages.admin.newitemsPage import newItem_page
from src.ui.NEW.inventory_page import Ui_Form as items_page
from src.pages.admin.edit_product_page import EditProductInformation
from src.pages.admin.restock_page import RestockProduct
from src.utils.Inventory_Monitor import InventoryMonitor
from src.custom_widgets.message_box import CustomMessageBox

import pymongo, os, re, json, datetime

class ItemsPage(QWidget, items_page):
    table_loading_signal = pyqtSignal(str)

    def __init__(self, username, dashboard_mainWindow):
        super().__init__()  
        self.setupUi(self)
        
        self.dashboard_mainWindow = dashboard_mainWindow

        self.is_updating_table = False  # Flag to track if the table is being updated

        self.collection = self.connect_to_db('products_items')

        self.load_filters()

        self.load_monitors()

        # Call update_all function to populate table once
        self.update_all()
        self.load_button_connections()

    def load_monitors(self):
        """load collection monitors"""
        self.products_monitor = InventoryMonitor("products_items")
        self.products_monitor.start_listener_in_background()
        self.products_monitor.data_changed_signal.connect(self.update_all)

    def print_btn_clicked(self):
        print(f"Print button clicked.")
        self.create_inventory_report()

    def create_inventory_report(self):
        """create inventory report"""
        try:
            # Fetch inventory data
            inventory_data = self.connect_to_db("products_items").find()

            # Initialize PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Title and Company Name
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(200, 10, txt="Magtibay LPG Trading", ln=True, align='C')  # Company Name
            pdf.ln(3)

            # Date and Time
            current_datetime = datetime.datetime.now()
            formatted_date = current_datetime.strftime("%b. %d, %Y")  # "Jul. 20, 2020" format
            formatted_time_print = current_datetime.strftime("%I:%M:%p")  # 12-hour format time with AM/PM (underscore separator)
            formatted_time = current_datetime.strftime("%I_%M_%p")  # 12-hour format time with AM/PM (underscore separator)
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 5, txt=f"Date: {formatted_date}", ln=True, align='C')  # Current Date
            pdf.cell(200, 5, txt=f"Time: {formatted_time_print}", ln=True, align='C')  # Current Time

            pdf.ln(10)

            # Title
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(200, 10, txt="Inventory Report", ln=True, align='C')
            pdf.ln(10)

            # Table headers
            pdf.set_font("Arial", style='B', size=12)
            headers = ["Product ID", "Product Name", "Cylinder Size", "Quantity", "Price/Unit", "Total Value"]
            for header in headers:
                pdf.cell(30, 10, txt=header, border=1, align='C')  # Centered text
            pdf.ln()

            # Table data
            pdf.set_font("Arial", size=10)
            for item in inventory_data:
                product_id = item["product_id"]
                product_name = item["product_name"]
                cylinder_size = item["cylinder_size"]
                quantity = item["quantity_in_stock"]
                price_per_unit = item["price_per_unit"]
                total_value = quantity * price_per_unit
                
                pdf.cell(30, 10, txt=str(product_id), border=1, align='C')  # Centered text
                pdf.cell(30, 10, txt=product_name, border=1, align='C')  # Centered text
                pdf.cell(30, 10, txt=str(cylinder_size), border=1, align='C')  # Centered text
                pdf.cell(30, 10, txt=str(quantity), border=1, align='C')  # Centered text
                pdf.cell(30, 10, txt=f"{price_per_unit:,.2f}", border=1, align='C')  # Centered text
                pdf.cell(30, 10, txt=f"{total_value:,.2f}", border=1, align='C')  # Centered text
                pdf.ln()

            # Open directory selection dialog
            folder = QFileDialog.getExistingDirectory(None, "Select Folder")

            if folder:
                # Save PDF with dynamic filename in the selected directory
                filename = f"{folder}/inventory_report_{formatted_date.replace(' ', '_').replace('.', '')}_{formatted_time}.pdf"
                pdf.output(filename)
                print(f"Report generated successfully! Filename: {filename}")
                CustomMessageBox.show_message(
                    'information',
                    'Inventory Report',
                    'Report generated successfully! Filename: ' + filename
                )
            else:
                print("No folder selected.")
                CustomMessageBox.show_message(
                    'information',
                    "No Folder Selected",
                    "Please select a folder to save the report."
                )
                
        except Exception as e:
            print(f'Error: {e}')
            CustomMessageBox.show_message(
                'critical',
                "Error",
                f"An error occurred while creating the report: {e}"
            )

    def load_filters(self):
        """Add items to the filter dropdowns"""
        self.add_cylinder_size_filter()
        self.load_stock_level_filter()
    
    def load_stock_level_filter(self):
        """Add stock level filter to the dropdown"""
        filter_dir = "D:/Inventory-System/app/resources/config/filters.json"
        with open(filter_dir, 'r') as f:
            data = json.load(f)

        # clear combo box
        self.stock_level_comboBox.clear()

        for category in data['stock_level']:
            self.stock_level_comboBox.addItem(list(category.values())[0])

    def add_cylinder_size_filter(self):
        """Add cylinder size filter to the dropdown"""
        filter_dir = "D:/Inventory-System/app/resources/config/filters.json"
        with open(filter_dir, 'r') as f:
            data = json.load(f)

        # clear combo box
        self.cylinderSize_comboBox.clear()

        for category in data['cylinder_size']:
            # print(f"CATEGORY: {list(category.values())[0]}")
            self.cylinderSize_comboBox.addItem(list(category.values())[0])

    def get_total_stock_quantity(self):
        """
        Fetch total stock quantity from the inventory collection.
        """
        try:
            # Aggregate to calculate total quantity
            total_quantity = self.connect_to_db("products_items").aggregate([
                {"$group": {"_id": None, "total_stock": {"$sum": "$quantity_in_stock"}}}
            ])

            # Fetch result and return total stock
            for result in total_quantity:
                return result['total_stock']
            
            # If no data exists
            return 0

        except Exception as e:
            print(f"Error: {e}")
            return None

    def update_total_stock_label(self):
        """Update the total stock quantity label"""
        total_stock_quantity = self.get_total_stock_quantity()
        print(f'Total stock quantity: {total_stock_quantity}')
        self.total_stock_quantity_label.setText(str(total_stock_quantity))

    def update_low_stock_label(self):
        """Updates the low stock label"""
        self.low_stock_label.setText(str(self.count_low_stock_products()))

    def count_low_stock_products(self):
        """
        Counts all products that have stock levels below their respective low stock threshold.

        :param inventory: The inventory data (a list of dictionaries).
        :return: The count of products with stock below their individual low stock threshold.
        """
        inventory = self.connect_to_db('products_items').find({})
        low_stock_count = 0
        
        # Iterate through each product in the inventory
        for product in inventory:
            # Check if the product's stock is below its low stock threshold
            if product['quantity_in_stock'] < product['minimum_stock_level']:
                low_stock_count += 1

        return low_stock_count

    def UpdateInventoryTotalValue(self):
        # Define the projection to include only the 'total_value' field
        filter_query = {"total_value": 1, "_id": 0}  # Include total_value, exclude _id

        # Retrieve documents from the collection with the specified projection
        data = list(self.collection.find({}, filter_query))
        
        # Print the retrieved data and add all the total value
        total_value = 0
        for TotalValue in data:
            total_value += TotalValue.get('total_value', 0)

        formated = f'{int(total_value):,.2f}'
        
        # set inventory total value label text
        self.inventoryTotalValue_label.setText(f"₱ {str(formated)}")
        
    def UpdateTotalStock(self):
        total_stock = str(self.collection.count_documents({}))
        self.inventoryTotalValue_label.setText(total_stock)

    def on_row_clicked(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        if selected_rows:

            row_index = selected_rows[0].row()
            print(f"Row {row_index} clicked")

            # self.restock_pushButton.show() # show restock button
            self.ShowButtons() # show buttons

            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_index, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")

            product_header_dir = "D:/Inventory-System/app/resources/config/table/items_tableHeader.json"

            with open(product_header_dir, 'r') as f:
                data = json.load(f)
                print(f'Data from items page (Table header): {data}')

            try:
                if 'Product ID' in data:
                    productID_header_index = data.index('Product ID')
                    print(f'Product id header index {productID_header_index}')
                else:
                    print("Column doesn't exist.")
            except Exception as e:
                print(f"An error occurred: {e}")

            document = self.collection.find_one({'product_id': row_data[productID_header_index]})
            # print(f"Data from items page (document): {document}")
            object_id = document['_id'] # get _id of product id
            # print(f'Object Id from items page: {object_id}')

            try:
                self.productID = document['product_id']
                self.productName = document['product_name']
                self.cylinderSize = document['cylinder_size']
                self.quantity = document['quantity_in_stock']
                self.price = document['price_per_unit']
                self.supplier = document['supplier']
                self.restockDate = document['last_restocked_date']
                self.description = document['description']
                self.totalValue = document['total_value']
                self.status = document['inventory_status']
                self.stock_level = document['stock_level']
                self.low_stock_threshold = document['minimum_stock_level']
            except Exception as e:
                print(f"Error: {e}")

            self.selected_row = row_index
            
            # update the object_id variable
            self.object_id = object_id

            self.productID_label.setText(self.productID)
            self.productName_label.setText(self.productName)
            self.cylinderSize_label.setText(str(self.cylinderSize))
            self.quantity_label.setText(str(self.quantity))

            formated_price = f'₱ {int(self.price):,.2f}'
            self.price_label.setText(str(formated_price))

            self.supplier_label.setText(self.supplier)
            self.restockedDate_label.setText(self.restockDate)
            self.description_label.setText(self.description)

            formated_total_val = f'₱ {int(self.totalValue):,.2f}'
            self.totalValue_label.setText(str(formated_total_val))

            self.status_label.setText(self.status)

            self.stock_level_label.setText(self.stock_level)

            self.low_stock_threshold_label.setText(str(self.low_stock_threshold))

            try:
                self.product_data = {
                    'product_id': self.productID,
                    'product_name': self.productName,
                    'cylinder_size': self.cylinderSize,
                    'quantity': self.quantity,
                    'price': self.price,
                    'supplier': self.supplier,
                    'restockDate': self.restockDate,
                    'description': self.description,
                    'total_value': self.totalValue,
                    'status': self.status,
                    'stock_level': self.stock_level,
                    'minimum_stock_level': self.low_stock_threshold
                }
            except Exception as e:
                print(f'Error: {e}')

            # Connect the edit button only once
            if not hasattr(self, 'edit_btn_connected'):
                if self.product_data.get('product_id') is not None:
                    self.editProduct_pushButton.clicked.connect(lambda: self.editProduct(self.product_data))
                    self.edit_btn_connected = True

            if not hasattr(self, 'restock_btn_connected'):
                if self.product_data.get('product_id') is not None:
                    self.restock_pushButton.clicked.connect(lambda: self.restockProduct(self.product_data))
                    self.restock_btn_connected = True

            if not hasattr(self, 'archive_btn_clicked'):
                if self.productID is not None:
                    self.archive_pushButton.clicked.connect(lambda: self.add_to_archive(self.productID))
                    self.archive_btn_clicked = True
        else:
            selected_rows = None
            self.product_data = None
            print('No row is selected')
            # self.restock_pushButton.hide()
            self.HideButtons()
            self.clearPreviewSection()

    def add_to_archive(self, product_id):
        print(f'Received product id: {product_id}')
        
        # products archive collection
        archive_collection = self.connect_to_db('product_archive')

        data_from_products_collection = list(self.connect_to_db('products_items').find({"product_id": product_id}, {"_id": 0}))
        print(f'Data collected using the Account id: {product_id}: {data_from_products_collection}')

        try:
            # If data is a list, iterate over each dictionary
            if isinstance(data_from_products_collection, list):
                for item in data_from_products_collection:
                    item['inventory_status'] = "Inactive"
                    archive_collection.insert_one(item)
            else:
                # If data_from_products_collection is a single dictionary, update it directly
                data_from_products_collection['inventory_status'] = "Inactive"
                archive_collection.insert_one(data_from_products_collection)
            self.update_table()

            self.connect_to_db('products_items').delete_one({'product_id': product_id})
        except Exception as e:
            print(f'Error: {e}')
        
    def restockProduct(self, product_data):
        print(f'Restock button clicked.')
        # print(f'Product data from restock button clicked: {product_data}')
        self.restockPage = RestockProduct(product_data)
        self.restockPage.show()
        self.restockPage.save_signal.connect(self.handleSave)

    def editProduct(self, product_data):
        print(f'Edit button clicked')
        print(f'product id from items page: {product_data}')
        self.editPage = EditProductInformation(product_data)
        self.editPage.show()
        self.editPage.save_signal.connect(self.handleSave)

    def handleSave(self, data):
        print('Edit product saved')
        print(f'data received from edit product page: {data}')
        self.updatePreviewSection(data)

    def on_item_clicked(self, item):
        row = self.tableWidget.row(item)
        self.tableWidget.selectRow(row)

    def update_all(self):
        self.update_table()
        self.UpdateTotalStock()
        self.UpdateInventoryTotalValue()
        # self.update_low_stock_label()
        self.update_total_stock_label()

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

    def get_products_data(self, filter):
        """Get prices data for prices table"""
        result = list(self.connect_to_db('products_items').find(filter).sort("_id", -1))
        
        # Rename 'product_name' to 'brand' in each item in the result
        for item in result:
            if 'product_name' in item:
                item['brand'] = item.pop('product_name')  # Rename the key

            if 'price_per_unit' in item:
                item['selling_price'] = item.pop('price_per_unit')
        return result
    
    def update_table(self):
        print('Loading inventory table')
        table = self.tableWidget

        # Set the flag to indicate the table is being updated
        self.is_updating_table = True

        # Temporarily block signals to prevent itemChanged from being emitted during table population
        table.blockSignals(True) 

        table.setRowCount(0)  # Clear the table
        table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)

        table.verticalHeader().setDefaultSectionSize(50)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
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

        vertical_header = table.verticalHeader()
        vertical_header.hide()
        header_dir = "D:/Inventory-System/app/resources/config/table/items_tableHeader.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setFixedHeight(40)

        for column in range(table.columnCount()):
            if column == 0:
                table.setColumnWidth(column, 20)
            else:
                table.setColumnWidth(column, 150)

        self.header_labels = [self.clean_header(header) for header in header_labels]

        cylinder_size = self.cylinderSize_comboBox.currentText()
        stock_level = self.stock_level_comboBox.currentText()

        filter = {}
        if cylinder_size != "Show All":
            filter['cylinder_size'] = cylinder_size

        if stock_level != "Show All":
            filter['stock_level'] = stock_level

        data = list(self.get_products_data(filter))

        for row, item in enumerate(data):
            table.setRowCount(row + 1)
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)

                if column == 0:  # Add checkbox to the first column
                    check_box = QCheckBox()
                    check_box.setChecked(False)  # Set initial checkbox state (unchecked)
                    check_box.setStyleSheet("""
                        QCheckBox {
                            font-size: 16px;
                            color: #2c3e50;
                            spacing: 10px;
                        }
                        QCheckBox::indicator {
                            width: 10px;
                            height: 10px;
                        }
                        QCheckBox::indicator:checked {
                            background-color: #27ae60;
                            border: 2px solid #2ecc71;
                        }
                        QCheckBox::indicator:unchecked {
                            background-color: #ecf0f1;
                            border: 2px solid #bdc3c7;
                        }
                    """)

                    # Create a layout to center the checkbox
                    layout = QHBoxLayout()
                    layout.addWidget(check_box)
                    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    # Create a QWidget to hold the layout and set it as the cell widget
                    widget = QWidget()
                    widget.setLayout(layout)
                    table.setCellWidget(row, column, widget)

                elif value is not None:
                    # For other columns, format the value (price, etc.)
                    if header == 'sellingprice' or header == 'supplierprice' or header == 'totalvalue':
                        formatted_price = f"₱ {int(value):,.2f}" if value else ""
                        value = formatted_price

                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, column, table_item)

        # table.hideColumn(0) # column for remove product
        table.hideColumn(1) # column for product id

        # Unblock signals after table is populated
        table.blockSignals(False)
        # Reset the flag once the table is updated
        self.is_updating_table = False

        # Now, connect the itemChanged signal to the handler function after loading is done
        table.itemChanged.connect(self.price_table_item_changed)

    def get_row_data(self):
        """Get all the checked rows in the table."""
        checked_rows = []
        for row in range(self.tableWidget.rowCount()):
            # Get the checkbox widget from the first column
            checkbox_widget = self.tableWidget.cellWidget(row, 0)

            if checkbox_widget:
                # Extract the QCheckBox from the widget
                check_box = checkbox_widget.layout().itemAt(0).widget()

                # Check if the checkbox is checked
                if check_box.isChecked():
                    row_data = {}
                    # Get quantity and price values
                    quantity_widget = self.tableWidget.item(row, 1)  # Assuming quantity is in column 1
                    price_widget = self.tableWidget.item(row, 2)     # Assuming price is in column 2

                    # Retrieve the text (or data) from quantity and price cells
                    row_data['Row'] = row
                    row_data['product_id'] = quantity_widget.text() if quantity_widget else ''
                    row_data['brand'] = price_widget.text() if price_widget else ''

                    checked_rows.append(row_data)

        return checked_rows

    def remove_button_clicked(self):
        """handle click event for the remove products button"""
        checked_rows = self.get_row_data()
        print(f'Checked Rows: {checked_rows}')

        # extract all the product id
        product_ids = []
        for data in checked_rows:
            print(data['product_id'])
            product_ids.append(data['product_id'])

        if product_ids:
            result = CustomMessageBox.show_message('question', 'Archive', 'The selected products will be archived. Are you sure?')
            if result == 1:
                for id in product_ids:
                    self.add_to_archive(id)



    def price_table_item_changed(self, item):
        """Handles the price table item changed event"""
        try:
            if self.is_updating_table:
                # If the table is being updated, don't handle item changes
                print('Table is being updated, ignoring item change.')
                return

            self.tableWidget.blockSignals(True)  # Temporarily block signals to avoid recursion

            new_value = item.text()
            column = item.column()
            row = item.row()

            print(f"Item changed: Row {row}, Column {column}, New Value: {new_value}")

            product_id = self.tableWidget.item(row, 1).text()
            header = self.tableWidget.horizontalHeaderItem(column)
            cleaned_header = header.text().replace(' ', '_').lower()

            print(f"Product ID: {product_id}, Header: {cleaned_header}")

            if product_id:
                if cleaned_header == 'quantity_in_stock':
                    try:
                        total_value = self.calculate_total_value_from_quantity(product_id, new_value)
                        filter = {'product_id': product_id}
                        update = {"$set": {cleaned_header: int(new_value), "total_value": total_value}}
                        self.connect_to_db('products_items').update_one(filter, update)
                    except Exception as e:
                        print(f'Error: {e}')
                elif cleaned_header == 'selling_price':
                    try:
                        total_value = self.calculate_total_value_from_selling_price(product_id, new_value)
                        filter = {'product_id': product_id}
                        update = {"$set": {"price_per_unit": float(new_value), "total_value": total_value}}
                        self.connect_to_db('products_items').update_one(filter, update)
                    except Exception as e:
                        print(f'Error: {e}')
                elif cleaned_header == 'supplier_price':
                    try:
                        filter = {'product_id': product_id}
                        update = {"$set": {"supplier_price": float(new_value)}}
                        self.connect_to_db('products_items').update_one(filter, update)
                    except Exception as e:
                        print(f'Error: {e}')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.tableWidget.blockSignals(False)  # Re-enable signals after processing

    def calculate_total_value_from_quantity(self, product_id, quantity):
        """calculate the total value"""
        filter = {'product_id': product_id}
        projection = {'_id': 0}
        result = list(self.connect_to_db('products_items').find(filter, projection))
        if result:
            for data in result:
                price = data.get('price_per_unit', '')
        return float(quantity) * float(price)

    def calculate_total_value_from_selling_price(self, product_id, selling_price):
        """calculate the total value"""
        filter = {'product_id': product_id}
        projection = {'_id': 0}
        result = list(self.connect_to_db('products_items').find(filter, projection))
        if result:
            for data in result:
                quantity = data.get('quantity_in_stock', '')
        return float(quantity) * float(selling_price)

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
            return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))
    
    def open_add_product_form(self):
        """Open add product form"""
        print('gumana')
        self.addProduct = newItem_page()
        self.addProduct.show()
        # self.addProduct.save_signal.connect(self.handleSave)

    def onCreateAccountBtnClicked(self):
        self.dashboard_mainWindow.content_window_layout.setCurrentIndex(0)

    def closeEditProductPage(self):
        if self.edit_product_page is not None:
            self.edit_product_page.close()
            self.edit_product_page = None

    def load_button_connections(self):
        """load button, comboBox etc connections"""
        # ComboBox connections
        self.cylinderSize_comboBox.currentTextChanged.connect(self.update_table)
        self.stock_level_comboBox.currentTextChanged.connect(self.update_table)
        # new item button connection
        self.setItems.clicked.connect(lambda: self.open_add_product_form())
        self.print_btn.clicked.connect(lambda: self.print_btn_clicked())
        self.remove_product_pushButton.clicked.connect(lambda: self.remove_button_clicked())