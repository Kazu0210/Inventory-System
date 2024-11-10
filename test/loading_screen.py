from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QTransform
import sys

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 300)  # Adjust size as needed
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Optional: Add a logo (if you have one)
        # logo = QLabel(self)
        # pixmap = QPixmap("path/to/your_logo.png").scaled(QSize(150, 150), Qt.AspectRatioMode.KeepAspectRatio)
        # logo.setPixmap(pixmap)
        # layout.addWidget(logo)

        # Spinning animation
        self.spinning_label = QLabel(self)
        self.spinning_pixmap = QPixmap("path/to/loading_icon.png").scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio)
        self.spinning_label.setPixmap(self.spinning_pixmap)
        self.angle = 0
        layout.addWidget(self.spinning_label)

        # Set up the timer for rotation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate_spinner)
        self.timer.start(50)  # Rotate every 50 ms for smooth spinning

        # Loading text
        self.text_label = QLabel("Loading, please wait...", self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label)

    def rotate_spinner(self):
        # Rotate the pixmap by updating the angle and applying a transformation
        self.angle += 10  # Adjust for faster/slower spin
        transform = QTransform().rotate(self.angle)
        rotated_pixmap = self.spinning_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.spinning_label.setPixmap(rotated_pixmap)

    def show_loading_screen(self):
        self.show()

    def close_loading_screen(self):
        self.timer.stop()  # Stop the spinning animation
        self.close()

# Example of how to use the Loading Screen in your main app
class MainApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.loading_screen = LoadingScreen()
        self.loading_screen.show_loading_screen()

        # Simulate a delay for loading (replace with actual loading logic)
        QTimer.singleShot(3000, self.on_loading_complete)  # 3-second delay

    def on_loading_complete(self):
        self.loading_screen.close_loading_screen()
        # Proceed to show the main window or other parts of your app here

if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec())
