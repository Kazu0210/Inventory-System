from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt


class CustomMessageBox(QDialog):
    def __init__(self, message_type: str, title: str, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(300, 150)

        # Disable resizing
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)

        # Icon for the message box
        icon_label = QLabel(self)
        if message_type == "information":
            icon_label.setText("ℹ️")  # Information icon (Unicode)
        elif message_type == "critical":
            icon_label.setText("❌")  # Critical icon (Unicode)
        elif message_type == "warning":
            icon_label.setText("⚠️")  # Warning icon (Unicode)
        elif message_type == "question":
            icon_label.setText("❓")  # Question icon (Unicode)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px;")  # Set icon size

        # Message label
        message_label = QLabel(message, self)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 14px; color: black;")

        # Layout for buttons
        button_layout = QHBoxLayout()

        # Buttons based on message type
        if message_type == "question":
            yes_button = QPushButton("Yes", self)
            yes_button.setStyleSheet(self.button_stylesheet())
            yes_button.clicked.connect(lambda: self.done(1))  # Return 1 for Yes
            button_layout.addWidget(yes_button)

            no_button = QPushButton("No", self)
            no_button.setStyleSheet(self.button_stylesheet())
            no_button.clicked.connect(lambda: self.done(0))  # Return 0 for No
            button_layout.addWidget(no_button)
        else:
            ok_button = QPushButton("OK", self)
            ok_button.setStyleSheet(self.button_stylesheet())
            ok_button.clicked.connect(self.accept)
            button_layout.addWidget(ok_button)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(icon_label)
        layout.addWidget(message_label)
        layout.addLayout(button_layout)

    def button_stylesheet(self):
        """Return a common stylesheet for buttons."""
        return """
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid black;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """

    @staticmethod
    def show_message(message_type: str, title: str, message: str, parent=None):
        """Convenience method to show the message box."""
        dialog = CustomMessageBox(message_type, title, message, parent)
        result = dialog.exec()
        return result


# # Example Usage
# if __name__ == "__main__":
#     app = QApplication([])

#     # Information message box
#     CustomMessageBox.show_message("information", "Information", "This is an information message.")

#     # Critical message box
#     CustomMessageBox.show_message("critical", "Critical Error", "A critical error occurred.")

#     # Warning message box
#     CustomMessageBox.show_message("warning", "Warning", "This is a warning message.")

#     # Question message box with two buttons
#     result = CustomMessageBox.show_message("question", "Confirmation", "Are you sure you want to continue?")
#     if result == 1:
#         print("User clicked Yes.")
#     else:
#         print("User clicked No.")

#     app.exec()