from PyQt6.QtWidgets import QWidget
from ui.NEW.prices_page import Ui_Form as Ui_price_page

class PricesPage(QWidget, Ui_price_page):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # show all prices in this page