from PyQt6.QtWidgets import QWidget
from src.ui.employee.dashboard_page import Ui_Form as dashboard_employee_page

class employee_dashboard(QWidget):
    def __init__(self):
        super(employee_dashboard, self).__init__()
        self.ui = dashboard_employee_page()
        self.ui.setupUi(self)