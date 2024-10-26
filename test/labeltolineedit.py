from PyQt6.QtWidgets import QLabel, QLineEdit, QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Click Me!")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        self.clicked.emit()

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.label = ClickableLabel()
        self.layout.addWidget(self.label)
        
        self.label.clicked.connect(self.replace_with_lineedit)

    def replace_with_lineedit(self):
        self.line_edit = QLineEdit()
        self.line_edit.setText(self.label.text())  
        self.layout.replaceWidget(self.label, self.line_edit)  
        self.label.deleteLater()  

        self.save_button = QPushButton("Save")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_text)

        self.line_edit.setFocus()  

    def save_text(self):
        text = self.line_edit.text()
        self.layout.removeWidget(self.line_edit)
        self.line_edit.deleteLater()
        self.save_button.deleteLater()

        self.label = ClickableLabel()
        self.label.setText(text)
        self.layout.addWidget(self.label)
        self.label.clicked.connect(self.replace_with_lineedit)

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()