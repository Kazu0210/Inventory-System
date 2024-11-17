from PyQt6.QtWidgets import *
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from PyQt6.QtGui import QColor, QLinearGradient, QBrush
from ui.dashboard_page import Ui_Form as Ui_dashboard_page

from utils.DB_checker import db_checker
from utils.Inventory_Monitor import InventoryMonitor

from PyQt6.QtCore import QThread, pyqtSignal, QSize
from datetime import datetime, timedelta
import pymongo, random

class Dashboard(QWidget, Ui_dashboard_page):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window

        # Database connection
        self.collection_name = self.connect_to_db("products_items")

        # Create and start the update thread for total stock
        self.update_thread = UpdateThread(self.collection_name)
        self.update_thread.updated.connect(self.update_total_stock_label)
        self.update_thread.start()
        
        # Set up the layout for the QScrollArea
        cylinderContainerWidget = self.scrollAreaWidgetContents
        self.cylinderContainerLayout = QVBoxLayout(cylinderContainerWidget)
        self.cylinderTypes_scrollArea.setWidget(cylinderContainerWidget)

        self.labels = []

        # Initialize the products monitor to listen for changes
        self.products_monitor = InventoryMonitor('products_items')
        self.products_monitor.start_listener_in_background()
        self.products_monitor.data_changed_signal.connect(self.update_stock_widgets)

        # Initialize orders monitor
        self.order_monitor = InventoryMonitor('orders')
        self.order_monitor.start_listener_in_background()
        self.order_monitor.data_changed_signal.connect(self.display_total_orders)

        # Initialize monitor to update stock level chart
        self.stock_level_monitor = InventoryMonitor('products')

        # Call the function to update the cylinder list
        self.update_cylinder_list()
        # Call funcion that display order summary once
        self.display_total_orders()

        self.show_completed_order()
        self.show_pending_order()
        self.show_cancelled_order()

        self.completed_order_listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.pending_order_listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.cancelled_order_listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # call funcion that load the stock level chart once
        self.load_stock_level_chart()

    def update_stock_widgets(self):
        self.update_cylinder_list()
        self.load_stock_level_chart()

    def create_pie_chart(self, processed_data):
        series = QPieSeries()

        for data in processed_data:
            cylinder_size = data['cylinder_size']
            total_quantity = data['total_quantity']
            series.append(f'{cylinder_size}kg', total_quantity)
            print(f'Series Slices: {series.slices()}')

            # Check if there are slices in the series
            if series.slices():
                # Iterate through slices and update them based on the data
                for idx, slice in enumerate(series.slices()):
                    # Match the slice to the current data by its index
                    if idx == len(series.slices()) - 1:  # last slice
                        print(f'Last Slice: {slice}')

                        # Hide the label on top
                        slice.setLabelVisible(False)

                        # Apply conditions to the last slice
                        if total_quantity <= 5:
                            slice.setLabel(f"Low stock: {total_quantity} units left")
                            slice.setLabelVisible(True)
                            # slice.setBrush(QColor("red"))  # Mark low stock with red color
                            if int(cylinder_size) == 5:
                                slice.setBrush(QColor("#2ecc71"))  # Green
                            elif int(cylinder_size) == 10:
                                slice.setBrush(QColor("#f39c12"))  # Yellow
                            elif int(cylinder_size) == 11:
                                slice.setBrush(QColor("#9b59b6"))  # Purple
                            elif int(cylinder_size) == 15:
                                slice.setBrush(QColor("#1abc9c"))  # Teal
                            elif int(cylinder_size) == 22:
                                slice.setBrush(QColor("#f1c40f"))  # Gold
                            elif int(cylinder_size) == 50:
                                slice.setBrush(QColor("#34495e"))  # Dark gray
                        else:
                            # Update brush color for non-low-stock slices
                            if int(cylinder_size) == 5:
                                slice.setBrush(QColor("#2ecc71"))  # Green
                            elif int(cylinder_size) == 10:
                                slice.setBrush(QColor("#f39c12"))  # Yellow
                            elif int(cylinder_size) == 11:
                                slice.setBrush(QColor("#9b59b6"))  # Purple
                            elif int(cylinder_size) == 15:
                                slice.setBrush(QColor("#1abc9c"))  # Teal
                            elif int(cylinder_size) == 22:
                                slice.setBrush(QColor("#f1c40f"))  # Gold
                            elif int(cylinder_size) == 50:
                                slice.setBrush(QColor("#34495e"))  # Dark gray


        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Stock Levels")

        chart_view = QChartView(chart)

        # frame to hold the chart
        self.chart_frame = self.stockChart_frame
        # self.chart_frame.setStyleSheet("border: 2px solid black;")
                # Clear existing layout if present
        if self.chart_frame.layout():
            # Remove the old layout before setting a new one
            QWidget().setLayout(self.chart_frame.layout())  # Removes the layout

        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        self.chart_frame.setLayout(layout)

    def load_stock_level_chart(self):
        print(f'showing stock level chart')
        # get data from database

        processed_data = self.get_quantity_in_stock()
        print(processed_data)
        # for data in processed_data:
        #     cylinder_size = data['cylinder_size']
        #     total_quantity = data['total_quantity']

        self.create_pie_chart(processed_data)

    def show_cancelled_order(self):
        orders = self.get_cancelled_orders()
        for order in orders:
            orderID = order.get('order_id', '')
            customer_name = order.get('customer_name')
            order_date = order.get('order_date')
            order_status = order.get('order_status')

            order_id_label = QLabel(
                f"Order ID: {orderID}\n"
                f"Customer Name: {customer_name}\n"
                f"Order Date: {order_date}\n"
                f"Order Status: {order_status}"
            )

            item = QListWidgetItem(self.cancelled_order_listWidget)
            item.setSizeHint(QSize(200, 100))
            self.cancelled_order_listWidget.setItemWidget(item, order_id_label)

    def show_pending_order(self):
        orders = self.get_pending_orders()
        for order in orders:
            orderID = order.get('order_id', '')
            customer_name = order.get('customer_name')
            order_date = order.get('order_date')
            order_status = order.get('order_status')

            order_id_label = QLabel(
                f"Order ID: {orderID}\n"
                f"Customer Name: {customer_name}\n"
                f"Order Date: {order_date}\n"
                f"Order Status: {order_status}"
            )

            item = QListWidgetItem(self.pending_order_listWidget)
            item.setSizeHint(QSize(200, 100))
            self.pending_order_listWidget.setItemWidget(item, order_id_label)

    def show_completed_order(self):
        orders = self.get_completed_orders()
        for order in orders:
            orderID = order.get('order_id', '')
            customer_name = order.get('customer_name')
            order_date = order.get('order_date')
            order_status = order.get('order_status')

            order_id_label = QLabel(
                f"Order ID: {orderID}\n"
                f"Customer Name: {customer_name}\n"
                f"Order Date: {order_date}\n"
                f"Order Status: {order_status}"
            )

            item = QListWidgetItem(self.completed_order_listWidget)
            item.setSizeHint(QSize(200, 100))
            self.completed_order_listWidget.setItemWidget(item, order_id_label)
    def get_cancelled_orders(self):
        try:
            orders_collection = self.connect_to_db('orders')
            completed_orders = orders_collection.find({"order_status": "Cancelled"})
            return completed_orders
        except Exception as e:
            print(f"Error getting completed orders: {e}")
            return []
    def get_pending_orders(self):
        try:
            orders_collection = self.connect_to_db('orders')
            completed_orders = orders_collection.find({"order_status": "Pending"})
            return completed_orders
        except Exception as e:
            print(f"Error getting completed orders: {e}")
            return []

    def get_completed_orders(self):
        try:
            orders_collection = self.connect_to_db('orders')
            completed_orders = orders_collection.find({"order_status": "Completed"})
            return completed_orders
        except Exception as e:
            print(f"Error getting completed orders: {e}")
            return []

    def display_total_orders(self):
        daily_order_count = self.get_daily_order_count()
        weekly_order_count = self.get_weekly_order_count()
        monthly_order_count = self.get_monthly_order_count()

        self.daily_order_label.setText(daily_order_count)
        self.weekly_order_label.setText(weekly_order_count)
        self.monthly_order_label.setText(monthly_order_count)

    def get_monthly_order_count(self):
        # Get today's date
        today = datetime.today()

        # Calculate the start of the current month (1st day of the month)
        start_of_month = today.replace(day=1).date().strftime('%Y-%m-%d')

        # Get today's date in "YYYY-MM-DD" format
        today_str = today.date().strftime('%Y-%m-%d')

        # Connect to the orders collection
        orders_collection = self.connect_to_db('orders')

        # Query for orders from the start of the month to today
        order_count = orders_collection.count_documents({
            "order_date": {
                "$gte": start_of_month,
                "$lte": today_str
            }
        })

        # Print the monthly order count
        return str(order_count)
    
    def get_weekly_order_count(self):
        # Get today's date
        today = datetime.today()

        # Calculate the start of the current week (Monday)
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        start_of_week_str = start_of_week.date().strftime('%Y-%m-%d')

        # Calculate the end of the current week (Sunday)
        end_of_week = start_of_week + timedelta(days=7)  # Sunday
        end_of_week_str = end_of_week.date().strftime('%Y-%m-%d')

        # Connect to the orders collection
        orders_collection = self.connect_to_db('orders')

        # Query for orders between the start and end of the current week
        order_count = orders_collection.count_documents({
            "order_date": {
                "$gte": start_of_week_str,
                "$lte": end_of_week_str
            }
        })

        # Print the weekly order count
        return str(order_count)

    def get_daily_order_count(self):
        # Get today's date in "YYYY-MM-DD" format
        today = datetime.today().date().strftime('%Y-%m-%d')

        # Connect to the orders collection
        orders_collection = self.connect_to_db('orders')

        # Query orders where order_date matches today's date
        order_count = orders_collection.count_documents({"order_date": today})

        return str(order_count)
    
    def get_daily_order_count_shyet(self):
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$order_date",  # Group by date
                        "total_orders": {"$sum": 1}  # Count the orders
                    }
                }
            ]
            result = self.connect_to_db("orders").aggregate(pipeline)
            daily_orders = {}
            for item in result:
                date = item['_id']
                total_orders = item['total_orders']
                daily_orders[date] = total_orders
            return daily_orders
        except Exception as e:
            print(f"Error getting daily order count: {e}")
            return {}

    def update_cylinder_list(self):
        processed_data = self.get_quantity_in_stock()
        self.display_cylinder_data(processed_data)

    def display_cylinder_data(self, processed_data):
        # This method will update the scroll area with new data
        # Make sure to reuse existing labels or create new ones as needed
        
        # First, clear the existing labels in the scroll area (if needed)
        for label in self.labels:
            self.cylinderContainerLayout.removeWidget(label)
            label.deleteLater()  # Ensure the widgets are deleted properly
        self.labels.clear()  # Clear the list of stored labels

        # Now, create new labels based on the processed data
        for data in processed_data:
            cylinder_size = data['cylinder_size']
            total_quantity = data['total_quantity']

            label = QLabel(f'{cylinder_size}KG - {total_quantity} cylinder in stock')
            label.setMaximumHeight(50)  # Set max height if needed
            self.labels.append(label)  # Store reference to the label
            self.cylinderContainerLayout.addWidget(label)  # Add the label to the layout

    def get_quantity_in_stock(self):
        try:
            # Use aggregation to group by cylinder_size and sum quantity_in_stock
            pipeline = [
                {
                    "$group": {
                        "_id": "$cylinder_size",  # Group by cylinder_size
                        "total_quantity": {"$sum": "$quantity_in_stock"}  # Sum the quantities
                    }
                }
            ]
            # Run the aggregation pipeline on the "products_items" collection
            result = self.connect_to_db("products_items").aggregate(pipeline)

            processed_data = []
            # Process the results
            for item in result:
                cylinder_size = item['_id']
                processed_cylinder_size = cylinder_size.replace('kg', '')
                total_quantity = item['total_quantity']

                processed_data.append({
                    "cylinder_size": processed_cylinder_size,
                    "total_quantity": total_quantity
                })

            processed_data.sort(key=lambda x: int(x['cylinder_size']))

            return processed_data  # Return the result (list) if needed for further processing

        except Exception as e:
            print(f"Error getting quantity in stock: {e}")
            return []

    def update_total_stock_label(self, total_stock=None):
        # display the total on a label
        if total_stock is None:
            total_stock = self.get_total_stock()
        try:
            self.totalItemStock_label.setText(f'{total_stock}')
        except Exception as e:
            print(e)

    def get_total_stock(self):
        try:
            total_stock = self.connect_to_db("products_items").count_documents({})
            print(f'total stock: {total_stock}')
            return total_stock
        except Exception as e:
            print(f"Error getting total stock: {e}")
            return 0

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
class UpdateThread(QThread):
    updated = pyqtSignal(int)

    def __init__(self, collection):
        super().__init__()
        self.collection = collection
        self.running = True

    def run(self):
        while self.running:
            try:
                total_stock = self.collection.count_documents({})
                self.updated.emit(total_stock)
            except Exception as e:
                print(f"Error updating total stock: {e}")
            QThread.msleep(1000)  # Update every second

    def stop(self):
        self.running = False
