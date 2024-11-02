from PyQt6.QtWidgets import QWidget, QMessageBox, QStackedLayout
from PyQt6.QtCore import Qt, pyqtSignal
from ui.NEW.new_backupSched_page import Ui_Form

from pages.admin.daily_backup_page import DailyBackup
from pages.admin.weekly_backup_page import WeeklyBackup
from pages.admin.monthly_backup_page import MonthlyBackup

import json

class NewBackupPage(QWidget, Ui_Form):
    # signals 
    cancel_signal = pyqtSignal(str)
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.loadAll()

        # buttons and comboBox
        self.frequency_comboBox.currentTextChanged.connect(lambda: self.changedForm())
        self.cancel_pushButton.clicked.connect(lambda: self.cancelButtonClicked())

        # create layout
        self.scrollArea_layout = QStackedLayout(self.scrollArea)

        dailyBackupPage = DailyBackup(self) # index 0
        self.scrollArea_layout.addWidget(dailyBackupPage)

        weeklyBackupPage = WeeklyBackup(self) # index 1
        self.scrollArea_layout.addWidget(weeklyBackupPage)

        monthlyBackupPage = MonthlyBackup(self) # index 2
        self.scrollArea_layout.addWidget(monthlyBackupPage)


    def changedForm(self):
        frequency = self.getCurrentFrequency()
        if frequency == "Daily":
            self.scrollArea_layout.setCurrentIndex(0)
        elif frequency == "Weekly":
            self.scrollArea_layout.setCurrentIndex(1)
        elif frequency == "Monthly":
            self.scrollArea_layout.setCurrentIndex(2)

    def getCurrentFrequency(self):
        # get current text from frequency comboBox
        print(f'Current Frequency: {self.frequency_comboBox.currentText()}')
        return self.frequency_comboBox.currentText()

    def cancelButtonClicked(self):
        self.cancel_signal.emit("Creating Daily Backup Cancelled.")
        self.close()

    def loadAll(self):
        self.fillFrequencyComboBox()

    def fillFrequencyComboBox(self):
        settings_dir = "app/resources/config/settings.json"

        with open(settings_dir, 'r') as f:
            frequency = json.load(f)

        self.frequency_comboBox.clear()

        for fre in frequency['backup_frequency']:
            self.frequency_comboBox.addItem(list(fre.values())[0])
