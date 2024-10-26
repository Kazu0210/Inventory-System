from PyQt6.QtWidgets import QWidget
from ui.settings_page import Ui_settings_page
import json

class settingsPage(QWidget, Ui_settings_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        # setting json file directory
        self.settings_dir = "app/resources/config/settings.json"

        self.timeFormat_comboBox.addItem("12hr")
        self.timeFormat_comboBox.addItem("24hr")
        self.timeFormat_comboBox.currentTextChanged.connect(self.check_timeFormat_setting)

    def check_timeFormat_setting(self, text):
        print(f"current time format: {text}")

        with open(self.settings_dir, 'r+') as f:
            settings = json.load(f)
            settings['time_date'][0]['time_format'] = text
            f.seek(0)
            json.dump(settings, f, indent=4)
            f.truncate()