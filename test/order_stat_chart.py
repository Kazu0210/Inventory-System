from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Order Status Distribution")
        self.setGeometry(100, 100, 800, 600)

        self.create_pie_chart()

    def create_pie_chart(self):
        series = QPieSeries()
        series.append("Pending", 35)
        series.append("Completed", 80)
        series.append("Canceled", 5)

        # Customize slice colors
        pending_slice = series.slices()[0]
        completed_slice = series.slices()[1]
        canceled_slice = series.slices()[2]

        pending_slice.setBrush(QColor("#4E4E4E"))
        completed_slice.setBrush(QColor("green"))
        canceled_slice.setBrush(QColor("red"))

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Order Status Distribution")

        chart_view = QChartView(chart)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
