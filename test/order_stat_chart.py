from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Order Status Distribution")
        self.setGeometry(100, 100, 800, 600)

        self.create_pie_chart()

    def create_pie_chart(self):
        series = QPieSeries()
        shyet = 10
        series.append(f"Pending {shyet}%", 35)
        series.append("Completed", 80)
        series.append("Canceled", 5)
        series.append("Hatdog", 10)

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