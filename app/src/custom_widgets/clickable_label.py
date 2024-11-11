from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSlot

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def mousePressEvent(self, event):
        self.clicked.emit()

    def clicked(self):
        print("Label clicked")