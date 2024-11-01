# BACKUP AND RESTORE PAGE for admin account
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import Qt
from ui.NEW.backupRestore_page import Ui_Form as Ui_backupRestore

import os, json, pymongo
from datetime import datetime

class BackupRestorePage(QWidget, Ui_backupRestore):
    def __init__(self, parent_window = None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.backupNow_pushButton.clicked.connect(lambda: self.backupNow_pushButton_clicked())

        # run all function
        self.loadAll()

    def loadAll(self):
        self.fillFormatComboBox()
        self.fillFrequencyComboBox()

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
            print(f"JOB FILTERS: {list(format.values())[0]}")
            self.fileFormat_comboBox.addItem(list(format.values())[0])

    def fillFrequencyComboBox(self):
        settings_dir = "app/resources/config/settings.json"

        with open(settings_dir, 'r') as f:
            frequency = json.load(f)

        self.frequency_comboBox.clear()

        for fre in frequency['backup_frequency']:
            self.frequency_comboBox.addItem(list(fre.values())[0])

    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = collectionN
        return client[db][collection_name]
        