from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt6.QtCore import QPropertyAnimation, QRect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Slide-out Navbar Example")

        # Sidebar (Navbar)
        self.navbar = QWidget(self)
        self.navbar.setGeometry(0, 0, 200, 400)  # Initial width of 200
        self.navbar.setStyleSheet("background-color: lightgray;")

        # Button to toggle the sidebar
        self.button = QPushButton("Toggle Navbar", self)
        self.button.setGeometry(220, 10, 100, 30)  # Position the button outside of the navbar
        self.button.clicked.connect(self.toggle_navbar)

        # Flag to track navbar visibility
        self.navbar_visible = True

    def toggle_navbar(self):
        # Create the animation
        self.animation = QPropertyAnimation(self.navbar, b"geometry")
        self.animation.setDuration(100)  # Duration in milliseconds

        # Toggle between showing and hiding the navbar
        if self.navbar_visible:
            # Animate to hide the navbar (width to 0)
            self.animation.setStartValue(QRect(0, 0, 200, 400))  # Starting position (visible)
            self.animation.setEndValue(QRect(0, 0, 0, 400))      # Ending position (hidden)
        else:
            # Animate to show the navbar (width to 200)
            self.animation.setStartValue(QRect(0, 0, 0, 400))    # Starting position (hidden)
            self.animation.setEndValue(QRect(0, 0, 200, 400))    # Ending position (visible)

        # Start the animation
        self.animation.start()

        # Toggle the visibility flag
        self.navbar_visible = not self.navbar_visible

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
