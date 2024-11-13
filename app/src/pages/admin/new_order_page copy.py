from PyQt6.QtWidgets import QAbstractItemView, QWidget, QMessageBox, QComboBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QFrame, QPushButton, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression, QTimer
from PyQt6.QtGui import QRegularExpressionValidator
from ui.NEW.new_order_page import Ui_newOrder_Form
from pages.admin.productTemplate import ProductTemplate
from datetime import datetime
import pymongo, json, random

class NewOrderPage(QWidget, Ui_newOrder_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # self.productsCollection = self.connect_to_product_collection()

        print('this is from new order page')

        # set order date
        self.setOrderDateLabel()

        # BUTTONS
        # self.addItem_pushButton.clicked.connect(lambda: self.addItem())
        self.createOrder_pushButton.clicked.connect(lambda: self.createOrderBtn_clicked())
        # self.testAdd_pushButton.clicked.connect(lambda: self.testAddItem())

        # self.getItemFromDB()

        # # create a timer to update
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_all)
        # self.timer.start(1000)

        # self.updateProductsTable()
        # self.updateTable()

    def createOrderBtn_clicked(self):
        print("Create order button clicked")

    def setOrderDateLabel(self):
        current_date = datetime.now().date()
        self.orderDate_label.setText(str(current_date))

    # def testAddItem(self):
    #     print(f'Test add button clicked')
    #     currentRowCount = self.products_tableWidget.rowCount()
    #     name = "gasul"

    #     data = {
    #         'product_name': name
    #     }

    #     product_template = ProductTemplate(self, data)

    #     # Hide column header
    #     self.products_tableWidget.horizontalHeader().hide()
    #     self.products_tableWidget.verticalHeader().hide()

    #     # Ensure the table has only 1 column
    #     self.products_tableWidget.setColumnCount(1)
    #     # Add a new row
    #     self.products_tableWidget.insertRow(currentRowCount)

    #     # Set the QFrame (product_template) in the newly added row and first column
    #     self.products_tableWidget.setCellWidget(currentRowCount, 0, product_template)

    #     # Stretch the column to fill the entire width of the table
    #     self.products_tableWidget.horizontalHeader().setStretchLastSection(True)

    #     # Set column width and row height
    #     for column in range(self.products_tableWidget.columnCount()):
    #         self.products_tableWidget.setColumnWidth(column, self.products_tableWidget.viewport().width())

    #     # Ensure the row height is set to 200 for the newly added row
    #     self.products_tableWidget.setRowHeight(currentRowCount, 200)

    #     # Enable smooth scrolling
    #     self.products_tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    #     self.products_tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

    # def update_all(self):
    #     # self.updateTable()
    #     # self.updateProductsTable()
    #     pass
    
    # def updateTable(self):
    #     table = self.orderList_tableWidget
    #     vertical_header = table.verticalHeader()
    #     vertical_header.hide()
    #     table.setRowCount(0)  # Clear the table

    #     header_dir = "app/resources/config/table/cart_tableHeader.json"

    #     with open(header_dir, 'r') as f:
    #         header_labels = json.load(f)

    #     table.setColumnCount(len(header_labels))
    #     table.setHorizontalHeaderLabels(header_labels)

    #     # set width of all the columns
    #     for column in range(table.columnCount()):
    #         table.setColumnWidth(column, 200)
        
    # def getItemFromDB(self):
    #     products = self.productsCollection.find({})
    #     products_list = list(products)
    #     return products_list
    
    # def updateProductsTable(self):
    #     table = self.products_tableWidget
    #     table.verticalHeader().hide()
    #     table.horizontalHeader().hide()
    #     table.setRowCount(0)  # Clear the table
    #     table.horizontalHeader().setStretchLastSection(True)

    #     # Check if the column count is greater than zero before setting widths
    #     column_count = table.columnCount()
    #     if column_count > 0:
    #         # Calculate and set column widths
    #         column_width = table.viewport().width() // column_count
    #         for column in range(column_count):
    #             table.setColumnWidth(column, column_width)

    #     # Retrieve data from the database
    #     data = list(self.connect_to_product_collection().find({}))
    #     print("Retrieved data:", data)  # Debugging line
    #     if not data:
    #         print("No data found")  # Debugging line
    #         return

    #     # Populate the table with retrieved data
    #     for row_index, product_data in enumerate(data):
    #         table.insertRow(row_index)

    #         # Create a new ProductTemplate for each product
    #         product_template = ProductTemplate(self, product_data)
    #         print(f"Adding product template for row {row_index}: {product_data}")  # Debugging line
            
    #         # Set the ProductTemplate widget in the first column
    #         table.setCellWidget(row_index, 0, product_template)
            
    #         # Ensure the row height is set appropriately
    #         table.setRowHeight(row_index, 200)

    #     table.update()  # Force table update

    # def addItem(self):
    #     currentRowCount = self.orderList_tableWidget.rowCount()
    #     self.orderList_tableWidget.insertRow(currentRowCount)  # Add a new row

    #     randomNumber = random.randint(1, 100)

    #     # Set data in the first column
    #     self.orderList_tableWidget.setItem(currentRowCount, 0, QTableWidgetItem(f'Data: {randomNumber}'))

    #     # Create a QFrame
    #     frame1 = QFrame()
    #     frame1.setFrameShape(QFrame.Shape.Box)

    #     button = QPushButton("Remove")
    #     button.clicked.connect(lambda: self.removeItem(currentRowCount))

    #     layout = QVBoxLayout(frame1)
    #     layout.setContentsMargins(0,0,0,0)
    #     layout.addWidget(button)

    #     frame1.setLayout(layout)

    #     # Insert the QFrame into the second column of the new row
    #     self.orderList_tableWidget.setCellWidget(currentRowCount, 1, frame1)

    # def removeItem(self, row):
    #     # Remove the specified row
    #     self.orderList_tableWidget.removeRow(row)

    #     # Update all buttons in the remaining rows to ensure they connect to the correct row index
    #     for rowIndex in range(self.orderList_tableWidget.rowCount()):
    #         button = self.orderList_tableWidget.cellWidget(rowIndex, 1).findChild(QPushButton)
    #         button.clicked.disconnect()  # Disconnect the old signal
    #         button.clicked.connect(lambda checked, r=rowIndex: self.removeItem(r))  # Connect to the new row index


    # def connect_to_product_collection(self):
    #     connection_string = "mongodb://localhost:27017/"
    #     client = pymongo.MongoClient(connection_string)
    #     db = "LPGTrading_DB"
    #     collection_name = "products_items"
    #     return client[db][collection_name]
    
    def connect_to_orders_collection(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = "orders"
        return client[db][collection_name]