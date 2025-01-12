from PyQt6.QtWidgets import QFrame
from src.ui.NEW.create_account_requirements.email_requirements import Ui_Frame

class EmailAccountRequirementPage(QFrame, Ui_Frame):
    def __init__(self, parent_window):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        