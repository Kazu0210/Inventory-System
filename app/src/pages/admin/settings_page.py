from PyQt6.QtWidgets import QWidget, QFileDialog, QCheckBox, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal
from src.ui.final_ui.settings import Ui_Form as Ui_settings_page
from src.custom_widgets.message_box import CustomMessageBox

import json, pymongo, os, datetime

class BackupEntireBDWorkerThread(QThread):
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    backup_done_signal = pyqtSignal(str, str)

    def __init__(self, **kwargs):
        super().__init__()

        self.selected_dir = kwargs.get('directory')

    def run(self):
        collection_names = [
            'account_archive',
            'accounts',
            'cart',
            'logs',
            'order_archive',
            'orders',
            'price_history',
            'prices',
            'product_archive',
            'sales'
        ]

        try:
            self.update_signal.emit("Starting backup...")
            date_today = datetime.datetime.today().strftime('%Y-%m-%d')  # Get date today
            folder_name = f'InventoryBackup_{date_today}'
            folder_dir = os.path.join(self.selected_dir, folder_name)
            
            # Create the folder if it doesn't exist
            if not os.path.exists(folder_dir):
                self.update_signal.emit('Creating folder for backup files')
                os.makedirs(folder_dir)  # Create folder in the specified directory
                print(f"Folder '{folder_name}' created successfully!")
                self.update_signal.emit(f'Folder ({folder_name}) created successfully!')
            else:
                print(f"Folder '{folder_name}' already exists.")
                self.update_signal.emit(f'Folder ({folder_name}) for backup files already exist.')

            # loop throught the collection name list
            for collection in collection_names:
                self.update_signal.emit(f'Creating {collection} collection backup.')
                total_document = self.connect_to_db(collection).count_documents({}) # get total document
                self.update_signal.emit(f'Total document: {total_document}')
                processed = 0
                self.update_signal.emit(f'Processed: {processed}')

                backup_data = [] # Initialize an empty list to hold all documents

                # Assuming you're iterating over the collection and processing documents
                save_dir_filename = f'{folder_dir}/{collection}_backup.json'

                with open(save_dir_filename, 'w') as backup_file:
                    # Iterate over documents in the collection
                    for doc in self.connect_to_db(collection).find({}).batch_size(100):
                        try:
                            # Check if '_id' is an ObjectId and convert it to a string
                            if isinstance(doc['_id'], dict) and '$oid' in doc['_id']:
                                doc['_id'] = str(doc['_id']['$oid'])
                            elif isinstance(doc['_id'], object):  # If it's an ObjectId directly
                                doc['_id'] = str(doc['_id'])

                            # Check for datetime fields and convert them
                            for key, value in doc.items():
                                if isinstance(value, datetime.datetime):
                                    doc[key] = value.isoformat()

                            # Append the document to the backup_data list
                            backup_data.append(doc)

                        except Exception as e:
                            print(f"Error processing document with _id {doc.get('_id', 'N/A')}: {e}")
                            continue
                        
                        # Update progress
                        processed += 1
                        progress = int((processed / total_document) * 100)
                        self.progress_signal.emit(progress)
                    
                    # Write all documents as a JSON array to the file
                    try:
                        json.dump(backup_data, backup_file, indent=4)
                    except Exception as e:
                        print(f"Error saving backup file: {e}")
                        CustomMessageBox.show_message('critical', 'Failed', f'Error saving backup file: {e}')

                    self.update_signal.emit(f'Backup for {collection} collection, created successfully!')
            
            self.backup_done_signal.emit('The system backup has been successfully created and stored.', f'{save_dir_filename}')
        except Exception as e:
            print(f'Error: {e}')

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]

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

    def get_checked_collections(self):
        """Retrieve the text of all checked checkboxes in the collections frame."""
        checked_collections = []

        # Iterate over all child widgets in the layout
        for i in range(self.collections_frame.layout().count()):
            widget = self.collections_frame.layout().itemAt(i).widget()  # Get the widget

            if isinstance(widget, QCheckBox) and widget.isChecked():  # Check if it's a QCheckBox and if it's checked
                checked_collections.append(widget.text())  # Add the text to the list

        return checked_collections

    def load_collection_names(self):
        """show all the collection names in the database for collections backup option"""
        collection_names = [
            'Accounts',
            'Archived Accounts',
            'Products',
            'Archived Products',
            'Sales',
            'Price History',
            'Logs',
            'Orders',
            'Prices',
        ]

        if not self.collections_frame.layout():
            layout = QVBoxLayout()  # Create layout if not already set
            self.collections_frame.setLayout(layout)  # Assign it to the frame
        else:
            layout = self.collections_frame.layout()  # Reuse the existing layout
            self.clear_layout(layout)  # Clear any existing widgets in the layout

        for collection in collection_names:
            checkbox = QCheckBox(collection)
            layout.addWidget(checkbox)  # Add checkboxes to the layout

    def clear_layout(self, layout):
        while layout.count():  # Check if there are widgets in the layout
            item = layout.takeAt(0)  # Take the first item
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Delete the widget if it exists
            # If the item contains a layout (nested layout), clear it recursively
            elif item.layout() is not None:
                self.clear_layout(item.layout())
    
    def clean_selected_collections(self, collections):
        """cleaned that selected collections to match the name of the collections in the database"""
        if collections:
            cleaned_collections = []
            collection_names = [
                'accounts',
                'account_archive',
                'products_items',
                'product_archive',
                'sales',
                'price_history',
                'logs',
                'orders',
                'prices',
            ]

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
            self.load_collection_names()
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

                self.worker = BackupEntireBDWorkerThread(directory=dir)
                self.worker.update_signal.connect(self.update_progress_label)
                self.worker.progress_signal.connect(self.update_progress_bar)
                self.worker.backup_done_signal.connect(self.show_done_signal)
                self.worker.start()
            else:
                CustomMessageBox.show_message('critical', 'Backup Cancelled', 'Backup cancelled')
            
        elif backup_option == 'collection':
            # get data from collections backup form
            format = self.CollectionBackupFormat_comboBox.currentText()
            dir = self.location2_lineEdit.text()
            print(f'Format: {format}, directory: {dir}')

            checked_collections = self.get_checked_collections()
            print(f'checked collections: {checked_collections}')
            self.clean_selected_collections(checked_collections)
        else:
            CustomMessageBox.show_message('critical', 'Error', 'Please select a backup option')

    def show_done_signal(self, message, directory):
        """show done signal"""
        CustomMessageBox.show_message('information', 'Backup Done', f'{message}\nFile name: {directory}')
        self.progressBar.setValue(0)
        self.backup_progress_label.setText('')

    def update_progress_bar(self, message):
        """update the progress bar"""
        self.progressBar.setValue(message)

    def update_progress_label(self, message):
        """update the progress label"""
        self.backup_progress_label.setText(str(message))

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