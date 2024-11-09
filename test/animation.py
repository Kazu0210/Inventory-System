from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect

app = QApplication([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)

        # Button to animate
        self.button = QPushButton("Fade Me", self)
        self.button.setGeometry(100, 100, 100, 50)

        # Set up opacity effect
        opacity_effect = QGraphicsOpacityEffect(self.button)
        self.button.setGraphicsEffect(opacity_effect)

        # Define the fade-out animation
        self.animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.animation.setDuration(300)  # Duration in milliseconds
        self.animation.setStartValue(1)   # Fully visible
        self.animation.setEndValue(0)     # Fully transparent
        self.animation.start()

window = MainWindow()
window.show()
app.exec()
