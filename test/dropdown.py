from PyQt6.QtWidgets import QApplication, QComboBox, QWidget, QVBoxLayout

class ComboBoxExample(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QComboBox
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Option 1", "Option 2", "Option 3"])

        # Apply a flat style to the QComboBox and drop-down arrow
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;  /* Flat white background */
                border: 1px solid #888;     /* Simple border */
                padding: 5px;
            }
            QComboBox::drop-down {
                border: none;              /* No border around drop-down */
                background: transparent;   /* No background for drop-down button */
                width: 20px;               /* Width of drop-down button */
            }
            QComboBox::down-arrow {
                
            }
        """)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        self.setLayout(layout)

        self.setWindowTitle("Flat QComboBox Example")
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = ComboBoxExample()
    app.exec()
