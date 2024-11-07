# BACKUP AND RESTORE PAGE for admin account
from PyQt6.QtWidgets import QWidget, QMessageBox, QListWidgetItem, QListWidget, QAbstractItemView
from PyQt6.QtCore import Qt
from ui.NEW.backupRestore_page import Ui_Form as Ui_backupRestore

from pages.admin.daily_backup_page import DailyBackup
from pages.admin.new_backupPage import NewBackupPage


import os, json, pymongo
from datetime import datetime

class BackupRestorePage(QWidget, Ui_backupRestore):
    def __init__(self, parent_window = None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # make the scroll on the list widget smoother
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.backupNow_pushButton.clicked.connect(lambda: self.backupNow_pushButton_clicked())
        self.setSched_pushButton.clicked.connect(lambda: self.setSched_pushButton_clicked())

        # run all function
        self.loadAll()

        # show schedules on list once
        self.showSchedList()

    def showSchedList(self):

        # get data from database
        collection = self.connect_to_db("auto_backup_sched")
        data = list(collection.find({}))
        
        for i in data:
            item = QListWidgetItem(self.listWidget)
            customItem = CustomListItem(i)

            # Set size hint to ensure QListWidgetItem matches custom widget size
            item.setSizeHint(customItem.sizeHint())

            self.listWidget.setItemWidget(item, customItem)

    def loadAll(self):
        self.fillFormatComboBox()
        # self.fillFrequencyComboBox()
        
    def setSched_pushButton_clicked(self):

        self.newBackupPage = NewBackupPage()
        self.newBackupPage.show()
        self.newBackupPage.cancel_signal.connect(lambda message: print(message))
        self.newBackupPage.save_signal.connect(lambda message: print(message))

    def getAccountsData(self):
        print('Getting data from accounts collection')
        data = list(self.connect_to_db("accounts").find({})) # convert cursor to list
        
        return data

    def getLogs(self):
        print('Getting data from logs collection')
        data = list(self.connect_to_db("logs").find({}))

        return data
    
    def getProducts(self):
        print('Getting data from products collection')
        data = list(self.connect_to_db("products_items").find({}))

        return data

    def getBackupFormat(self):
        return self.fileFormat_comboBox.currentText()
    
    def createBackup(self):
        print("Creating a backup")

        # Get backup file format
        backup_format = self.getBackupFormat()
        print(f"Backup format: {backup_format}")

        # Get current date
        current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M")

        # Retrieve all documents in the accounts collection
        accounts_data = self.getAccountsData()
        logs_data = self.getLogs()
        products_data = self.getProducts()

        # Prepare the backup data with timestamp and accounts data
        backup_data = {
            "backup_date": datetime.now().isoformat(),
            "accounts": accounts_data,
            "logs": logs_data,
            "products": products_data 
        }

        # Define the backup file name and save to JSON
        backup_name = f"backup_{current_date_time}{backup_format}"

        backup_dir = "app/resources/backup/"

        # Ensure the directory exist
        os.makedirs(backup_dir, exist_ok=True)

        backup_filename = os.path.join(backup_dir, backup_name)

        # FORMAT (backup_YYYY-MM-DD_HH-MM.sql)
        
        with open(backup_filename, 'w') as f:
            json.dump(backup_data, f, indent=4, default=str)  # default=str handles any MongoDB ObjectId or datetime fields

        print("Backup created")
        QMessageBox.information(self, "Backup Created", f'Backup "{backup_name}" created successfully.')

    def backupNow_pushButton_clicked(self):
        os.system('cls')
        print('Backup now button clicked')

        # call create backup function
        self.createBackup()

    def fillFormatComboBox(self):
        filter_dir = "app/resources/config/filters.json"

        with open(filter_dir, 'r') as f:
            data =  json.load(f)

        for format in data['backup_file_format']:
            self.fileFormat_comboBox.addItem(list(format.values())[0])

    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = collectionN
        return client[db][collection_name]
        
from ui.NEW.custom_listItem import Ui_Form as Ui_ListItem
class CustomListItem(QWidget, Ui_ListItem):
    def __init__(self, list_of_data):
        super().__init__()
        self.setupUi(self)

        self.data = list_of_data

        # set text to all the label
        self.setText()

    def setText(self):
        try:        
            # Set all the data on the labels
            self.schedID_label.setText(self.data.get('schedID', 'N/A'))
            self.freq_label.setText(self.data.get('frequency', 'N/A'))
            self.time_label.setText(self.data.get('backup_time', 'N/A'))

            # Check and set the checkboxes based on data
            self.enableAutoBackup_checkBox.setChecked(self.data.get('enable_backup', False))
            self.enableNotif_checkBox.setChecked(self.data.get('enable_notification', False))

        except KeyError as e:
            # Handle specific missing keys
            print(f"Error: Missing expected key in data: {e}")
            self.schedID_label.setText("Error: Missing data")

        except Exception as e:
            # Handle any other exceptions
            print(f"Unexpected Error: {e}")
            self.schedID_label.setText(f"Error: {e}")
