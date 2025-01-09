from PyQt6.QtWidgets import QWidget, QFileDialog
from src.ui.final_ui.settings import Ui_Form as Ui_settings_page
from src.custom_widgets.message_box import CustomMessageBox

import json

class settingsPage(QWidget, Ui_settings_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        # setting json file directory
        self.settings_dir = "D:/Inventory-System/app/resources/config/settings.json"
        self.filters_dir = "D:/Inventory-System/app/resources/config/filters.json"

        self.hide_widgets()
        self.load_btn_connections()
        self.load_current_time_format()
        self.load_backup_format_filters()

        self.timeFormat_comboBox.addItem("12hr")
        self.timeFormat_comboBox.addItem("24hr")

    def get_directory_backup_entire(self):
        """get the directory for the entire backup option. handles the browse file button click event"""
        dir = QFileDialog.getExistingDirectory(self, "Select Directory") # get directory using file dialog
        if dir:
            self.location1_lineEdit.setText(dir)

    def get_directory_backup_collections(self):
        """get the directory for the collections backup option. handles the browse file button click event"""
        dir = QFileDialog.getExistingDirectory(self, "Select Directory") # get directory using file dialog
        if dir:
            self.location2_lineEdit.setText(dir)

    def load_backup_format_filters(self):
        """insert options for backup format comboBox"""
        # clear comboBox first
        self.EntireBackupFormat_comboBox.clear()
        self.CollectionBackupFormat_comboBox.clear()

        try:
            with open(self.filters_dir, 'r') as f:
                data = json.load(f)

                filter = data['backup_file_format']
                
                for format_key in filter:
                    for key, value in format_key.items():
                        self.EntireBackupFormat_comboBox.addItem(value)
                        self.CollectionBackupFormat_comboBox.addItem(value)
        except Exception as e:
            print(f"Error: {e}")

    def load_current_time_format(self):
        """Get the current time format and display it using a label"""
        try:
            with open(self.settings_dir, 'r') as f:
                settings = json.load(f)

                current_time_format = settings['time_date'][0]['time_format']

                if current_time_format is not None:
                    self.current_time_format_label.setText(str(current_time_format))  # Set current time format label
        except Exception as e:
            print(f"Error: {e}")

    def on_radio_button_toggled(self):
        """Handle the radio button state change."""
        # Check which radio button is selected
        if self.BackupEntireDB_radioButton.isChecked():
            self.BackupEntireDb_frame.show()
            self.BackupSpecificCollection_frame.hide()
            self.current_backup_option = 'entire_db'
        elif self.BackupSpecifics_radioButton.isChecked():
            self.BackupEntireDb_frame.hide()
            self.BackupSpecificCollection_frame.show()
            self.current_backup_option = 'collection'

    def get_current_backup_option(self):
        """get the current backup option"""
        try:
            print(f'Current backup option: {self.current_backup_option}')
            return self.current_backup_option
        except Exception as e:
            print(f'Error: {e}')
    
    def start_backup_clicked(self):
        """handles the click event of start backup button"""
        # get the current backup option
        backup_option = self.get_current_backup_option()

        # get directory and file format
        if backup_option == 'entire_db':
            try:
                # get data from entire db backup form
                format = self.EntireBackupFormat_comboBox.currentText()
                dir = self.location1_lineEdit.text()
                
                if dir == '':
                    CustomMessageBox.show_message('information', 'Select Directory', 'Please select a directory to save the backup file')
                    return

            except Exception as e:
                CustomMessageBox.show_message('critical', 'Error', f'Error: {e}')
            
            question = CustomMessageBox.show_message('question', 'Confirm Backup', f'Are you sure you want to backup in {format} to {dir}?')

            if question == 1:
                CustomMessageBox.show_message('information', 'Backup started', 'Backup started')
            else:
                CustomMessageBox.show_message('critical', 'Backup Cancelled', 'Backup cancelled')
            
        elif backup_option == 'collection':
            # get data from collections backup form
            format = self.CollectionBackupFormat_comboBox.currentText()
            dir = self.location2_lineEdit.text()
            print(f'Format: {format}, directory: {dir}')

    def load_btn_connections(self):
        """load button connections"""
        self.change_format_pushButton.clicked.connect(lambda: self.show_change_format_widgets())
        self.update_format_pushButton.clicked.connect(lambda: self.handle_update_button())
        self.BackupEntireDB_radioButton.toggled.connect(self.on_radio_button_toggled)
        self.BackupSpecifics_radioButton.toggled.connect(self.on_radio_button_toggled)
        self.entireBrowseFile_pushButton.clicked.connect(lambda: self.get_directory_backup_entire())
        self.collectionBrowseFile_pushButton.clicked.connect(lambda: self.get_directory_backup_collections())
        self.start_backup_pushButton.clicked.connect(lambda: self.start_backup_clicked())

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
            self.current_time_format_label.show()
            self.load_current_time_format() # load current time format to reload the label

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
        self.current_time_format_label.hide()

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