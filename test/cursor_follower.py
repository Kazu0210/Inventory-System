from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor

class CaretFollowerWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("I follow the caret!")
        self.setStyleSheet("background-color: yellow; padding: 5px; border-radius: 5px;")
        self.setFixedWidth(100)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

class CaretFollowerWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caret Follower Custom Widget")
        self.setGeometry(100, 100, 500, 400)  # Set window size

        # Create a QTextEdit widget (where the user will type)
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Type something here...")

        # Create the custom widget that will follow the caret
        self.custom_widget = CaretFollowerWidget(self)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.custom_widget)
        
        self.setLayout(layout)

        # Timer to update the widget's position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.follow_caret)
        self.timer.start(10)  # Update position every 20ms

    def follow_caret(self):
        cursor = self.text_edit.textCursor()
        if cursor.isNull():
            return
        
        # Get the caret's position
        cursor_rect = self.text_edit.cursorRect(cursor)

        # Add an offset to make the widget appear below the caret
        offset = 30  # Customize the offset (Y-axis)
        
        # Position the custom widget slightly below the caret
        self.custom_widget.move(cursor_rect.topLeft().x() + 10, cursor_rect.topLeft().y() + offset)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # Update position when user types (optional, in case key events need special handling)
        self.follow_caret()

if __name__ == "__main__":
    app = QApplication([])  # Create the application object
    window = CaretFollowerWindow()  # Create the window
    window.show()  # Show the window
    app.exec()  # Start the application event loop
