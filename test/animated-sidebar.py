import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFrame, QStackedWidget, QHBoxLayout

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(200)  # Set sidebar width
        self.setStyleSheet("background-color: #333;")
        self.layout = QVBoxLayout(self)

        # Button to trigger dropdown
        self.toggle_button = QPushButton("Toggle Menu")
        self.toggle_button.setStyleSheet("background-color: #444; color: white;")
        self.toggle_button.clicked.connect(self.toggle_dropdown)

        self.layout.addWidget(self.toggle_button)

        # The dropdown menu (initially hidden)
        self.dropdown = QWidget()
        self.dropdown_layout = QVBoxLayout(self.dropdown)

        # Add buttons to the dropdown
        self.dropdown_buttons = [QPushButton(f"Button {i}") for i in range(1, 6)]
        for btn in self.dropdown_buttons:
            btn.setStyleSheet("background-color: #555; color: white; margin: 2px;")
            self.dropdown_layout.addWidget(btn)

        self.dropdown.setMaximumHeight(0)  # Initially collapsed

        self.layout.addWidget(self.dropdown)
        self.setLayout(self.layout)

    def toggle_dropdown(self):
        current_height = self.dropdown.height()
        target_height = 0 if current_height > 0 else len(self.dropdown_buttons) * 40  # 40px per button

        # Create an animation to expand or collapse the dropdown
        self.animation = QPropertyAnimation(self.dropdown, b"maximumHeight")
        self.animation.setDuration(150)  # Duration of the animation
        self.animation.setStartValue(current_height)
        self.animation.setEndValue(target_height)
        self.animation.start()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animated Sidebar")
        self.setGeometry(100, 100, 800, 600)

        # Create the sidebar
        self.sidebar = Sidebar()

        # Create a main widget and set the layout
        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addStretch(1)  # Push the sidebar to the left
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
