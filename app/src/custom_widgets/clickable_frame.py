from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent



import sys


class ClickableFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("background-color: lightblue;")
        self.setFixedSize(200, 150)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            print("Frame clicked!")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clickable Frame Example")
        self.setGeometry(100, 100, 400, 300)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Add a label for instructions
        label = QLabel("Click the frame below:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the clickable frame
        frame = ClickableFrame()

        # Add widgets to the layout
        main_layout.addWidget(label)
        main_layout.addWidget(frame)

        # Set the main widget
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
