from PyQt6.QtWidgets import QWidget, QMessageBox 
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
# from ui.NEW.restock_page import Ui_Form as Ui_restock_form
from src.ui.final_ui.restock_product import Ui_Form as Ui_restock_form
from src.custom_widgets.message_box import CustomMessageBox
from datetime import date
import pymongo

class RestockProduct(QWidget, Ui_restock_form):
    save_signal = pyqtSignal(dict)

    def __init__(self, data=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.received_data = data
        self.productID = self.received_data.get('product_id')

        self.collection = self.connect_to_db()

        print(f'data recieved by restock_page: {self.received_data}')

        self.fillUpForm()
        
        self.restock_quantity__lineEdit.textChanged.connect(lambda: self.UpdateTotalValue())

        self.cancel_pushButton.clicked.connect(lambda: self.cancelBtnClicked())
        self.restock_pushButton.clicked.connect(lambda: self.restockBtnClicked())

    def get_stock_level(self, stock_quantity: int, stock_threshold: int):
        """Return stock level (in stock, low stock, out of stock)"""
        
        if stock_quantity == 0:
            return "Out of Stock"
        elif stock_quantity < stock_threshold:
            return "Low Stock"
        else:
            return "In Stock"

    def save(self, data):
        current_date = date.today().strftime("%d-%m-%Y")
        try:
            fixed_data = {
                'product_id': data['product_id'],
                'product_name': data['product_name'],
                'cylinder_size': data['cylinder_size'],
                'quantity_in_stock': data['quantity'],
                'price_per_unit': data['price'],
                'supplier': data['supplier'],
                'last_restocked_date': current_date,
                'description': data['description'],
                'total_value': data['total_value'],
                'inventory_status': data['status'],
                'stock_level': self.get_stock_level(int(data['quantity']), int(self.received_data['minimum_stock_level']))
            }

            self.collection.update_one({"product_id": self.productID}, {"$set": fixed_data})
            CustomMessageBox.show_message('information', 'Success', 'Product Informatoin Udpated Successfully')
            self.save_signal.emit(data)
            self.close()
        except Exception as e:
            print('Error saving data to database', e)

    def restockBtnClicked(self):
        try:
            print(f'restock button clicked')

            newQuantity = self.getNewTotalQuantity()
            newTotalVal = self.getNewTotalVal()

            print(f'NEW TOTAL VALUE: {newTotalVal}')
            print(f'NEW QUANTITY: {newQuantity}')

            self.received_data['quantity'] = newQuantity
            print(f"ADDING NEW QUANTITY: {self.received_data['quantity']}")

            self.received_data['total_value'] = newTotalVal
            print(f"ADDING NEW TOTAL VALUE: {self.received_data['total_value']}")

            print(f'RECEIVED DATA FROM RESTOCK PAGE: {self.received_data}')
            # print(f'KLEPOOOORD: {self.received_data}')

            self.save(self.received_data)
        except Exception as e:
            print('Error restocking product', e)

    def getNewTotalQuantity(self):
        # combine old and new quantity
        newQuantity = int(self.restock_quantity__lineEdit.text())
        oldQuantity = int(self.received_data['quantity'])
        TotalQuantity = oldQuantity + newQuantity

        return TotalQuantity

    def getNewTotalVal(self):
        # combine old and new quantity
        newQuantity = int(self.restock_quantity__lineEdit.text())
        oldQuantity = int(self.received_data['quantity'])
        TotalQuantity = oldQuantity + newQuantity

        # get current price of the product
        currentPrice = int(self.received_data['price'])

        # get total value currentPrice x totalQuantity
        newTotalVal = currentPrice * TotalQuantity

        return newTotalVal

    def UpdateTotalValue(self):
        try:
            newQuantity = int(self.restock_quantity__lineEdit.text()) + int(self.received_data.get('quantity'))
            # print(f'new quantity: {newQuantity}')

            self.addQuantity_label.setText(f'+{self.restock_quantity__lineEdit.text()} = {newQuantity}') # set new added quantity to label

            totalValue = newQuantity * int(self.received_data.get('price'))
            # print(f'Total value: {totalValue}')
            self.total_cost_label.setText(f"₱ {totalValue:,.2f}")

            data = {
                'total_value': totalValue,
                'quantity_in_stock': str(newQuantity)
            }
            return data
        except Exception as e:
            print(f'Error: {e}')
            self.addQuantity_label.setText('')

    def numberOnly(self):
        regex = QRegularExpression(r"^\d{1,4}(\.\d{1,3})?$")  # 1 to 4 digits before decimal, 1 to 3 digits after
        validator = QRegularExpressionValidator(regex)
        self.restock_quantity__lineEdit.setValidator(validator)

    def fillUpForm(self):
        self.prod_ID_label.setText(self.received_data.get('product_id'))
        self.prod_name_label.setText(self.received_data.get('product_name'))
        self.cylinder_size_label.setText(self.received_data.get('cylinder_size'))
        self.restock_date_label.setText(self.received_data.get('restockDate'))
        self.supplier_label.setText(self.received_data.get('supplier'))
        self.price_label.setText(f"₱ {self.received_data.get('price'):,.2f}")
        self.total_cost_label.setText(str(self.received_data.get('total_value')))
        self.total_cost_label.setText(f"₱ {self.received_data.get('total_value'):,.2f}")
        self.quantity_label.setText(str(self.received_data.get('quantity')))

        self.numberOnly()

    def connect_to_db(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = "products"
        return client[db][collection_name]
    
    def cancelBtnClicked(self):
        self.close()