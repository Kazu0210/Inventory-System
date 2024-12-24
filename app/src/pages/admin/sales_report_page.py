from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QListWidgetItem, QAbstractItemView, QCheckBox, QFrame, QLabel
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush, QColor

from ui.NEW.sales_report_page import Ui_Form as sales_report_UiForm
from ui.NEW.best_selling_product_template import Ui_Form as best_selling_UiForm

from utils.Inventory_Monitor import InventoryMonitor

from datetime import datetime, timedelta

import pymongo, re, json, random, os

class BestSellingListItem(QWidget, best_selling_UiForm):
    def __init__(self, list_of_data):
        super().__init__()
        self.setupUi(self)

        self.data = list_of_data

        self.setLabels()

    def setLabels(self):
        self.productID_label.setText(self.data.get('_id', 'N/A'))
        self.totalQuantitySold_label.setText(str(self.data.get('total_quantity_sold', 'N/A')))
        self.revenue_label.setText(str(self.data.get('total_sales_value', 'N/A')))

class SalesReportPage(QWidget, sales_report_UiForm):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)

        self.load_inventory_monitor()

        self.filter_query = {}

        # Make the scroll on the list widget smoother
        self.bestSelling_listWidget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Set layout for the product name filter
        self.productNameLayout = QVBoxLayout()

        # Make sure the frame exists and is defined in the UI file
        if hasattr(self, 'productName_frame'):
            self.productName_frame.setLayout(self.productNameLayout)
        else:
            print("Error: 'productName_frame' does not exist in the UI.")

        # Call function that sets the text label of today's sales and this month's revenue once
        self.update_labels()

    def load_product_category_filter(self):
        """Load product categories (cylinder sizes) from the database and populate the product category frame"""
        pipeline = [
            {"$group": {
                "_id": "$cylinder_size",
                "cylinder_size": {"$first": "$cylinder_size"}
            }}
        ]
        cylinder_sizes = list(self.connect_to_db('sales').aggregate(pipeline))
        available_cylinder_sizes = [size.get("cylinder_size") for size in cylinder_sizes]
        return available_cylinder_sizes 

    def load_product_name_filter(self):
        # Clear the layout by deleting all child widgets
        while self.productNameLayout.count():
            child = self.productNameLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Aggregate product data from the database
        pipeline = [
            {"$group": {
                "_id": "$product_name"
            }}
        ]
        product_data = list(self.connect_to_db('sales').aggregate(pipeline))

        # Add new checkboxes for each product name to the layout
        for product in product_data:
            product_name = product.get("_id")
            if product_name:
                product_filter_checkBox = QCheckBox(f"{product_name}")
                # Capture the current checkbox using a default argument in the lambda
                product_filter_checkBox.stateChanged.connect(lambda state, cb=product_filter_checkBox: self.handle_product_name_checkBox(cb))
                self.productNameLayout.addWidget(product_filter_checkBox)

    def handle_product_name_checkBox(self, checkbox):
        """Handle checkbox toggle signal to update the filter query."""
        checked_prod_name = []
        for i in range(self.productNameLayout.count()):
            item = self.productNameLayout.itemAt(i)
            widget = item.widget()

            # Ensure the widget is a QCheckBox and is checked
            if isinstance(widget, QCheckBox) and widget.isChecked():
                print(f"Checkbox '{widget.text()}' is checked.")
                checked_prod_name.append(widget.text())

        # Update the filter query with the checked product names
        if checked_prod_name:
            self.filter_query['product_name'] = checked_prod_name
        elif 'product_name' in self.filter_query:
            # Remove the 'product_name' key if no checkboxes are checked
            del self.filter_query['product_name']

        # Store the checked names in the instance attribute
        self.checked_prod_name = checked_prod_name

        print(f"Checked product names: {self.checked_prod_name}")
        self.update_sales_table()

    def update_top_product(self):
        data = self.get_best_selling_prod()

        if data:
            top_product_id = data[0]['_id']
            self.best_selling_label.setText(f"{top_product_id}")

    def update_best_selling_chart(self):
        # clear list widget first
        self.bestSelling_listWidget.clear()
        # get data from database
        data = self.get_best_selling_prod()
        
        for i in data:
            item = QListWidgetItem(self.bestSelling_listWidget)
            bestSellerItem = BestSellingListItem(i)
            print(f'ewan data: {i}')

            # Set size hint to ensure QListWidgetItem matches custom widget size
            item.setSizeHint(bestSellerItem.sizeHint())

            self.bestSelling_listWidget.setItemWidget(item, bestSellerItem)

    def get_best_selling_prod(self):
        # Aggregation pipeline to calculate total sales per product
        pipeline = [
            {"$group": {
                "_id": "$product_id",  # Group by product_id
                "total_quantity_sold": {"$sum": "$quantity"},  # Sum of quantity for each product_id
                "total_sales_value": {"$sum": "$total_amount"}, # Sum of total_amount for each product_id
            }},
            {"$sort": {"total_quantity_sold": -1}},  # Sort by total_quantity_sold in descending order
            {"$limit": 10}  # Limit to top 10 products
        ]
        top_products = list(self.connect_to_db('sales').aggregate(pipeline))

        # Print results
        for product in top_products:
            print(f"Product ID: {product['_id']}, Total Sold: {product['total_quantity_sold']}")

        return top_products

    def load_inventory_monitor(self):
        print(f'LOADING INVENTORY MONITOR')

        # monitor for today sales
        self.sales_monitor = InventoryMonitor("sales")
        self.sales_monitor.start_listener_in_background()
        self.sales_monitor.data_changed_signal.connect(lambda: self.update_labels())

    def update_labels(self):
        self.update_today_sales()
        self.update_revenue_this_month()
        self.update_sales_table()
        self.update_sales_trend_chart()
        self.update_best_selling_chart()
        self.update_top_product()

        self.load_product_name_filter()
        
    def get_last_7_days_sales(self):
        pipeline = [
            {
                "$match": {
                    "date": {
                        "$gte": datetime.now() - timedelta(days=7)
                    }
                }
            },
            {
                "$group": {
                    "_id": "$date",
                    "sales": {"$sum": "$total_amount"}
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]
        result = list(self.connect_to_db("sales").aggregate(pipeline))
        return result

    def get_sales_data(self):
        """
        Fetches or simulates sales data for the last 7 days.
        Returns a list of tuples (date, sales_amount).
        """
        # Fetch sales data for the last 7 days
        last7daysresult = self.get_last_7_days_sales()

        # Initialize a dictionary to store sales summed by date
        sales_by_date = {}
        for data in last7daysresult:
            datetime_obj = data['_id']  # Assuming '_id' contains the date
            date = datetime_obj.strftime('%Y-%m-%d')
            sales = data['sales']  # Sales for the given date
            sales_by_date[date] = sales_by_date.get(date, 0) + sales

        # Prepare sales data for the last 7 days
        sales_data = []
        today = datetime.now()
        for i in range(7):
            current_date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            # Fetch sales or use 0 if no sales data exists
            sales = sales_by_date.get(current_date, 0)
            sales_data.append((current_date, sales))

        return sales_data[::-1]  # Reverse to have the oldest date first

    def create_sale_trend_chart(self, sales_data):
        chart = QChart()
        chart.setTitle("Sales in the Last 7 Days")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # create a bar series
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
        axisY.setRange(0, sum(sales for _, sales in sales_data) + 50)

        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)  # Align the y-axis to the left
        bar_series.attachAxis(axisY)

        # Create the chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Check if the layout already exists
        if not self.sales_trend_frame.layout():
            layout = QVBoxLayout()
            layout.addWidget(chart_view)
            self.sales_trend_frame.setLayout(layout)
        else:
            # If layout exists, update the chart without creating a new layout
            self.sales_trend_frame.layout().itemAt(0).widget().setChart(chart)

    def update_sales_trend_chart(self):
        print(f'Updating sales trend chart')

        # Get sales data
        sales_data = self.get_sales_data()
        print(f'sales data: {sales_data}')
        self.create_sale_trend_chart(sales_data)

        print('Sales trend chart updated.')

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
            return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))

    def update_sales_table(self, page=0, rows_per_page=10):
            """Load prices current price on the prices table with pagination."""
            self.current_page = page  # Keep track of the current page
            self.rows_per_page = rows_per_page  # Number of rows per page

            table = self.sales_tableWidget
            table.setSortingEnabled(True)
            vertical_header = table.verticalHeader()
            vertical_header.hide()
            table.setRowCount(0)  # Clear the table

            table.setStyleSheet("""
            QTableWidget{
            border-radius: 5px;
            background-color: #fff;
            color: #000;
            }
            QHeaderView:Section{
            background-color: #228B22;
            color: #fff;               
            font: bold 12pt "Noto Sans";
            }
            QTableWidget::item {
                border: none;  /* Remove border from each item */
                padding: 5px;  /* Optional: Adjust padding to make the items look nicer */
            }
                QScrollBar:vertical {
                    border: none;
                    background: #0C959B;
                    width: 13px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical {
                    background: #002E2C;
                    border-radius: 7px;
                    min-height: 30px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: #0C959B;
                }
                QScrollBar:horizontal {
                    border: none;
                    background: #f0f0f0;
                    height: 14px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:horizontal {
                    background: #555;
                    border-radius: 7px;
                    min-width: 30px;
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                    background: none;
                }
                QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                    background: #f0f0f0;
                }
            """)

            # Header JSON directory
            header_dir = "app/resources/config/table/sales_tableHeader.json"

            # Settings directory
            settings_dir = "app/resources/config/settings.json"

            with open(header_dir, 'r') as f:
                header_labels = json.load(f)

            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            header = self.sales_tableWidget.horizontalHeader()
            header.setSectionsMovable(True)
            header.setDragEnabled(True)

            for column in range(table.columnCount()):
                table.setColumnWidth(column, 145)

            # Set uniform row height for all rows
            table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

            header.setFixedHeight(50)

            table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

            # Clean the header labels
            self.header_labels = [self.clean_header(header) for header in header_labels]
            
            # query filter
            # filter = {}

            # if self.searchBar_lineEdit != "":
            #     filter = {"$or": [
            #         {"product_name": {"$regex": self.searchBar_lineEdit.text(), "$options": "i"}},  # Case-insensitive match
            #         {"product_id": {"$regex": self.searchBar_lineEdit.text(), "$options": "i"}}
            #     ]}

            # Get data from MongoDB
            data = list(self.connect_to_db('sales').find({}).sort("_id", -1))
            if not data:
                return  # Exit if the collection is empty

            with open(settings_dir, 'r') as f:
                settings = json.load(f)
                self.current_time_format = settings['time_date'][0]['time_format']

            # Pagination logic
            start_row = page * rows_per_page
            end_row = start_row + rows_per_page
            paginated_data = data[start_row:end_row]

            # Populate table with paginated data
            for row, item in enumerate(paginated_data):
                table.setRowCount(row + 1)  # Add a new row for each item
                for column, header in enumerate(self.header_labels):
                    original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                    original_key = original_keys[0] if original_keys else None
                    value = item.get(original_key)
                    if value is not None:

                        if header == 'totalamount':
                            try:
                                if value:
                                    formatted_value = f"₱ {value:,.2f}"
                                    value = formatted_value

                            except Exception as e:
                                print(f"Error: {e}")

                        elif header == 'date':
                            try:
                                if value:
                                    print(f'VALUEEEEEE: {value}')
                                    
                                    # Directly format the datetime object
                                    value = value.strftime("%Y-%m-%d")
                                    print(f"DATE ONLYYYY: {value}")  # Output: 2024-12-24

                            except Exception as e:
                                print(f'Error: {e}')

                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                        # Check if row index is even
                        if row % 2 == 0:
                            table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                        table.setItem(row, column, table_item)

    def update_revenue_this_month(self):
        revenue = self.get_revenue_this_month()
        formatted = f"₱ {revenue:,.2f}"
        self.revenue_month_label.setText(formatted)

    def get_revenue_this_month(self):
        # Get the first day of the current month
        today = datetime.now()
        first_day_of_month = datetime(today.year, today.month, 1)

        # Get the first day of the next month (to use as an upper bound)
        if today.month == 12:
            first_day_of_next_month = datetime(today.year + 1, 1, 1)
        else:
            first_day_of_next_month = datetime(today.year, today.month + 1, 1)

        # MongoDB aggregation pipeline to calculate the revenue for the current month
        pipeline = [
            {
                "$match": {
                    "date": {
                        "$gte": first_day_of_month,  # Match documents from the start of the current month
                        "$lt": first_day_of_next_month  # Exclude documents from the next month
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {"$sum": "$total_amount"}  # Sum the total_amount field
                }
            }
        ]

        # Execute the aggregation pipeline
        result = list(self.connect_to_db('sales').aggregate(pipeline))

        # If there is a result, return the total revenue, else return 0
        if result:
            return result[0]["total_revenue"]
        else:
            return 0

    def update_today_sales(self):
        """Update the total sales today label"""
        sales = self.get_total_sales_today()
        formatted = f"₱ {sales:,.2f}"
        self.total_sales_label.setText(formatted)

    def get_total_sales_today(self):
        # Define the start of the day (midnight) for today
        today_start = datetime.combine(datetime.now().date(), datetime.min.time())
        pipeline = [
            {
                "$match": {
                    "date": {"$gte": today_start}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": "$total_amount"}
                }
            }
        ]
        result = list(self.connect_to_db("sales").aggregate(pipeline))  # Convert result to a list for easier handling
        # print(f'results: {result}')

        # print(f'today start date: {today_start}')

        if result:  # If result is not empty
            total_sales = result[0].get("total_sales", 0)
            return total_sales
        else:
            return 0  # Default to 0 if no sales found

    def connect_to_db(self, collectionN):
        connection_string = "mongodb://localhost:27017/"
        try:
            client = pymongo.MongoClient(connection_string)
            db_name = "LPGTrading_DB"
            return client[db_name][collectionN]
        except pymongo.errors.ConnectionError as e:
            print(f"Database connection failed: {e}")
            return None
