from PyQt6.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtCore import QTimer, QThread, pyqtSignal
import sys
import time
import shutil

class BackupThread(QThread):
    progress_update = pyqtSignal(int)  # Signal to update the progress bar

    def __init__(self, source, destination):
        super().__init__()
        self.source = source
        self.destination = destination

    def run(self):
        # Simulate copying file in chunks and updating progress
        total_size = 100  # Assume total units for demonstration
        for i in range(1, total_size + 1):
            # Simulate time taken for each chunk (in real backup, handle file chunks here)
            time.sleep(0.05)
            self.progress_update.emit(int(i / total_size * 100))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backup with Loading Bar Example")
        
        # Set up progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        
        # Set up start button
        self.start_button = QPushButton("Start Backup")
        self.start_button.clicked.connect(self.select_backup)

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        # Set central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_backup(self):
        # Get source and destination paths
        source_file, _ = QFileDialog.getOpenFileName(self, "Select File to Backup", "", "All Files (*)")
        destination_folder = QFileDialog.getExistingDirectory(self, "Select Backup Destination")
        
        if source_file and destination_folder:
            # Define destination file path
            destination_file = f"{destination_folder}/backup_file"
            
            # Initialize the backup thread
            self.backup_thread = BackupThread(source_file, destination_file)
            self.backup_thread.progress_update.connect(self.progress_bar.setValue)
            self.backup_thread.finished.connect(self.backup_finished)
            
            # Start the backup
            self.progress_bar.setValue(0)  # Reset progress bar
            self.backup_thread.start()
    
    def backup_finished(self):
        # Update UI when backup is complete
        self.progress_bar.setValue(100)
        self.start_button.setText("Backup Complete")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
