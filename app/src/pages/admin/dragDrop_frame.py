from PyQt6.QtWidgets import QApplication, QLabel, QFrame, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
import sys, magic, os

class DragDropFrame(QFrame):
    # signal
    dropped_file_signal = pyqtSignal(bool)
    file_signal = pyqtSignal(dict)

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

        # Create magic instance
        self.file_magic = magic.Magic()

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
            # emit signal to show restore button
            self.dropped_file_signal.emit(True)
            
            try:
                file_url = event.mimeData().urls()[0]
                file_path = file_url.toLocalFile()  # Get the full path of the dropped file

                print(f'File path: {file_path}')
                file_name = os.path.basename(file_path)

                print(f'File name: {file_name}')

                # Get the file extension using os.path
                file_extension = os.path.splitext(file_path)[1].lower()  # Extract the extension and convert to lowercase

                print(f'File extension: {file_extension}')

                self.label.setText(file_name) # Set text label to dropped file name

                # emit signal to send file path etc. to backup_restore.py
                file = {
                    'file_path': file_path,
                    'file_name': file_name,
                }
                self.file_signal.emit(file)

                print(f'Is file type .json? {self.isJsonType(file_extension)}')

                if not self.isJsonType(file_extension):
                    self.dropped_file_signal.emit(False)
                    self.label.setText("Drag a file here")
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"File type {file_extension} is not supported."
                    )
                    file_url = None
                    file_path = None
                    file_name = None
                    file_extension = None

            except Exception as e:
                QMessageBox.information(
                    self,
                    "Error",
                    "Something went wrong. Please try again"
                )

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
        
    def isJsonType(self, file_extension):
        return file_extension == '.json'