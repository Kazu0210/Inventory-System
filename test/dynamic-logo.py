from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class DynamicLogoApp(QWidget):
    def __init__(self):
        super().__init__()

        # QLabel for displaying the logo
        self.logo_label = QLabel(self)

        # Set up a vertical layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.logo_label)
        self.setLayout(layout)

        # Load and set the initial logo
        self.logo_pixmap = QPixmap("app/resources/icons/system-icon.png")
        self.update_logo()

        # Set window properties
        self.setWindowTitle("Dynamic Logo Resizing")
        self.resize(400, 300)

    def update_logo(self):
        """Update the logo size dynamically based on QLabel's current height."""
        if not self.logo_pixmap.isNull():
            max_height = self.logo_label.height()
            if max_height > 0:  # Ensure QLabel has a height before scaling
                scaled_logo = self.logo_pixmap.scaledToHeight(
                    max_height,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.logo_label.setPixmap(scaled_logo)

    def resizeEvent(self, event):
        """Recalculate the logo size whenever the window is resized."""
        self.update_logo()
        super().resizeEvent(event)


# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = DynamicLogoApp()
    window.show()
    app.exec()
