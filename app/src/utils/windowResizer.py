from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QGuiApplication

ASPECT_RATIO_WIDTH = 16
ASPECT_RATIO_HEIGHT = 9

class WindowResizer:
    def __init__(self, window: QWidget):
        self.window = window

    def resize_window(self):
        # Get the screen's resolution
        primary_screen = QGuiApplication.screens()[0]
        screen_width = primary_screen.availableGeometry().width()
        screen_height = primary_screen.availableGeometry().height()

        # Calculate the window's width and height to maintain 16:9 aspect ratio
        if screen_width / screen_height > ASPECT_RATIO_WIDTH / ASPECT_RATIO_HEIGHT:
            width = int(screen_height * ASPECT_RATIO_WIDTH / ASPECT_RATIO_HEIGHT)
            height = screen_height
        else:
            width = screen_width
            height = int(screen_width * ASPECT_RATIO_HEIGHT / ASPECT_RATIO_WIDTH)

        self.window.resize(width, height)