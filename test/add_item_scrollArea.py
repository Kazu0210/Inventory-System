from PyQt6.QtWidgets import (
    QApplication, QWidget, QScrollArea, QVBoxLayout, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
import sys


class ResizableScrollAreaWithFrames(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resizable Scroll Area with Frames Example")
        self.setGeometry(100, 100, 800, 600)

        # Main Splitter (Vertical)
        vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        vertical_splitter.setHandleWidth(5)

        # Horizontal Splitter for Resizing Horizontally
        horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)
        horizontal_splitter.setHandleWidth(5)

        # QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.StyledPanel)

        # Content inside QScrollArea
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Add QFrames to the layout
        for i in range(10):
            frame = self.create_frame(f"Item {i + 1}")
            scroll_layout.addWidget(frame)

        self.scroll_area.setWidget(scroll_content)

        # Add scroll area to horizontal splitter
        horizontal_splitter.addWidget(self.scroll_area)

        # Add another widget to horizontal splitter
        right_widget = QFrame()
        right_widget.setFrameShape(QFrame.Shape.StyledPanel)
        right_widget.setStyleSheet("background-color: lightblue;")
        horizontal_splitter.addWidget(right_widget)

        # Add horizontal splitter to vertical splitter
        vertical_splitter.addWidget(horizontal_splitter)

        # Add another widget below (optional)
        bottom_widget = QFrame()
        bottom_widget.setFrameShape(QFrame.Shape.StyledPanel)
        bottom_widget.setStyleSheet("background-color: lightgray;")
        vertical_splitter.addWidget(bottom_widget)

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(vertical_splitter)

    def create_frame(self, text):
        """Creates a styled QFrame with text."""
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setStyleSheet("background-color: lightgray; border: 1px solid black;")
        frame.setFixedHeight(50)

        # Add layout and content inside the frame
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)

        # You can add any widgets inside the frame here
        # label = QLabel(text)
        # layout.addWidget(label)

        return frame


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResizableScrollAreaWithFrames()
    window.show()
    sys.exit(app.exec())
