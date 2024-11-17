from PyQt6.QtWidgets import QWidget

from ui.NEW.sales_report_page import Ui_Form

class SalesReportPage(QWidget, Ui_Form):
    def __init__(self, parent_window = None):
        super().__init__()
        self.setupUi(self)