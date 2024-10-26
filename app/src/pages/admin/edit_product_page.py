from PyQt6.QtWidgets import QWidget, QMessageBox 
from PyQt6.QtCore import pyqtSignal, Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from ui.NEW.edit_product_page import Ui_Form as editProductPage
import json, pymongo

class EditProductInformation(QWidget, editProductPage):
    # signals
    save_signal = pyqtSignal(dict)

    def __init__(self, data=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        print(f'DATA FROM EDIT PRODUCT PAGE: {data}')
        self.productID = data.get('product_id')
        self.productData = data
        print(f'PRODUCT ID: {self.productID}')

        self.cancel_btn.clicked.connect(lambda: self.cancelBtnClicked())
        self.save_btn.clicked.connect(lambda: self.saveBtnClicked())

        self.collection = self.connect_to_db() # connect to database
        self.fillupForm()

    def connect_to_db(self):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = "products_items"
        return client[db][collection_name]

    def saveNewData(self, data):
        try:
            self.collection.update_one({"product_id": self.productID}, {"$set": data})
            QMessageBox.information(self, 'Success', 'Product Information Updated Successfully')
            self.save_signal.emit(data)
            self.close()
        except Exception as e:
            print('Error saving data to database', e)

    def calculateTotalVal(self, currentProductPrice):
        data = self.collection.find_one({"product_id": self.productID})
        quantity_in_stock = data.get('quantity_in_stock')
        
        totalValue = int(currentProductPrice) * int(quantity_in_stock)
        return totalValue

    def saveBtnClicked(self):
        currentPrice = self.getData().get('price_per_unit')
        totalValue = self.calculateTotalVal(currentPrice)
        data = self.getData()
        data['total_value'] = totalValue
        self.saveNewData(data)

    def getData(self):
        print(f'Getting data from the form')
        data = {
            'product_id': self.productID_label.text(),
            'product_name': self.productName_field.text(),
            'cylinder_size': self.cylinderSize_comboBox.currentText(),
            'price_per_unit': self.pricePerUnit_field.text(),
            'supplier': self.supplier_field.text(),
            'description': self.description_field.text(),
            'inventory_status': self.status_comboBox_2.currentText(),
            'quantity_in_stock': self.quantity_lineEdit.text()
        }
        print(f'Data collected: {data}')
        return data
    
    def limitProductName(self):
        self.productName_field.setMaxLength(50)
        regex = QRegularExpression(r"^[a-zA-Z\s]+$")
        validator = QRegularExpressionValidator(regex)
        self.productName_field.setValidator(validator)

    def numberOnly(self):
        regex = QRegularExpression(r"^\d{1,4}(\.\d{1,3})?$")  # 1 to 4 digits before decimal, 1 to 3 digits after
        validator = QRegularExpressionValidator(regex)
        self.pricePerUnit_field.setValidator(validator)

    def fillupForm(self):
        # add validations and limitations
        self.limitProductName()
        self.numberOnly()

        # fills the form of the current information of the product/item
        self.productID_label.setText(self.productData.get('product_id'))
        self.productName_field.setText(self.productData.get('product_name'))
        self.cylinderSize_comboBox.addItem(self.productData.get('cylinder_size'))
        self.pricePerUnit_field.setText(self.productData.get('price'))
        self.supplier_field.setText(self.productData.get('supplier'))
        self.description_field.setText(self.productData.get('description'))
        self.status_comboBox_2.addItem(self.productData.get('status'))
        self.quantity_lineEdit.setText(self.productData.get('quantity'))

        self.UpdateComboBox('filters.json')

    def add_comboBox_options(self, directory_name, comboBox_name, option_name):
        filter_dir = f"app/resources/config/{directory_name}"

        print(f"ComboBox's current text: {comboBox_name.currentText()}")
        currentText = comboBox_name.currentText()

        with open(filter_dir, 'r') as f:
            options = json.load(f)

        for option in options[option_name]:
            # Get the first value from the option
            value = list(option.values())[0]

            # Skip adding "Show All"
            if value == "Show All":
                continue

            # Only add the item if it is not the current text
            if value != currentText:
                comboBox_name.addItem(value)
            else:
                # If the item matches the current text, do not add it (optional)
                print(f'Item "{value}" not added because it matches the current selection.')

    def UpdateComboBox(self, filter_filename):
        self.add_comboBox_options(filter_filename, self.cylinderSize_comboBox, 'cylinder_size')
        self.add_comboBox_options(filter_filename, self.status_comboBox_2, 'product_status')

    def cancelBtnClicked(self):
        self.close()