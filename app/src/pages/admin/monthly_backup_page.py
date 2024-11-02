from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from ui.NEW.monthly_backup_page import Ui_Form
import json

class MonthlyBackup(QWidget, Ui_Form):
    # signals
    save_signal = pyqtSignal(dict)
    cancel_signal = pyqtSignal(str)

    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)

        self.calendarWidget.clicked.connect(self.showSelectedDate)
        
        self.showSelectedDate()
    def showSelectedDate(self):
        selected_date = self.calendarWidget.selectedDate()

        date_str = selected_date.toString("yyyy-MM-dd")

        self.selectedDate_label.setText(f"Selected Date: {date_str}")