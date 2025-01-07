from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from src.ui.NEW.monthly_backup_page import Ui_Form

class MonthlyBackup(QWidget, Ui_Form):
    # signals
    save_signal = pyqtSignal(dict)
    cancel_signal = pyqtSignal(str)

    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)

        self.calendarWidget.clicked.connect(self.showSelectedDate) # taga detect pag napindot yung date sa calendar widget, mag rrun yung self.showSelectedDate() pag na click yung date

        self.showSelectedDate()

    def showSelectedDate(self):
        selected_date = self.calendarWidget.selectedDate()

        date_str = selected_date.toString("dd") # taga convert the date to string
        self.selectedDate_label.setText(date_str) # ilalagay yung date sa label