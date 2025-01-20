# BACKUP AND RESTORE PAGE for admin account
from PyQt6.QtWidgets import QWidget, QMessageBox, QListWidgetItem, QListWidget, QAbstractItemView, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal

from src.ui.NEW.backupRestore_page import Ui_Form as Ui_backupRestore
from src.utils.Inventory_Monitor import InventoryMonitor
# from src.pages.admin.daily_backup_page import DailyBackup
from src.pages.admin.new_backupPage import NewBackupPage
from src.pages.admin.dragDrop_frame import DragDropFrame
from src.utils.dir import ConfigPaths

import os, json, pymongo, plyer
from datetime import datetime
from plyer import notification

class BackupWorker(QObject):
    finished_signal = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path  # Path to the JSON file for backup

    def restoreDB(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            # Get the keys that hold arrays
            keys_with_array = self.get_keys_with_arrays(data)

            # Iterate over each key that holds an array of documents
            for key in keys_with_array:
                # Print the key for debugging purposes
                print(f'Inserting data for key: {key}')

                # Retrieve the array of documents (e.g., accounts, logs) from data[key]
                documents = data[key]

                # Insert data into MongoDB collection associated with the key
                if isinstance(documents, list):
                    # Insert multiple documents at once for arrays of documents
                    self.connect_to_db(key).insert_many(documents)
                else:
                    # Insert a single document if it’s not an array (unlikely in this structure but added for completeness)
                    self.connect_to_db(key).insert_one(documents)
        except Exception as e:
            print(f"Error restoring DB: {e}")
        finally:
            self.finished_signal.emit()

    def get_keys_with_arrays(self, data):
        # get keys with arrays (lists) as values
        keys_with_arrays = []

        if isinstance(data, dict):  # If the data is a dictionary, iterate through its keys
            for key, value in data.items():
                if isinstance(value, list):  # Check if the value is a list (array)
                    keys_with_arrays.append(key)
                elif isinstance(value, dict):  # If the value is a dictionary, recurse into it
                    keys_with_arrays.extend(self.get_keys_with_arrays(value))
        elif isinstance(data, list):  # If the data is a list, we can directly check each element
            for item in data:
                if isinstance(item, dict):
                    keys_with_arrays.extend(self.get_keys_with_arrays(item))
        
        return keys_with_arrays
    
    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = collectionN
        return client[db][collection_name]


class BackupRestorePage(QWidget, Ui_backupRestore):
    def __init__(self, parent_window = None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # make the scroll on the list widget smoother
        self.listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.backupNow_pushButton.clicked.connect(lambda: self.backupNow_pushButton_clicked())
        self.setSched_pushButton.clicked.connect(lambda: self.setSched_pushButton_clicked())
        self.restore_pushButton.clicked.connect(lambda: self.restore_pushButton_clicked())

        # initializa ConfigPaths
        self.directory = ConfigPaths
        # run all function
        self.loadAll()

        # show schedules on list once
        self.showSchedList()

        # set layout for dragdrop frame
        self.dragDrop_frame = DragDropFrame()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.dragDrop_frame)
        self.frame.setLayout(layout)

        # hide restore button on start on the program
        self.restore_pushButton.hide()

        # connect dragdrop frame signal
        self.dragDrop_frame.dropped_file_signal.connect(lambda message: self.handleDragDropSignal(message))

        self.dragDrop_frame.file_signal.connect(lambda message: self.getDroppedFileData(message))

        # Initialize inventory monitor
        self.backup_monitor = InventoryMonitor("auto_backup_sched")
        self.backup_monitor.start_listener_in_background()
        self.backup_monitor.data_changed_signal.connect(lambda: self.showSchedList())

    def restore_pushButton_clicked(self):
        print('Restore button clicked')
        print(f'File data: {self.dropped_file_data}')

        file_data = self.dropped_file_data
        if file_data:
            # Create the QThread and the Worker
            self.thread = QThread()
            self.backup_worker = BackupWorker(file_data['file_path'])

            # Move the worker to the thread and connect the signals
            self.backup_worker.moveToThread(self.thread)
            self.backup_worker.finished_signal.connect(self.on_backup_finished)
            
            # Connect the thread's started signal to the worker's run_backup method
            self.thread.started.connect(self.backup_worker.restoreDB)

            # Start the thread
            self.thread.start()

            # self.restoreDB(file_data['file_path'])
            # print('gumana')

    def on_backup_finished(self):
        # QMessageBox.information(
        #     self,
        #     "Backup Finished",
        #     "Backup has been successfully restored",
        # )

        notification.notify(
            title="LPG Trading Inventory System",
            message="Backup Created Successfully.",
            timeout=10
        )

    def getDroppedFileData(self, message):
        self.dropped_file_data = message

    def handleDragDropSignal(self, message):
        os.system('cls')
        print(f'File signal message: {message}')
        if message: 
            self.restore_pushButton.show()
        else:
            self.restore_pushButton.hide()

    def showSchedList(self):
        # clear list widget first
        self.listWidget.clear()
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

        # Get the current window username
        username = os.getlogin()

        backup_dir = f"C:/Users/{username}/Downloads"

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
        filter_dir = self.directory.get_path('filters')

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
    
from src.ui.NEW.custom_listItem import Ui_Form as Ui_ListItem
class CustomListItem(QWidget, Ui_ListItem):
    def __init__(self, list_of_data):
        super().__init__()
        self.setupUi(self)

        self.data = list_of_data

        # set text to all the label
        self.setText()

        self.enableAutoBackup_checkBox.clicked.connect(self.handleAutoBackupCheckBox)
        self.enableNotif_checkBox.clicked.connect(self.handleNotifCheckBox)

    def update_sched(self, sched_id, **kwargs):
        enable_backup = kwargs.get('enable_backup')
        disable_backup = kwargs.get('disable_backup')
        enable_notification = kwargs.get('enable_notification')
        disable_notification = kwargs.get('disable_notification')

        if sched_id:
            if enable_backup:
                self.connect_to_db('auto_backup_sched').update_one({'schedID': sched_id}, {'$set': {'enable_backup': enable_backup}})
            elif disable_backup:
                self.connect_to_db('auto_backup_sched').update_one({'schedID': sched_id}, {'$set': {'enable_backup': False}})
            if enable_notification:
                self.connect_to_db('auto_backup_sched').update_one({'schedID': sched_id}, {'$set': {'enable_notification': enable_notification}})
            elif disable_notification:
                self.connect_to_db('auto_backup_sched').update_one({'schedID': sched_id}, {'$set': {'enable_notification': False}})

    def handleNotifCheckBox(self):
        if self.enableNotif_checkBox.isChecked():
            response = QMessageBox.question(
                self,
                "Notification",
                "Do you want to enable notification for this schedule?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
            )
            if response == QMessageBox.StandardButton.Yes:
                try:
                    self.update_sched(self.data.get('schedID'), enable_notification=True) # update

                    self.enableNotif_checkBox.setChecked(True) # set checkBox to checked

                    # show notification
                    plyer.notification.notify(
                        title="Notification",
                        message="Backup schedule notification enabled",
                        timeout = 3
                    )
                except Exception as e:
                    print(e)
                    self.enableNotif_checkBox.setChecked(False)
                    return
            else:
                self.enableNotif_checkBox.setChecked(False)
                return
        else:
            response = QMessageBox.question(
                self,
                "Notification",
                "Do you want to disable notification for this schedule?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
            )
            if response == QMessageBox.StandardButton.Yes:
                try:
                    print('Disabling Auto backup')
                    print(f"Sched ID: {self.data.get('schedID')}")
                    self.update_sched(self.data.get('schedID'), disable_notification=True) # update

                    self.enableNotif_checkBox.setChecked(False)

                    plyer.notification.notify(
                        title="Notification",
                        message="Backup schedule notification enabled",
                        timeout = 3
                    )
                except Exception as e:
                    print(e)
                    self.enableNotif_checkBox.setChecked(True)
                    return
            else:
                self.enableNotif_checkBox.setChecked(True)
                return
            
            
    def handleAutoBackupCheckBox(self):
        if self.enableAutoBackup_checkBox.isChecked():
            response = QMessageBox.question(
                self,
                "Enable Auto Backup",
                f"Auto Backup enabled for {self.data.get('schedID')}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
            )

            if response == QMessageBox.StandardButton.Yes:
                try:
                    self.update_sched(self.data.get('schedID'), enable_backup=True) # update

                    self.enableAutoBackup_checkBox.setChecked(True) # set checkBox to checked

                    # show notification
                    plyer.notification.notify(
                        title="Enable Auto Backup",
                        message=f"Auto Backup enabled for {self.data.get('schedID')}",
                        timeout = 3
                    )
                except Exception as e:
                    print(e)
                    self.enableAutoBackup_checkBox.setChecked(False)
                    return
            else:
                self.enableAutoBackup_checkBox.setChecked(False)
                return
        else:
            response = QMessageBox.question(
                self,
                "Disable Auto Backup",
                f"Auto Backup disabled for {self.data.get('schedID')}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
            )
            if response == QMessageBox.StandardButton.Yes:
                try:
                    print('Disabling Auto backup')
                    print(f"Sched ID: {self.data.get('schedID')}")
                    self.update_sched(self.data.get('schedID'), disable_backup=True) # update

                    self.enableAutoBackup_checkBox.setChecked(False)

                    plyer.notification.notify(
                        title="Disable Auto Backup",
                        message=f"Auto Backup disabled for {self.data.get('schedID')}",
                        timeout = 3
                    )
                except Exception as e:
                    print(e)
                    self.enableAutoBackup_checkBox.setChecked(True)
                    return
            else:
                self.enableAutoBackup_checkBox.setChecked(True)
                return

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

    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        collection_name = collectionN
        return client[db][collection_name]