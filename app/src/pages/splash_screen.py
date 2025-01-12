from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap


from src.ui.final_ui.splash_screen import Ui_Form as Ui_splash_screen

class WorkerThread(QThread):
    update_progress = pyqtSignal(str)

class SplashScreen(QWidget, Ui_splash_screen):
    def __init__(self, user_role, username):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.insert_logo()

        print(f'user role: {user_role}\nusername: {username}')

    def load_admin_dashboard(self):
        """load admin dashboard"""

    def update_progress_bar(self):
        """update value of the progress bar"""
        current_value = self.progressBar.value()
        print(f"Current value: {current_value}")

    def insert_logo(self):
        """insert logo"""
        logo = QPixmap("D:/Inventory-System/app/resources/icons/system-icon.png")
        
        min_height = 180  # Minimum height
        max_height = 200  # Maximum height

        # Calculate the height of the QLabel
        current_height = self.logo.height()

        # Ensure the height stays within the defined range
        height_to_use = max(min_height, min(max_height, current_height))

        # Scale the pixmap to the computed height while maintaining aspect ratio
        scaled_logo = logo.scaledToHeight(height_to_use, Qt.TransformationMode.SmoothTransformation)

        # Set the scaled pixmap to the QLabel
        self.logo.setPixmap(scaled_logo)

        # Ensure the QLabel does not distort the pixmap
        self.logo.setScaledContents(True)