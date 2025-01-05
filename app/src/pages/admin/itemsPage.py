from PyQt6.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QApplication, QAbstractItemView, QSplitter, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QColor
import pymongo
from bson import ObjectId
# from ui.inventoryPage import Ui_Form as items_page
from pages.admin.newitemsPage import newItem_page

from ui.NEW.inventory_page import Ui_Form as items_page

from pages.admin.edit_product_page import EditProductInformation
from pages.admin.restock_page import RestockProduct
# from ui.itemsPage import Ui_Form as items_page
# from docx import Document

from utils.Inventory_Monitor import InventoryMonitor

import time
import os
import re
import json
import datetime

class ItemsPage(QWidget, items_page):
    def __init__(self, username, dashboard_mainWindow):
        super().__init__()
        self.setupUi(self)
        self.dashboard_mainWindow = dashboard_mainWindow

        # new item button connection
        self.setItems.clicked.connect(lambda: self.open_add_product_form())
        # print button
        self.print_btn.clicked.connect(self.print_btn_clicked)

        self.collection = self.connect_to_db('products_items')

        self.tableWidget.itemSelectionChanged.connect(self.on_row_clicked)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

        # hide button
        self.HideButtons()

        # Call function that load all the filters once
        self.load_filters()

        # Initialize Inventory Monitor
        self.products_monitor = InventoryMonitor("products_items")
        self.products_monitor.start_listener_in_background()
        self.products_monitor.data_changed_signal.connect(self.update_all)

        # Call update_all function to populate table once
        self.update_all()

        # ComboBox connections
        self.cylinderSize_comboBox.currentTextChanged.connect(self.update_table)
        self.stock_level_comboBox.currentTextChanged.connect(self.update_table)

    def load_filters(self):
        """Add items to the filter dropdowns"""
        self.add_cylinder_size_filter()
        self.load_stock_level_filter()
    
    def load_stock_level_filter(self):
        """Add stock level filter to the dropdown"""
        filter_dir = "app/resources/config/filters.json"
        with open(filter_dir, 'r') as f:
            data = json.load(f)

        # clear combo box
        self.stock_level_comboBox.clear()

        for category in data['stock_level']:
            # print(f"CATEGORY: {list(category.values())[0]}")
            self.stock_level_comboBox.addItem(list(category.values())[0])

    def add_cylinder_size_filter(self):
        """Add cylinder size filter to the dropdown"""
        filter_dir = "app/resources/config/filters.json"
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

    def ShowButtons(self):
        self.restock_pushButton.show()
        self.editProduct_pushButton.show()
        self.archive_pushButton.show()
        
    def HideButtons(self):
        self.restock_pushButton.hide()
        self.editProduct_pushButton.hide()
        self.archive_pushButton.hide()

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

            product_header_dir = "app/resources/config/table/items_tableHeader.json"

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
        os.system('cls')

        if not self.object_id:
            print('Object ID is empty')
            return
        
        print(f'Received account id: {product_id}')
        
        # products archive collection
        archive_collection = self.connect_to_db('product_archive')

        data = list(self.collection.find({"product_id": product_id}, {"_id": 0}))
        print(f'Data collected using the Account id: {product_id}: {data}')
        
        selected_rows = self.tableWidget.selectionModel().selectedRows()

        reply = QMessageBox.question(
            self, 
            "Archive Confirmation", 
            "Are you certain you want to add this product to the archive?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            print('Clicked yes')

            # Get the ObjectId of the account to be deleted
            self.collection.delete_one({'_id': self.object_id})

            # Remove the row from the table
            row_index = selected_rows[0].row()
            self.tableWidget.removeRow(row_index)

            print(f"DATA NA KELANGAN KOOO: {data}")

            print(f'BAGONG DATA: {data}')

            try:
                # If data is a list, iterate over each dictionary
                if isinstance(data, list):
                    for item in data:
                        item['inventory_status'] = "Inactive"
                        archive_collection.insert_one(item)
                else:
                    # If data is a single dictionary, update it directly
                    data['inventory_status'] = "Inactive"
                    archive_collection.insert_one(data)
            except Exception as e:
                print(f"Error adding to archive: {e}")

            # Update the selected_row variable
            self.selected_row = None

            # Clear the account information section
            # self.username_label.setText("")
            # self.fname_label.setText("")
            # self.lname_label.setText("")
            # self.pass_label.setText("")
            # self.job_label.setText("")
            # self.usertype_label.setText("")
        
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

    def clearPreviewSection(self):
        self.productID_label.clear()
        self.productName_label.clear()
        self.cylinderSize_label.clear()
        self.quantity_label.clear()
        self.price_label.clear()
        self.supplier_label.clear()
        self.restockedDate_label.clear()
        self.description_label.clear()
        self.totalValue_label.clear()
        self.status_label.clear()
        self.stock_level_label.clear()
        self.low_stock_threshold_label.clear()

    def updatePreviewSection(self, data_dict):
        productID = data_dict.get('product_id')
        print(f'RECEIVED PRODUCT ID: {productID}')
        document = self.collection.find_one({'product_id': productID})
        print(f'DOKYUMENT: {document}')

        self.productID_label.setText(document['product_id'])
        self.productName_label.setText(document['product_name'])
        self.cylinderSize_label.setText(document['cylinder_size'])
        self.quantity_label.setText(str(document['quantity_in_stock']))
        self.price_label.setText(str(document['price_per_unit']))
        self.supplier_label.setText(document['supplier'])
        self.restockedDate_label.setText(document['last_restocked_date'])
        self.description_label.setText(document['description'])
        self.totalValue_label.setText(str(document['total_value']))
        self.status_label.setText(document['inventory_status'])
        self.low_stock_threshold_label.setText(str(document['minimum_stock_level']))

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
        self.update_low_stock_label()
        self.update_total_stock_label()

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

    # def CreateInventoryReport(self):
        # Get current time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print('Creating Inventory Report')

        # Create a new Document
        doc = Document()

        # Title
        doc.add_heading('Magtibay LPG Trading: Inventory Report', level=1)
        # Date
        doc.add_heading(f'Date: {current_time}', level=4)

        # Create a table
        # Assuming you want to include fields like Product ID, Product Name, Cylinder Size, Quantity, Price, etc.
        # Adjust the number of rows and columns based on your needs
        table = doc.add_table(rows=1, cols=8)

        # Define headers for the table
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Product ID'
        hdr_cells[1].text = 'Product Name'
        hdr_cells[2].text = 'Cylinder Size'
        hdr_cells[3].text = 'Quantity in Stock'
        hdr_cells[4].text = 'Price per Unit'
        hdr_cells[5].text = 'Supplier'
        hdr_cells[6].text = 'Last Restocked Date'
        hdr_cells[7].text = 'Total Value'

        # Example data to fill the table
        # You can replace this with your actual data
        inventory_data = [
            ['001', 'LPG Cylinder A', '14kg', '50', '800', 'Supplier A', '2024-10-15', '40000'],
            ['002', 'LPG Cylinder B', '11kg', '30', '750', 'Supplier B', '2024-10-10', '22500'],
            ['003', 'LPG Cylinder C', '5kg', '20', '400', 'Supplier C', '2024-10-12', '8000'],
        ]

        # Add inventory data to the table
        for item in inventory_data:
            row_cells = table.add_row().cells
            for i in range(len(item)):
                row_cells[i].text = item[i]
        # Save the document
        doc.save('Inventory Report.docx')

        print("Inventory Report created successfully!")

    def print_btn_clicked(self):
        print(f"Print button clicked.")
        # self.CreateInventoryReport()

    def update_table(self):
        table = self.tableWidget
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

        # header json directory
        header_dir = "app/resources/config/table/items_tableHeader.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)

        # set width of all the columns
        for column in range(table.columnCount()):
            table.setColumnWidth(column, 150)

        # Set uniform row height for all rows
        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

        header.setFixedHeight(50)

        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

        cylinder_size = self.cylinderSize_comboBox.currentText()
        stock_level = self.stock_level_comboBox.currentText()

        filter = {}

        if cylinder_size != "Show All":
            filter['cylinder_size'] = cylinder_size

        if stock_level != "Show All":
            filter['stock_level'] = stock_level

        data = list(self.collection.find(filter).sort("_id", -1))
        
        for row, item in enumerate(data):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)

                if value is not None:
                    if header == 'priceperunit' or header == 'totalvalue':
                        # Format value as price
                        formatted_price = f"₱ {int(value):,.2f}" if value else ""
                        value = formatted_price

                    # Check if the field is quantityinstock and get minimum_stock_level
                    if header == 'quantityinstock':
                        minimum_stock_level = item.get("minimum_stock_level")  # Assuming 'minimum_stock_level' exists in the document

                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text

                        # Highlight if the quantity is below the minimum stock level
                        if value < minimum_stock_level:
                            table_item.setForeground(QColor(255, 0, 0))  # Set text color to red, adjust RGB values as needed

                    else:
                        # For other columns
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    table.setItem(row, column, table_item)
                            


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

    
    # def switch_to_items_page(self):
    #     self.dashboard_mainWindow.content_window_layout.setCurrentIndex(5)

    def onCreateAccountBtnClicked(self):
        self.dashboard_mainWindow.content_window_layout.setCurrentIndex(0)

    def closeEditProductPage(self):
        if self.edit_product_page is not None:
            self.edit_product_page.close()
            self.edit_product_page = None


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = ItemsPage(None)  # Pass `None` if there's no `dashboard_mainWindow` for standalone testing
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())