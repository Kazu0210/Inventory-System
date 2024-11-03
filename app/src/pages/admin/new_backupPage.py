from PyQt6.QtWidgets import QWidget, QMessageBox, QStackedLayout
from PyQt6.QtCore import Qt, pyqtSignal
from ui.NEW.new_backupSched_page import Ui_Form

from pages.admin.daily_backup_page import DailyBackup
from pages.admin.weekly_backup_page import WeeklyBackup
from pages.admin.monthly_backup_page import MonthlyBackup

import json, os

class NewBackupPage(QWidget, Ui_Form):
    # signals 
    cancel_signal = pyqtSignal(str)
    save_signal = pyqtSignal(str)

    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.loadAll()

        # buttons and comboBox
        self.frequency_comboBox.currentTextChanged.connect(lambda: self.changedForm())
        self.cancel_pushButton.clicked.connect(lambda: self.cancelButtonClicked())
        self.save_pushButton.clicked.connect(lambda: self.saveButtonClicked())

        # create layout
        self.scrollArea_layout = QStackedLayout(self.scrollArea)

        self.dailyBackupPage = DailyBackup(self) # index 0
        self.scrollArea_layout.addWidget(self.dailyBackupPage)

        self.weeklyBackupPage = WeeklyBackup(self) # index 1
        self.scrollArea_layout.addWidget(self.weeklyBackupPage)

        self.monthlyBackupPage = MonthlyBackup(self) # index 2
        self.scrollArea_layout.addWidget(self.monthlyBackupPage)

        # settings.json directory for saving backups
        self.settings_dir = "app/resources/config/settings.json"

    def saveMonthlyBackup(self):
        selected_date = self.monthlyBackupPage.calendarWidget.selectedDate()
        selected_date_str = selected_date.toString('dd') # only get the day

        try:
            # get time
            time_selection = self.monthlyBackupPage.timeEdit.time()
            time_str = time_selection.toString("hh:mm AP")

            # check if notification checkBox is Checked
            notification = self.monthlyBackupPage.enableNotif_checkBox.isChecked()

            # check if auto backup checkBox is checked
            auto_backup = self.monthlyBackupPage.enable_checkBox.isChecked()

            print(f'Selected time: {time_str}')
            print(f'Enable Backup: {auto_backup}')
            print(f'Get Notification: {notification}')

            new_backup = {
                "frequency": f"{self.getCurrentFrequency()}",
                "days": selected_date_str,
                "backup_time": time_str,
                "enable_backup": auto_backup,
                "enable_notification": notification
            }   

            # Read the existing data from the JSON file
            with open(self.settings_dir, "r") as json_file:
                data = json.load(json_file)

            # Append the new backup entry to the "backups" list
            data["backups_settings"].append(new_backup)

            # Write the updated data back to the JSON file
            with open(self.settings_dir, "w") as json_file:
                json.dump(data, json_file, indent=4)

            self.save_signal.emit(f"{self.getCurrentFrequency()} Backup Created Successfully.") # send signal to backp_restore.py
            QMessageBox.information(self, "Back Created", f"{self.getCurrentFrequency()} Backup Created Successfully.")
            self.close()

        except Exception as e:
            print(f"Error: {e}")

    def weeklyOneDay(self):
        # selected day
        selected_day = self.weeklyBackupPage.oneDay_comboBox.currentText()
        return selected_day
    
    def weeklyMultipleDay(self):
        # return multiple days
        page = self.weeklyBackupPage

        # Assuming each QCheckBox has a text label with the day name
        selected_days = [day.text() for day in [page.sunday_checkBox, page.monday_checkBox, page.tues_checkBox, page.wed_checkBox, page.thurs_checkBox, page.fri_checkBox, page.sat_checkBox] if day.isChecked()]
        return selected_days

    def saveWeeklyBackup(self):
        selection = None
        try:
            if self.weeklyBackupPage.oneDay_radioButton.isChecked():
                print('one day is checked')
                selection = self.weeklyOneDay()
            if  self.weeklyBackupPage.multipleDays_radioButton.isChecked():
                print('multiple days is checked')
                selection = self.weeklyMultipleDay()

            print(selection)

            # get time
            time_selection = self.weeklyBackupPage.timeEdit.time()
            time_str = time_selection.toString("hh:mm AP")

            # check if notification checkBox is Checked
            notification = self.weeklyBackupPage.enableNotif_checkBox.isChecked()

            # check if auto backup checkBox is checked
            auto_backup = self.weeklyBackupPage.enable_checkBox.isChecked()

            print(f'Selected time: {time_str}')
            print(f'Enable Backup: {auto_backup}')
            print(f'Get Notification: {notification}')

            new_backup = {
                "frequency": f"{self.getCurrentFrequency()}",
                "days": selection,
                "backup_time": time_str,
                "enable_backup": auto_backup,
                "enable_notification": notification
            }   

            # Read the existing data from the JSON file
            with open(self.settings_dir, "r") as json_file:
                data = json.load(json_file)

            # Append the new backup entry to the "backups" list
            data["backups_settings"].append(new_backup)

            # Write the updated data back to the JSON file
            with open(self.settings_dir, "w") as json_file:
                json.dump(data, json_file, indent=4)

            self.save_signal.emit(f"{self.getCurrentFrequency()} Backup Created Successfully.") # send signal to backp_restore.py
            QMessageBox.information(self, "Back Created", f"{self.getCurrentFrequency()} Backup Created Successfully.")
            self.close()

        except Exception as e:
            print(f"Error: {e}")

    def saveDailyBackup(self):
        try:
            # get time
            time_selection = self.dailyBackupPage.timeEdit.time()
            time_str = time_selection.toString("hh:mm AP")

            # check if notification checkBox is Checked
            notification = self.dailyBackupPage.enableNotif_checkBox.isChecked()

            # check if auto backup checkBox is checked
            auto_backup = self.dailyBackupPage.enable_checkBox.isChecked()

            print(f'Selected time: {time_str}')
            print(f'Enable Backup: {auto_backup}')
            print(f'Get Notification: {notification}')

            new_backup = {
                "frequency": "Daily",
                "days": "1",
                "backup_time": time_str,
                "enable_backup": auto_backup,
                "enable_notification": notification
            }   

            # Read the existing data from the JSON file
            with open(self.settings_dir, "r") as json_file:
                data = json.load(json_file)

            # Append the new backup entry to the "backups" list
            data["backups_settings"].append(new_backup)

            # Write the updated data back to the JSON file
            with open(self.settings_dir, "w") as json_file:
                json.dump(data, json_file, indent=4)

            self.save_signal.emit(f"{self.getCurrentFrequency()} Backup Created Successfully.") # send signal to backp_restore.py
            QMessageBox.information(self, "Back Created", "Daily Backup Created Successfully.")
            self.close()
        except Exception as e:
            print(f"Error: {e}")

    def saveButtonClicked(self):
        os.system('cls')
        print('Save button clicked')

        # get current frequency
        frequency = self.getCurrentFrequency()

        if frequency == "Daily":
            self.saveDailyBackup()
        elif frequency == "Weekly":
            self.saveWeeklyBackup()
        elif frequency == "Monthly":
            self.saveMonthlyBackup()

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
