from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom QTabWidget Example")

        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #333;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #eee;
                border: 1px solid #aaa;
                padding: 5px;
                margin: 1px;
            }
            QTabBar::tab:selected {
                background: #d4d4d4;
                font-weight: bold;
                color: #333;
            }
            QTabBar::tab:hover {
                background: #ccc;
            }
        """)

        # Adding tabs
        tab_widget.addTab(QWidget(), "Tab 1")
        tab_widget.addTab(QWidget(), "Tab 2")

        layout = QVBoxLayout(self)
        layout.addWidget(tab_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
