import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Maintain Aspect Ratio')
        self.setGeometry(100, 100, 640, 360)  # Initial size in 16:9 ratio
        self.setMinimumSize(640, 360)  # Set the minimum size to 640x360

        layout = QVBoxLayout()
        button = QPushButton('Maximize', self)
        button.clicked.connect(self.showMaximized)
        layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def resizeEvent(self, event):
        new_width = event.size().width()
        new_height = event.size().height()
        aspect_ratio = 16 / 9

        if new_width / new_height != aspect_ratio:
            if new_width / aspect_ratio <= new_height:
                new_height = int(new_width / aspect_ratio)
            else:
                new_width = int(new_height * aspect_ratio)
            self.resize(new_width, new_height)

        super().resizeEvent(event)

app = QApplication(sys.argv)
window = MainWindow()
window.show()  # Show the window at its minimum size
sys.exit(app.exec())