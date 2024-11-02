from PyQt6.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a calendar widget
        self.calendar = QCalendarWidget(self)
        self.calendar.clicked.connect(self.show_selected_date)  # Connect the clicked signal to get the selected date

        # Create a label to display the selected date
        self.date_label = QLabel("Selected Date:", self)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.date_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_selected_date(self):
        # Get the selected date from the calendar
        selected_date = self.calendar.selectedDate()
        
        # Convert the QDate to a string format (e.g., "yyyy-MM-dd")
        date_str = selected_date.toString("yyyy-MM-dd")
        
        # Display the date on the label
        self.date_label.setText(f"Selected Date: {date_str}")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
