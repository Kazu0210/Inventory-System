from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from src.ui.NEW.daily_backup_page import Ui_Form


class DailyBackup(QWidget, Ui_Form):
    # signals
    save_signal = pyqtSignal(dict)
    cancel_signal = pyqtSignal(str)

    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        
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