import sys
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class CustomTable(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Custom Table')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)

        self.tableWidget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])

        for row in range(5):
            for column in range(3):
                item = QTableWidgetItem(f'Row {row+1}, Column {column+1}')
                self.tableWidget.setItem(row, column, item)

        self.layout.addWidget(self.tableWidget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CustomTable()
    ex.show()
    sys.exit(app.exec())