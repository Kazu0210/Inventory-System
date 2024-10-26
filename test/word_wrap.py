from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy

app = QApplication([])

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QLabel
        self.label = QLabel("This is a long text that should wrap and adjust to the parent widget size.")

        # Enable word wrap to fit the text in the available width
        self.label.setWordWrap(True)

        # Set size policy to expand horizontally
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Create a layout and add the label
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # Set the layout to the widget
        self.setLayout(layout)

# Create and show the window
window = MyWidget()
window.show()

app.exec()
