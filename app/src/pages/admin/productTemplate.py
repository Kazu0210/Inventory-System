from PyQt6.QtWidgets import QFrame
from ui.NEW.productTemplate import Ui_Frame

class ProductTemplate(QFrame, Ui_Frame):
    def __init__(self, parent_window, data):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        self.products_list = data

        document = self.getData()

        print(f"Received data from ProductTemplate: {document}")
        try:
            self.price_label.setText(document['price_per_unit'])
        except Exception as e:
            print(f"Error: {e}")

        
    def getData(self):
        return self.products_list
