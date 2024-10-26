from PyQt6.QtWidgets import QWidget
from ui.employee.dashboard import Ui_Form as employee_dashboard_UI

class employee_dashboard(QWidget):
    def __init__(self):
        super(employee_dashboard, self).__init__()
        self.ui = employee_dashboard_UI()
        self.ui.setupUi(self)