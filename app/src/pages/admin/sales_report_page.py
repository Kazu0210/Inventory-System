from PyQt6.QtWidgets import QWidget, QTableWidgetItem
from ui.NEW.sales_report_page import Ui_Form
from utils.Inventory_Monitor import InventoryMonitor

from datetime import datetime, timedelta

import pymongo, re, json

class SalesReportPage(QWidget, Ui_Form):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)

        self.sales_monitor = InventoryMonitor("sales")
        self.sales_monitor.start_listener_in_background()
        self.sales_monitor.data_changed_signal.connect(lambda: self.update_labels())

        # call function that set text label of today sales and this month revenue once
        self.update_labels()

    def update_labels(self):
        self.update_today_sales()
        self.update_revenue_this_month()
        self.update_sales_table()

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
            return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))

    def update_sales_table(self):
        table = self.sales_tableWidget
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table

        # header json directory
        header_dir = "app/resources/config/table/sales_tableHeader.json"

        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        # set width of all the columns
        for column in range(table.columnCount()):
            table.setColumnWidth(column, 200)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

        data = list(self.connect_to_db('sales').find())
        if not data:
            return  # Exit if the collection is empty

        # Populate table with data
        for row, item in enumerate(data):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)
                if value is not None:
                    if header == 'priceperunit' or header == 'totalvalue':
                        if value:
                            formatted_price = f"{int(value):,.2f}"
                            value = formatted_price
                    table.setItem(row, column, QTableWidgetItem(str(value)))


    def update_revenue_this_month(self):
        self.revenue_month_label.setText(str(self.get_revenue_this_month()))

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
        self.total_sales_label.setText(str(self.get_total_sales_today()))

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
        print(f'results: {result}')

        print(f'today start date: {today_start}')

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
