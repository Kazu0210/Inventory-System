import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from window import Ui_Form

class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        # Initialize the UI
        self.setupUi(self)

        # get column count
        num_columns = self.tableWidget.columnCount()
        print(f'Number of columns: {num_columns}')

        # Set the row count and column count
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(num_columns)
        
        for col in range(self.tableWidget.columnCount()):
            self.tableWidget.setItem(0, col, QTableWidgetItem(f'Col: {col}'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())