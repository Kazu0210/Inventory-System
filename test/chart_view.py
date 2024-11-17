from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget


class PieChartExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Pie Chart Example")
        self.resize(800, 600)

        # Set up the layout and chart
        self.layout = QVBoxLayout()
        self.chart_view = self.create_pie_chart()
        self.layout.addWidget(self.chart_view)
        self.setLayout(self.layout)

    def create_pie_chart(self):
        # Create a QChart instance
        chart = QChart()
        chart.setTitle("Pie Chart Example")
        
        # Create a QPieSeries instance
        series = QPieSeries()
        series.append("Category A", 40)
        series.append("Category B", 30)
        series.append("Category C", 20)
        series.append("Category D", 10)

        # Customize individual slices (optional)
        slice_a = series.slices()[0]
        slice_a.setExploded(True)  # Highlight this slice
        slice_a.setLabelVisible(True)
        slice_a.setBrush(QColor("cyan"))

        # Add the series to the chart
        chart.addSeries(series)

        # Create a QChartView for displaying the chart
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        return chart_view


if __name__ == "__main__":
    app = QApplication([])
    window = PieChartExample()
    window.show()
    app.exec()
