from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QTextEdit, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Splitter Animation Example")

        # Main layout and splitter
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Add widgets to the splitter
        self.text_edit_1 = QTextEdit("Widget 1 (Collapsed by default)")
        self.text_edit_2 = QTextEdit("Widget 2")
        self.splitter.addWidget(self.text_edit_1)
        self.splitter.addWidget(self.text_edit_2)

        # Initially, collapse the first widget (set its size to 0)
        self.splitter.setSizes([0, 1])

        # Add a button to animate the first widget
        button = QPushButton("Expand First Widget")
        button.clicked.connect(self.animate_widget)

        # Add the splitter and button to the layout
        layout.addWidget(self.splitter)
        layout.addWidget(button)
        self.setCentralWidget(main_widget)

    def animate_widget(self):
        # Get the current size of the first widget (text_edit_1)
        start_width = self.text_edit_1.width()

        # Set the target width for the first widget (e.g., 200px)
        target_width = 200

        # Create the animation for the first widget's width
        animation = QPropertyAnimation(self.text_edit_1, b"geometry")
        animation.setDuration(1000)  # 1 second for animation
        animation.setStartValue(self.text_edit_1.geometry())  # Start position and size
        animation.setEndValue(QRect(self.text_edit_1.pos(), QSize(target_width, self.text_edit_1.height())))  # Target position and size
        
        # Start the animation
        animation.start()

        # Adjust the splitter sizes after animation
        animation.finished.connect(self.adjust_splitter_sizes)

    def adjust_splitter_sizes(self):
        # After the animation finishes, set the splitter sizes
        self.splitter.setSizes([200, 400])  # Adjust the sizes for both widgets

# Run the application
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
