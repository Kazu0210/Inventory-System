from PyQt6.QtWidgets import QWidget

from ui.NEW.archive_page import Ui_Form as Ui_archive

import json, os, pymongo


class ArchivePage(QWidget, Ui_archive):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window

        # buttons connecion
        self.accounts_pushButton.clicked.connect(lambda: self.accounsBtnClicked())

    def loadTable(self, list_name):
        print(f'List name: {list_name}')

    def accounsBtnClicked(self):
        os.system('cls')
        print(f'Accounts button clicked')

        print('Loading table.')
        self.loadTable('account_archive')

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]