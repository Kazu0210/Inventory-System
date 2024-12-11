from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QToolTip
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor

class FollowCursorTooltipWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Follow Cursor Tooltip")
        self.resize(400, 300)


        # Create a QPushButton
        self.button = QPushButton("Hover over me", self)
        self.button.setToolTip("This tooltip follows the cursor!")
        self.button.setGeometry(150, 100, 150, 50)

        # Timer to update the tooltip's position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_tooltip_position)
        self.timer.start(50)  # Update every 50ms

    def update_tooltip_position(self):
        """Move the tooltip based on the cursor position."""
        cursor_pos = QCursor.pos()  # Get cursor position globally
        tooltip_rect = self.button.rect()
        tooltip_pos = self.mapFromGlobal(cursor_pos)

        # Check if the cursor is inside the button's area
        if tooltip_rect.contains(tooltip_pos):
            QToolTip.showText(cursor_pos, "This tooltip follows the cursor!", self.button)
        else:
            QToolTip.hideText()

# Run the application
app = QApplication([])
window = FollowCursorTooltipWidget()
window.show()
app.exec()
