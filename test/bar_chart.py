import random
from datetime import datetime, timedelta
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter


class DailySalesChart(QMainWindow):
    def __init__(self, sales_data):
        super().__init__()
        self.setWindowTitle("Daily Sales (Last 7 Days)")
        self.resize(800, 600)

        # Create a frame to hold the chart
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        
        # Create the chart
        chart = QChart()
        chart.setTitle("Sales in the Last 7 Days")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # Create a bar series
        bar_series = QBarSeries()

        # Add the sales data to the series
        bar_set = QBarSet("Sales")
        for _, sales in sales_data:
            bar_set.append(sales)

        bar_series.append(bar_set)
        chart.addSeries(bar_series)

        # Create a category axis for the dates (X-axis)
        axisX = QBarCategoryAxis()  # Use QBarCategoryAxis instead of QCategoryAxis
        dates = [date for date, _ in sales_data]  # Extract the dates
        axisX.append(dates)  # Set the custom labels

        axisX.setTitleText("Date")
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)  # Align the x-axis at the bottom
        bar_series.attachAxis(axisX)

        # Configure the value axis (Y-axis)
        axisY = QValueAxis()
        axisY.setTitleText("Sales Amount")
        axisY.setRange(0, max(sales for _, sales in sales_data) + 50)  # Add a buffer above max sales
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)  # Align the y-axis to the left
        bar_series.attachAxis(axisY)

        # Create the chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create a layout for the frame and add the chart view to it
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        frame.setLayout(layout)

        # Set the frame as the central widget of the window
        self.setCentralWidget(frame)


def simulate_sales_data():
    """
    Simulates sales data for the last 7 days.
    Returns a list of tuples (date, sales_amount).
    """
    sales_data = []
    today = datetime.now()
    for i in range(7):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")  # Format date as YYYY-MM-DD
        sales = random.randint(100, 500)  # Random sales amount between 100 and 500
        sales_data.append((date, sales))

    return sales_data[::-1]  # Reverse to have the oldest date first


if __name__ == "__main__":
    app = QApplication([])

    # Simulate sales data and create the chart
    sales_data = simulate_sales_data()
    window = DailySalesChart(sales_data)

    window.show()
    app.exec()
