from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QWidget
)
import sys


class PaginationExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Example dataset
        self.data = [
            [f"Row {i + 1}", f"Value {i + 1}"] for i in range(50)
        ]
        self.rows_per_page = 10
        self.current_page = 0
        self.total_pages = len(self.data) // self.rows_per_page + (
            1 if len(self.data) % self.rows_per_page > 0 else 0
        )

        self.load_page()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Column 1", "Column 2"])
        self.layout.addWidget(self.table)

        # Pagination controls
        self.controls_layout = QVBoxLayout()
        self.previous_button = QPushButton("Previous")
        self.previous_button.clicked.connect(self.previous_page)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        self.page_label = QLabel()

        self.controls_layout.addWidget(self.previous_button)
        self.controls_layout.addWidget(self.next_button)
        self.controls_layout.addWidget(self.page_label)

        self.layout.addLayout(self.controls_layout)
        self.setLayout(self.layout)

    def load_page(self):
        # Clear current table content
        self.table.setRowCount(0)

        # Calculate start and end indices
        start_index = self.current_page * self.rows_per_page
        end_index = start_index + self.rows_per_page
        page_data = self.data[start_index:end_index]

        # Populate the table with data for the current page
        self.table.setRowCount(len(page_data))
        for row_idx, row_data in enumerate(page_data):
            for col_idx, cell_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

        # Update page label
        self.page_label.setText(f"Page {self.current_page + 1} of {self.total_pages}")

        # Enable/disable navigation buttons
        self.previous_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_page()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaginationExample()
    window.show()
    sys.exit(app.exec())
