import sys
from PyQt6.QtWidgets import QApplication, QTableView, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QTableView
        self.tableView = QTableView()
        self.tableViewModel = self.createTableModel()
        self.tableView.setModel(self.tableViewModel)
        self.tableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)  # Add this line
        layout.addWidget(self.tableView)

        # Create a QTableWidget
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Add this line
        for row in range(5):
            for column in range(3):
                item = QTableWidgetItem(f'Item {row},{column}')
                self.tableWidget.setItem(row, column, item)
        layout.addWidget(self.tableWidget)

        self.show()

    def createTableModel(self):
        model = QStandardItemModel(5, 3)
        model.setHorizontalHeaderLabels(['Column 1', 'Column 2', 'Column 3'])
        for row in range(5):
            for column in range(3):
                item = QStandardItem(f'Item {row},{column}')
                model.setItem(row, column, item)
        return model

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())