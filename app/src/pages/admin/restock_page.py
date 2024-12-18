from PyQt6.QtWidgets import QWidget, QMessageBox 
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from ui.NEW.restock_page import Ui_Form as Ui_restock_form
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
        
        self.restockQuantity_lineEdit.textChanged.connect(lambda: self.UpdateTotalValue())

        self.cancel_btn.clicked.connect(lambda: self.cancelBtnClicked())
        self.restock_pushButton.clicked.connect(lambda: self.restockBtnClicked())

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
            }

            self.collection.update_one({"product_id": self.productID}, {"$set": fixed_data})
            QMessageBox.information(self, 'Success', 'Product Information Updated Successfully')
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
        newQuantity = int(self.restockQuantity_lineEdit.text())
        oldQuantity = int(self.received_data['quantity'])
        TotalQuantity = oldQuantity + newQuantity

        return TotalQuantity


    def getNewTotalVal(self):
        # combine old and new quantity
        newQuantity = int(self.restockQuantity_lineEdit.text())
        oldQuantity = int(self.received_data['quantity'])
        TotalQuantity = oldQuantity + newQuantity

        # get current price of the product
        currentPrice = int(self.received_data['price'])

        # get total value currentPrice x totalQuantity
        newTotalVal = currentPrice * TotalQuantity

        return newTotalVal

    def UpdateTotalValue(self):
        try:
            newQuantity = int(self.restockQuantity_lineEdit.text()) + int(self.received_data.get('quantity'))
            # print(f'new quantity: {newQuantity}')

            self.addQuantity_label.setText(f'+{self.restockQuantity_lineEdit.text()} = {newQuantity}') # set new added quantity to label

            totalValue = newQuantity * int(self.received_data.get('price'))
            # print(f'Total value: {totalValue}')
            self.totalCost_label.setText(str(totalValue))

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
        self.restockQuantity_lineEdit.setValidator(validator)

    def fillUpForm(self):
        self.productID_label.setText(self.received_data.get('product_id'))
        self.productName_label.setText(self.received_data.get('product_name'))
        self.cylinderSize_label.setText(self.received_data.get('cylinder_size'))
        self.lastRestockD_label.setText(self.received_data.get('restockDate'))
        self.supplier_label.setText(self.received_data.get('supplier'))
        self.pricePerUnit_label.setText(str(self.received_data.get('price')))
        self.totalCost_label.setText(str(self.received_data.get('total_value')))
        self.quantityInStock_label.setText(str(self.received_data.get('quantity')))

        self.numberOnly()


    def connect_to_db(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = "products_items"
        return client[db][collection_name]
    
    def cancelBtnClicked(self):
        self.close()