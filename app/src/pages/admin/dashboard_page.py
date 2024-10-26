from PyQt6.QtWidgets import *
from ui.dashboard_page import Ui_Form as Ui_dashboard_page
from utils.DB_checker import db_checker
from PyQt6.QtCore import QThread, pyqtSignal

class Dashboard(QWidget, Ui_dashboard_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        # database
        self.checker = db_checker("mongodb://localhost:27017/", "LPGTrading_DB")
        self.checker.connect_to_client()
        self.checker.check_db_exist()
        self.checker.connect_to_db()
        self.collection_name = 'products_items'

        self.document = self.checker.db[self.collection_name].find({})

        # for doc in self.document:
        #     print(doc)

        # print(f'collection name: {self.checker.db[self.collection_name]}')

        # create a thread to always update the table
        self.update_thread = UpdateThread(self.checker.db[self.collection_name])
        self.update_thread.updated.connect(self.update_total_stock_label)
        self.update_thread.start()

        # set layout
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)

        self.total_stock_label = QLabel()
        self.verticalLayout.addWidget(self.total_stock_label)
        self.update_total_stock_label()

    def update_total_stock_label(self, total_stock=None):
        if total_stock is None:
            total_stock = self.get_total_stock()
        self.total_stock_label.setText(f"Total Stock: {total_stock}")

    def get_total_stock(self):
        try:
            total_stock = self.checker.db[self.collection_name].count_documents({})
            return total_stock
        except Exception as e:
            print(f"Error getting total stock: {e}")
            return 0

    def closeEvent(self, event):
        self.update_thread.stop()
        event.accept()

class UpdateThread(QThread):
    updated = pyqtSignal(int)

    def __init__(self, collection):
        super().__init__()
        self.collection = collection
        self.running = True

    def run(self):
        while self.running:
            try:
                total_stock = self.collection.count_documents({})
                self.updated.emit(total_stock)
            except Exception as e:
                print(f"Error updating total stock: {e}")
            QThread.msleep(1000)

    def stop(self):
        self.running = False