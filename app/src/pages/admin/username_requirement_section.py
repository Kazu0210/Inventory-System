from PyQt6.QtWidgets import QFrame
from ui.NEW.create_account_requirements.username_requirements import Ui_Frame

class UsernameAccountRequirementPage(QFrame, Ui_Frame):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.parent_window = parent_window
        