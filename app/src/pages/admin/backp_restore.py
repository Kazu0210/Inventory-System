# BACKUP AND RESTORE PAGE for admin account
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from ui.NEW.backupRestore_page import Ui_Form as Ui_backupRestore

class BackupRestorePage(QWidget, Ui_backupRestore):
    def __init__(self, parent_window = None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
