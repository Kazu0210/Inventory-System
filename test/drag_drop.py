from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
import sys
import os

class DragDropWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag and Drop Example")
        self.setGeometry(100, 100, 400, 200)
        
        # Set up layout and label to display directory path
        layout = QVBoxLayout()
        self.label = QLabel("Drag a file here", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # Enable drag and drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # Check if dragged item contains file URLs
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the directory of the dropped file
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()[0]
            file_path = file_url.toLocalFile()  # Full file path
            directory_path = os.path.dirname(file_path)  # Directory of the file
            self.label.setText(f"Dropped file directory: {directory_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropWidget()
    window.show()
    sys.exit(app.exec())
