from PyQt6.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QApplication, QAbstractItemView
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

from ui.NEW.orders_page import Ui_orderPage_Form
from pages.admin.new_order_page import NewOrderPage
import pymongo

class OrderPage(QWidget, Ui_orderPage_Form):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # self.createOrder_pushButton.clicked.connect(lambda: self.createOrder())
        self.cancelOrder_pushButton.clicked.connect(lambda: print('cancel order button clicked'))
        self.editOrder_pushButton.clicked.connect(lambda: print('edit order button clicked'))
        self.orderHistory_pushButton.clicked.connect(lambda: print('order history button clicked'))

        if not hasattr(self, 'createOrderBtn_connected'):
            self.createOrder_pushButton.clicked.connect(lambda: self.createOrder())
            self.createOrderBtn_connected = True

    def createOrder(self):
        print(f'Create order button clicked')
        self.new_order_page = NewOrderPage()
        self.new_order_page.show()