from PyQt6.QtWidgets import QWidget, QMessageBox
from ui.final_ui.settings import Ui_Form as Ui_settings_page

from custom_widgets.message_box import CustomMessageBox

import json

class settingsPage(QWidget, Ui_settings_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        self.hide_widgets()
        self.load_btn_connections()

        # setting json file directory
        self.settings_dir = "app/resources/config/settings.json"

        self.timeFormat_comboBox.addItem("12hr")
        self.timeFormat_comboBox.addItem("24hr")

    def on_radio_button_toggled(self):
        """Handle the radio button state change."""
        # Check which radio button is selected
        if self.BackupEntireDB_radioButton.isChecked():
            self.BackupEntireDb_frame.show()
            self.BackupSpecificCollection_frame.hide()
        elif self.BackupSpecifics_radioButton.isChecked():
            self.BackupEntireDb_frame.hide()
            self.BackupSpecificCollection_frame.show()

    def load_btn_connections(self):
        """load button connections"""
        self.change_format_pushButton.clicked.connect(lambda: self.show_change_format_widgets())
        self.update_format_pushButton.clicked.connect(lambda: self.handle_update_button())
        self.BackupEntireDB_radioButton.toggled.connect(self.on_radio_button_toggled)
        self.BackupSpecifics_radioButton.toggled.connect(self.on_radio_button_toggled)

    def handle_update_button(self):
        """Handle click event for update time format button."""
        print("Update format button clicked")

        # Get the selected time format from the combo box
        time_format = self.timeFormat_comboBox.currentText()

        try:
            # Read the current settings from the JSON file
            with open(self.settings_dir, "r") as f:
                settings = json.load(f)

            # Update the time format
            if "time_date" in settings:
                settings["time_date"][0]["time_format"] = time_format
            else:
                settings["time_date"] = [{"time_format": time_format}]  # Add time_date if missing

            # Write the updated settings back to the file
            with open(self.settings_dir, "w") as file:
                json.dump(settings, file, indent=4)
                print("File updated successfully.")

            CustomMessageBox.show_message('information', 'Success', 'Time format updated successfully')

            self.hide_widgets()
            self.change_format_pushButton.show()

        except FileNotFoundError:
            print(f"Error: Settings file '{self.settings_dir}' not found.")
            CustomMessageBox.show_message('critical', 'Error', 'Settings file not found')
        except json.JSONDecodeError:
            print(f"Error: Settings file '{self.settings_dir}' contains invalid JSON.")
            CustomMessageBox.show_message('critical', 'Error', 'Settings file contains invalid JSON')
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            CustomMessageBox.show_message('critical', 'Error', 'An unexpected error occurred')

    def show_change_format_widgets(self):
        """show widgets to change time format"""
        self.update_format_pushButton.show()
        self.timeFormat_comboBox.show()

        # hide change format button 
        self.change_format_pushButton.hide()

    def hide_widgets(self):
        """hide widgets"""
        widgets = {
            self.update_format_pushButton,
            self.timeFormat_comboBox,
            self.BackupEntireDb_frame,
            self.BackupSpecificCollection_frame
        }
        for widget in widgets:
            widget.hide()