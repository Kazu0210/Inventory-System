from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem,
    QVBoxLayout, QWidget, QLabel, QPushButton
)
import sys

# Custom widget to be added to the list
class CustomWidget(QWidget):
    def __init__(self, text):
        super().__init__()

        # Set up layout for the custom widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a label and a button and add them to the layout
        self.label = QLabel(text)
        self.button = QPushButton("Click Me")
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("QListWidget with Custom Widgets")
        self.setGeometry(100, 100, 300, 400)

        # Create the QListWidget
        self.list_widget = QListWidget()
        self.setCentralWidget(self.list_widget)

        # Add custom widgets to the QListWidget
        for i in range(5):
            # Create a QListWidgetItem
            item = QListWidgetItem(self.list_widget)
            
            # Create a custom widget with a unique label text
            custom_widget = CustomWidget(f"Item {i + 1}")
            
            # Set size hint to ensure QListWidgetItem matches custom widget size
            item.setSizeHint(custom_widget.sizeHint())
            
            # Add the custom widget to the QListWidget
            self.list_widget.setItemWidget(item, custom_widget)

# Main application execution
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
