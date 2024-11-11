from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class Profile(QWidget):
    def __init__(self, profile_name, parent=None):
        super().__init__(parent)
        
        self.name_label = QLabel(profile_name, self)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)