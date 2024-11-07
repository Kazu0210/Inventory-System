from PyQt6.QtWidgets import QApplication, QLabel, QFrame, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import sys

class DragDropFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(2)

        # Set up a label
        self.label = QLabel("Drag a file here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up a layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Track drag state
        self.drag_in_progress = False
        self.drag_cancelled = False

    def dragEnterEvent(self, event):
        # If drag contains files, accept the drag
        if event.mimeData().hasUrls():
            self.drag_in_progress = True
            self.drag_cancelled = False
            event.acceptProposedAction()
            self.setStyleSheet('background-color: #D7D9D7;')
        else:
            self.drag_in_progress = False
            event.ignore()

    def dragLeaveEvent(self, event):
        # Drag left the widget area (this could imply cancellation)
        if self.drag_in_progress:
            self.drag_cancelled = True
            print("Drag was cancelled or left the widget area.")
            self.setStyleSheet('background-color: none;')
        self.drag_in_progress = False

    def dropEvent(self, event):
        # Handle the drop event
        if event.mimeData().hasUrls():
            file_url = event.mimeData().urls()[0]
            file_path = file_url.toLocalFile()
            self.label.setText(f"Dropped file path: {file_path}")
            self.drag_in_progress = False  # Reset the drag state
            self.setStyleSheet('background-color: none;')
        else:
            self.drag_cancelled = True  # If something unexpected happens during drop
            print("Drag drop was invalid or cancelled.")

    def getDragStatus(self):
        # Check if the drag event was cancelled or completed
        if self.drag_cancelled:
            print("Drag event was cancelled.")
        elif self.drag_in_progress:
            print("Drag event is ongoing.")
        else:
            print("No drag event occurred.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag-and-Drop Cancellation Detection")
        self.setGeometry(100, 100, 400, 200)
        
        frame = DragDropFrame()
        layout = QVBoxLayout()
        layout.addWidget(frame)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
