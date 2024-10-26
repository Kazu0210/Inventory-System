from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QComboBox, QWidget

class PaginatedTable(QWidget):
    def __init__(self):
        super().__init__()
        
        self.data = [f"Item {i}" for i in range(1, 101)]  # Example data: 100 items
        self.items_per_page = 10
        self.current_page = 0
        
        # Create table
        self.table = QTableWidget(self)
        self.table.setRowCount(self.items_per_page)
        self.table.setColumnCount(1)
        
        # Pagination Controls
        self.prev_button = QPushButton('Previous', self)
        self.next_button = QPushButton('Next', self)
        self.items_per_page_dropdown = QComboBox(self)
        self.items_per_page_dropdown.addItems(['10', '25', '50'])
        self.items_per_page_dropdown.currentIndexChanged.connect(self.change_items_per_page)

        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.items_per_page_dropdown)
        layout.addWidget(self.prev_button)
        layout.addWidget(self.next_button)
        
        self.setLayout(layout)
        
        # Load initial data
        self.load_data()

    def load_data(self):
        self.table.clearContents()
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        page_data = self.data[start:end]

        self.table.setRowCount(len(page_data))
        for row, item in enumerate(page_data):
            self.table.setItem(row, 0, QTableWidgetItem(item))
        
        # Update buttons' states
        self.update_button_states()

    def update_button_states(self):
        total_pages = len(self.data) // self.items_per_page
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages)

    def next_page(self):
        self.current_page += 1
        self.load_data()

    def prev_page(self):
        self.current_page -= 1
        self.load_data()

    def change_items_per_page(self):
        self.items_per_page = int(self.items_per_page_dropdown.currentText())
        self.current_page = 0  # Reset to first page
        self.load_data()

if __name__ == "__main__":
    app = QApplication([])
    window = PaginatedTable()
    window.show()
    app.exec()
