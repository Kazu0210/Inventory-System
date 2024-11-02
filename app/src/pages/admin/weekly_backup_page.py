from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from ui.NEW.weekly_backup_page import Ui_Form
import json

class WeeklyBackup(QWidget, Ui_Form):
    # signals
    save_signal = pyqtSignal(dict)
    cancel_signal = pyqtSignal(str)

    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)

        # hide days of the week options
        self.hideDays()

        # radio buttons
        self.oneDay_radioButton.toggled.connect(self.toggle_oneDay_frame)
        self.multipleDays_radioButton.toggled.connect(self.toggle_multipleDay_frame)

        # fillup comboBox
        self.fillDaysComboBox()

    def toggle_multipleDay_frame(self, checked):
        if checked:
            self.multipleDay_frame.show()
        else:
            self.multipleDay_frame.hide()

    def toggle_oneDay_frame(self, checked):
        if checked:
            self.oneDay_frame.show()
        else:
            self.oneDay_frame.hide()

    def hideDays(self):
        self.oneDay_frame.hide()
        self.multipleDay_frame.hide()

    def getData(self):
        # get time
        time_selection = self.timeEdit.time()
        time_string = time_selection.toString("hh:mm AP")

        # check if notification checkBox is Checked
        notification = self.enableNotif_checkBox.isChecked()

        # check if auto backup checkBox is checked
        auto_backup = self.enable_checkBox.isChecked()

        print(f'Selected time: {time_string}')
        print(f'Enable Backup: {auto_backup}')
        print(f'Get Notification: {notification}')

    def cancelButtonClicked(self):
        self.cancel_signal.emit("Creating Daily Backup Cancelled.")
        self.close()

    def fillDaysComboBox(self):
        settings_dir = "app/resources/config/settings.json"

        with open(settings_dir, 'r') as f:
            frequency = json.load(f)

        self.oneDay_comboBox.clear()

        for fre in frequency['days_in_week']:
            self.oneDay_comboBox.addItem(list(fre.values())[0])