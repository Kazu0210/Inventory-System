import sys
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtCore import QPropertyAnimation, pyqtProperty, QVariant
from PyQt6.QtGui import QColor, QPalette

class AnimatedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.hover_color = QColor("red")
        self.normal_color = QColor("#f0f0f0")

    def enterEvent(self, event):
        self.animate_color(self.hover_color)

    def leaveEvent(self, event):
        self.animate_color(self.normal_color)

    def animate_color(self, color):
        animation = QPropertyAnimation(self, b"backgroundColor")
        animation.setDuration(200)
        animation.setStartValue(self.palette().color(QPalette.ColorRole.Button))
        animation.setEndValue(color)
        animation.valueChanged.connect(self.update_background_color)
        animation.start()

    @pyqtProperty(QVariant)
    def backgroundColor(self):
        return self.palette().color(QPalette.ColorRole.Button)

    @backgroundColor.setter
    def backgroundColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Button, color)
        self.setPalette(palette)

    def update_background_color(self, color):
        self.backgroundColor = color

def main():
    app = QApplication(sys.argv)
    button = AnimatedButton("Click me!")
    button.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()