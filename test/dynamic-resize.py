import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Widget Minimize/Maximize Example')

        # Main layout
        layout = QVBoxLayout(self)

        # Create four widgets with horizontal layout
        self.widget1 = self.create_widget("Widget 1", 200)
        self.widget2 = self.create_widget("Widget 2", 200)
        self.widget3 = self.create_widget("Widget 3", 200)
        self.widget4 = self.create_widget("Widget 4", 200)

        # Add widgets to main layout
        layout.addWidget(self.widget1)
        layout.addWidget(self.widget2)
        layout.addWidget(self.widget3)
        layout.addWidget(self.widget4)

        self.setLayout(layout)

    def create_widget(self, name, height):
        """Helper method to create a widget with a button inside to toggle minimize/maximize"""
        widget = QWidget(self)
        widget.setStyleSheet(f"background-color: lightblue;")
        widget.setFixedHeight(height)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create horizontal layout for the widget
        h_layout = QHBoxLayout(widget)

        # Create button to toggle minimize/maximize
        button = QPushButton("Minimize", widget)
        button.clicked.connect(lambda: self.toggle_widget(widget, button))

        # Add button to the horizontal layout
        h_layout.addWidget(button)
        widget.setLayout(h_layout)

        return widget

    def toggle_widget(self, widget, button):
        """Toggle the widget's height between minimized and maximized"""
        if widget.height() == 50:
            self.maximize_widget(widget, button)
        else:
            self.minimize_widget(widget, button)

    def minimize_widget(self, widget, button):
        """Minimize the widget by setting height to 50"""
        widget.setFixedHeight(50)
        button.setText("Maximize")  # Change the button text

    def maximize_widget(self, widget, button):
        """Maximize the widget by setting height to 200"""
        widget.setFixedHeight(200)
        button.setText("Minimize")  # Change the button text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWidget()
    window.resize(400, 600)  # Initial window size
    window.show()
    sys.exit(app.exec())
