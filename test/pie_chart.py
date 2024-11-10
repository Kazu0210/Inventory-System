from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import sys
import random

class DonutChartWidget(FigureCanvas):
    def __init__(self, data, labels, colors):
        self.data = data
        self.labels = labels
        self.colors = colors
        self.fig, self.ax = plt.subplots()
        
        super().__init__(self.fig)
        self.plot_donut_chart()

    def plot_donut_chart(self):
        """Plot the donut chart using the current data."""
        self.ax.clear()  # Clear previous plot
        wedges, _ = self.ax.pie(self.data, labels=self.labels, colors=self.colors, wedgeprops=dict(width=0.3, edgecolor='w'))
        
        # Add some styling for better appearance
        for wedge in wedges:
            wedge.set_linewidth(1.5)  # Line thickness between slices
            wedge.set_edgecolor('white')  # Color for the gap between slices

        self.ax.set_aspect("equal")  # Ensure the pie chart is circular
        self.draw()  # Render the updated chart

    def update_data(self, new_data, new_labels):
        """Update the data and re-plot the donut chart."""
        self.data = new_data
        self.labels = new_labels
        self.plot_donut_chart()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initial data for the chart
        self.data = [30, 20, 50]
        self.labels = ["Category A", "Category B", "Category C"]
        self.colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]

        # Set up the main window
        self.setWindowTitle("Dynamic Donut Chart with Matplotlib in PyQt6")
        self.setGeometry(100, 100, 500, 500)

        # Create the donut chart widget
        self.donut_chart = DonutChartWidget(self.data, self.labels, self.colors)

        # Layout for chart and controls
        layout = QVBoxLayout()
        layout.addWidget(self.donut_chart)

        # Add button to update data
        self.update_button = QPushButton("Update Chart")
        self.update_button.clicked.connect(self.add_random_data)
        layout.addWidget(self.update_button)

        # Central widget setup
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_random_data(self):
        """Adds a new random data slice and updates the chart."""
        new_value = random.randint(10, 50)  # Random value for demonstration
        self.data.append(new_value)
        self.labels.append(f"Category {chr(65 + len(self.labels))}")  # Label like Category D, E, etc.

        # Update the chart data
        self.donut_chart.update_data(self.data, self.labels)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
