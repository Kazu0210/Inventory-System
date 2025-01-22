from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QVBoxLayout, QAbstractItemView, QPushButton, QFileDialog, QHeaderView, QFrame
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QBrush, QColor, QIcon

from src.ui.sales_report_page import Ui_Form as sales_report_UiForm
from src.ui.NEW.best_selling_product_template import Ui_Frame as best_selling_UiForm
from src.utils.Inventory_Monitor import InventoryMonitor
from src.utils.Logs import Logs
from src.utils.dir import ConfigPaths
from src.custom_widgets.message_box import CustomMessageBox

from datetime import datetime, timedelta
from fpdf import FPDF
import pymongo, re, json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class BestSellingListItem(QFrame, best_selling_UiForm):
    def __init__(self, list_of_data):
        super().__init__()
        self.setupUi(self)

        self.setLabels(list_of_data)

    def setLabels(self, data):
        """Set insert data to the labels"""
        product_name: str = str(data.get('product_name', 'N/A'))
        product_id: str = str(data.get('product_id', 'N/A'))
        cylinder_size: str = str(data.get('cylinder_size', 'N/A'))
        revenue: int = f"₱ {data.get('total_value_sold', 'N/A'):,.2f}"
        price: int = f"₱ {data.get('price', 'N/A'):,.2f}"
        total_quantity_sold: int = str(data.get('total_quantity_sold', 'N/A'))

        try:
            self.product_name_label.setText(product_name)
            self.productID_label.setText(product_id)
            self.cylinderSize_label.setText(cylinder_size)
            self.revenue_label.setText(revenue)
            self.price_label.setText(price)
            self.totalQuantitySold_label.setText(total_quantity_sold)
        except Exception as e:
            print(f"Error: {e}")
            CustomMessageBox.show_message('warning', 'Error', 'An unexpected error occurred while updating the labels. Please try again if the issue persists.')

class BarChartFrame(QWidget):
    def __init__(self, categories, values, title="Bar Chart", xlabel="Categories", ylabel="Values", color='skyblue'):
        super().__init__()

        # Create the matplotlib figure and canvas
        self.figure = plt.Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Create the initial bar chart
        self.create_bar_chart(categories, values, title, xlabel, ylabel, color)

    def create_bar_chart(self, categories, values, title, xlabel, ylabel, color):
        # Create a subplot
        self.ax = self.figure.add_subplot(111)

        # Create a bar chart
        self.ax.bar(categories, values, color=color)

        # Set labels and title
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)

        # Refresh the canvas to display the plot
        self.canvas.draw()

    def reload_chart(self):
        print('clearing chart')
        self.figure.clf()  # Clear the entire figure
        self.ax = self.figure.add_subplot(111)  # Recreate the axes
        self.canvas.draw()  # Update the canvas to reflect the changes

class SalesReportPage(QWidget, sales_report_UiForm):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setupUi(self)
        self.logs = Logs() # initialize activity logs
        self.dirs = ConfigPaths() # initialize config paths

        self.filter_query = {}
        self.load_filters() # call function that loads all the filters
        self.update_labels()
        self.hide_back_button()
        self.set_icons()
        self.custom_time_period_frame.hide() # hide the frame the holds the inputs for custom time period filter
        self.load_button_connections()

        # self.load_inventory_monitor()
        self.sales_monitor = InventoryMonitor("sales")
        self.sales_monitor.start_listener_in_background()
        self.sales_monitor.data_changed_signal.connect(lambda: self.update_labels())
        self.load_default_key_metrics()

    def load_default_key_metrics(self):
        """load revenue and estimated profit for today etc. which is the default"""
        formatted_revenue = f"₱ {self.get_total_revenue_today():,.2f}"
        self.revenue_label.setText(str(formatted_revenue))

        formatted_profit = f"₱ {self.get_estimated_profit_today():,.2f}"
        self.estimated_profit_label.setText(str(formatted_profit))

    # def load_bar_chart(self):
    #     """Load sales trend chart"""
    #     # remove margin
    #     # Get sales data for the last 7 days
    #     sales_data = self.get_sales_data()
    #     print(f'Sales data: {sales_data}')
        
    #     # Extract the categories (dates) and values (sales amounts)
    #     categories = [data[0] for data in sales_data]  # Get dates (e.g., "2025-01-16")
    #     values = [data[1] for data in sales_data]  # Get sales amounts (e.g., 0, 3000, 9000)

    #     # Create the chart frame with the actual data
    #     self.chart_frame = BarChartFrame(categories, values, title="Sales In the Last 7 Days", xlabel="Date", ylabel="Sales")

    #     # Check if the layout already exists
    #     if not self.sales_trend_frame.layout():
    #         layout = QVBoxLayout()
    #         layout.addWidget(self.chart_frame)
    #         self.sales_trend_frame.setLayout(layout)
    #         self.sales_trend_frame.setContentsMargins(0,0,0,0)
    #     else:
    #         print('Chart already have a layout')
    #         self.chart_frame.reload_chart()

    def get_estimated_profit_today(self):
        """
        Calculate the estimated profit for today's sales.
        
        Returns:
            float: Total profit for today's sales.
        """
        try:
            
            # Get the current date in YYYY-MM-DD format
            today_date = datetime.now().strftime('%Y-%m-%d')
            
            # Query to fetch today's sales
            filter = {
                "sale_date": {
                    "$regex": f"^{today_date}"
                }
            }
            today_sales = list(self.connect_to_db('sales').find(filter))
            print(f'Result from getting today sales: {list(today_sales)}')
            
            # Calculate total profit
            total_profit = 0
            for sale in today_sales:
                for product in sale.get('products_sold', []):
                    # Calculate profit per product
                    selling_price = product.get('price', 0)
                    supplier_price = product.get('supplier_price', 0)
                    quantity_sold = product.get('quantity', 0)
                    
                    profit = (selling_price - supplier_price) * quantity_sold
                    total_profit += profit
                    
            print(f'Total profit: {total_profit}')
            return total_profit
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0

    def get_estimated_profit_this_week(self):
        """
        Calculate the estimated profit for this week's sales.

        Returns:
            float: Total profit for this week's sales.
        """
        try:
            # Get the current date and determine the start and end of the week
            today = datetime.now()
            start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
            end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week

            # Format dates in YYYY-MM-DD for filtering
            start_of_week_str = start_of_week.strftime('%Y-%m-%d')
            end_of_week_str = end_of_week.strftime('%Y-%m-%d')

            # Query to fetch this week's sales
            filter = {
                "sale_date": {
                    "$gte": start_of_week_str,
                    "$lte": end_of_week_str
                }
            }
            this_week_sales = list(self.connect_to_db('sales').find(filter))
            print(f'Result from getting this week sales: {list(this_week_sales)}')

            # Calculate total profit
            total_profit = 0
            for sale in this_week_sales:
                for product in sale.get('products_sold', []):
                    # Calculate profit per product
                    selling_price = product.get('price', 0)
                    supplier_price = product.get('supplier_price', 0)
                    quantity_sold = product.get('quantity', 0)

                    profit = (selling_price - supplier_price) * quantity_sold
                    total_profit += profit

            print(f'Total profit for this week: {total_profit}')
            return total_profit

        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0
        
    def get_estimated_profit_this_month(self):
        """
        Calculate the estimated profit for this month's sales.

        Returns:
            float: Total profit for this month's sales.
        """
        try:
            # Get the current date and determine the start and end of the month
            today = datetime.now()
            start_of_month = today.replace(day=1)  # First day of the month
            end_of_month = (today.replace(month=today.month % 12 + 1, day=1) - timedelta(days=1)) if today.month < 12 else today.replace(month=12, day=31)

            # Format dates in YYYY-MM-DD for filtering
            start_of_month_str = start_of_month.strftime('%Y-%m-%d')
            end_of_month_str = end_of_month.strftime('%Y-%m-%d')

            # Query to fetch this month's sales
            filter = {
                "sale_date": {
                    "$gte": start_of_month_str,
                    "$lte": end_of_month_str
                }
            }
            this_month_sales = list(self.connect_to_db('sales').find(filter))
            print(f'Result from getting this month sales: {list(this_month_sales)}')

            # Calculate total profit
            total_profit = 0
            for sale in this_month_sales:
                for product in sale.get('products_sold', []):
                    # Calculate profit per product
                    selling_price = product.get('price', 0)
                    supplier_price = product.get('supplier_price', 0)
                    quantity_sold = product.get('quantity', 0)

                    profit = (selling_price - supplier_price) * quantity_sold
                    total_profit += profit

            print(f'Total profit for this month: {total_profit}')
            return total_profit

        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0
    
    def get_estimated_profit_for_period(self, start_date, end_date):
        """
        Calculate the estimated profit for a given date range.
        """
        # Ensure start_date and end_date are datetime.date objects if they are strings
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").date()

        # Convert start_date and end_date to string format (YYYY-MM-DD) for MongoDB query
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Query sales in the specified date range
        sales = self.connect_to_db('sales').find({
            'sale_date': {'$gte': start_date_str, '$lte': end_date_str}
        })

        total_profit = 0

        # Loop through sales to calculate total profit
        for sale in sales:
            # Ensure sale_date is valid and in the correct format
            try:
                sale_date = datetime.strptime(sale["sale_date"], "%Y-%m-%d %H:%M:%S").date()  # Convert to date
            except (KeyError, ValueError):
                continue  # Skip sales with invalid or missing sale_date

            # Only calculate profit for sales within the date range
            if start_date <= sale_date <= end_date:
                # Loop through products sold in this sale
                for product in sale.get("products_sold", []):
                    # Calculate profit for each product in the sale
                    if all(key in product for key in ["price", "supplier_price", "quantity"]):
                        profit_per_unit = product["price"] - product["supplier_price"]
                        total_profit += profit_per_unit * product["quantity"]

        return total_profit

    def get_estimated_profit_this_year(self):
        """
        Calculate the estimated profit for this year's sales.
        
        Returns:
            float: Total profit for this year's sales.
        """
        try:
            # Get the current year
            current_year = datetime.now().year
            
            # Query to fetch this year's sales
            filter = {
                "sale_date": {
                    "$regex": f"^{current_year}-"
                }
            }
            this_year_sales = list(self.connect_to_db('sales').find(filter))
            print(f'Result from getting this year\'s sales: {this_year_sales}')
            
            # Calculate total profit for this year
            total_profit = 0
            for sale in this_year_sales:
                for product in sale.get('products_sold', []):
                    # Calculate profit per product
                    selling_price = product.get('price', 0)
                    supplier_price = product.get('supplier_price', 0)
                    quantity_sold = product.get('quantity', 0)
                    
                    profit = (selling_price - supplier_price) * quantity_sold
                    total_profit += profit
            
            print(f'Total profit for this year: {total_profit}')
            return total_profit
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0

    def get_estimated_profit_last_month(self):
        """
        Calculate the estimated profit for last month's sales.
        
        Returns:
            float: Total profit for last month's sales.
        """
        try:
            # Get the current date and last month
            today = datetime.now()
            first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
            last_month = first_day_last_month.month
            year_last_month = first_day_last_month.year
            
            # Query to fetch last month's sales
            filter = {
                "sale_date": {
                    "$regex": f"^{year_last_month}-{last_month:02d}-"
                }
            }
            last_month_sales = list(self.connect_to_db('sales').find(filter))
            print(f'Result from getting last month\'s sales: {last_month_sales}')
            
            # Calculate total profit for last month
            total_profit = 0
            for sale in last_month_sales:
                for product in sale.get('products_sold', []):
                    # Calculate profit per product
                    selling_price = product.get('price', 0)
                    supplier_price = product.get('supplier_price', 0)
                    quantity_sold = product.get('quantity', 0)
                    
                    profit = (selling_price - supplier_price) * quantity_sold
                    total_profit += profit
            
            print(f'Total profit for last month: {total_profit}')
            return total_profit
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0.0

    def update_profit_label(self, **kwargs):
        """Update the dynamic profit labels based on the selected time period."""
        time_period = kwargs.get('time_period', '')
        if time_period:  # Update profit title label
            self.profit_title_label.setText(f'Profit for {time_period}')
        if time_period == 'Today':
            # start_date = end_date = today.replace(hour=0, minute=0, second=0, microsecond=0)  # Start of today
            formatted_profit = f"₱ {self.get_estimated_profit_today():,.2f}"
            self.estimated_profit_label.setText(str(formatted_profit))
        elif time_period == 'This Week':
            formatted_profit = f"₱ {self.get_estimated_profit_this_week():,.2f}"
            self.estimated_profit_label.setText(str(formatted_profit))
        elif time_period == 'This Month':
            formatted_profit = f"₱ {self.get_estimated_profit_this_month():,.2f}"
            self.estimated_profit_label.setText(str(formatted_profit))
        elif time_period == 'This Year':
            formatted_profit = f"₱ {self.get_estimated_profit_this_year():,.2f}"
            self.estimated_profit_label.setText(str(formatted_profit))
        elif time_period == 'Last Month':
            formatted_profit = f"₱ {self.get_estimated_profit_last_month():,.2f}"
            self.estimated_profit_label.setText(str(formatted_profit))
        else:
            self.estimated_profit_label.setText("₱ 0.00")
            return

    def update_revenue_label(self, **kwargs):
        """update the dynamic revenue labels"""
        time_period = kwargs.get('time_period', '')
        if time_period: # update revenue title label
            self.revenue_title_label.setText(f'Revenue for {time_period}')
        if time_period == 'Today':
            formatted_revenue = f"₱ {self.get_total_revenue_today():,.2f}"
            self.revenue_label.setText(str(formatted_revenue))
        elif time_period == 'This Week':
            formatted_revenue = f"₱ {self.get_total_revenue_this_week():,.2f}"
            self.revenue_label.setText(str(formatted_revenue))
        elif time_period == 'This Month':
            formatted_revenue = f"₱ {self.get_total_revenue_this_month():,.2f}"
            self.revenue_label.setText(str(formatted_revenue))
        elif time_period == 'This Year':
            formatted_revenue = f"₱ {self.get_total_revenue_this_year():,.2f}"
            self.revenue_label.setText(str(formatted_revenue))
        elif time_period == 'Last Month':
            formatted_revenue = f"₱ {self.get_total_revenue_last_month():,.2f}"
            self.revenue_label.setText(str(formatted_revenue))

    def get_total_revenue_today(self):
        # Get today's date (midnight to midnight)
        today_start = datetime.combine(datetime.today(), datetime.min.time())  # Midnight today
        today_end = today_start.replace(hour=23, minute=59, second=59, microsecond=999999)  # Last moment of today

        # Convert start and end to string format (YYYY-MM-DD HH:MM:SS) for comparison with sale_date
        today_start_str = today_start.strftime("%Y-%m-%d %H:%M:%S")
        today_end_str = today_end.strftime("%Y-%m-%d %H:%M:%S")

        # Query for sales made today
        query = {
            'sale_date': {'$gte': today_start_str, '$lte': today_end_str}
        }

        # Aggregate the total revenue by summing the 'total_value' field of all sales made today
        total_revenue = self.connect_to_db('sales').aggregate([
            {'$match': query},
            {'$group': {'_id': None, 'totalRevenue': {'$sum': '$total_value'}}}
        ])

        # Extract the total revenue value
        total_revenue_value = 0
        for result in total_revenue:
            total_revenue_value = result['totalRevenue']

        return total_revenue_value

    def get_total_revenue_this_week(self):
        # Get today's date
        today = datetime.today()

        # Find the start of this week (Monday as the start of the week)
        start_of_week = today - timedelta(days=today.weekday())  # Monday as the start of the week
        if today.weekday() == 0:
            start_of_week -= timedelta(days=7)  # If today is Monday, make it Sunday of the previous week

        # Convert both start_of_week and today to string format (YYYY-MM-DD 00:00:00) for comparison with sale_date
        start_of_week_str = start_of_week.strftime("%Y-%m-%d 00:00:00")  # Start of the week at midnight
        today_str = today.strftime("%Y-%m-%d 23:59:59")  # End of today at 23:59:59 to include all sales of the current day

        # Query for sales made this week
        query = {
            'sale_date': {'$gte': start_of_week_str, '$lt': today_str}
        }

        # Aggregate the total revenue by summing the 'total_value' field of all sales made this week
        total_revenue = self.connect_to_db('sales').aggregate([
            {'$match': query},
            {'$group': {'_id': None, 'totalRevenue': {'$sum': '$total_value'}}}
        ])

        # Extract the total revenue value
        total_revenue_value = 0
        for result in total_revenue:
            total_revenue_value = result['totalRevenue']

        return total_revenue_value

    def get_total_revenue_this_month(self):
        # Get the current date
        now = datetime.now()

        # Calculate the start of the current month
        month_start = datetime(now.year, now.month, 1)

        # Calculate the start of the next month
        if now.month == 12:
            next_month_start = datetime(now.year + 1, 1, 1)
        else:
            next_month_start = datetime(now.year, now.month + 1, 1)

        # Convert both to string format (YYYY-MM-DD 00:00:00) for comparison with sale_date
        month_start_str = month_start.strftime("%Y-%m-%d 00:00:00")  # Start of the month at midnight
        next_month_start_str = next_month_start.strftime("%Y-%m-%d 00:00:00")  # Start of next month at midnight

        # Query for sales made this month
        query = {
            'sale_date': {'$gte': month_start_str, '$lt': next_month_start_str}
        }

        # Aggregate the total revenue by summing the 'total_value' field of all sales made this month
        total_revenue = self.connect_to_db('sales').aggregate([
            {'$match': query},
            {'$group': {'_id': None, 'totalRevenue': {'$sum': '$total_value'}}}
        ])

        # Extract the total revenue value
        total_revenue_value = 0
        for result in total_revenue:
            total_revenue_value = result['totalRevenue']

        return total_revenue_value
    
    def get_total_revenue_this_year(self):
        # Get the current date
        now = datetime.now()

        # Calculate the start of the current year (January 1st)
        year_start = datetime(now.year, 1, 1)

        # Convert year_start to string format (YYYY-MM-DD 00:00:00) for comparison with sale_date
        year_start_str = year_start.strftime("%Y-%m-%d 00:00:00")  # Start of the year at midnight

        # Query for sales made this year
        query = {
            'sale_date': {'$gte': year_start_str}
        }

        # Aggregate the total revenue by summing the 'total_value' field of all sales made this year
        total_revenue = self.connect_to_db('sales').aggregate([
            {'$match': query},
            {'$group': {'_id': None, 'totalRevenue': {'$sum': '$total_value'}}}
        ])

        # Extract the total revenue value
        total_revenue_value = 0
        for result in total_revenue:
            total_revenue_value = result['totalRevenue']

        return total_revenue_value
    
    def get_total_revenue_last_month(self):
        # Get the current date
        now = datetime.now()

        # Calculate the first day of the previous month
        if now.month == 1:
            last_month_start = datetime(now.year - 1, 12, 1)
        else:
            last_month_start = datetime(now.year, now.month - 1, 1)

        # Calculate the last day of the previous month
        if now.month == 1:
            last_month_end = datetime(now.year, 1, 1) - timedelta(days=1)
        else:
            last_month_end = datetime(now.year, now.month, 1) - timedelta(days=1)

        # Convert both to string format (YYYY-MM-DD HH:MM:SS) for comparison with sale_date
        last_month_start_str = last_month_start.strftime("%Y-%m-%d 00:00:00")  # Start of the month at midnight
        last_month_end_str = last_month_end.strftime("%Y-%m-%d 23:59:59")  # End of the month just before midnight

        # Query for sales made last month
        query = {
            'sale_date': {'$gte': last_month_start_str, '$lt': last_month_end_str}
        }

        # Aggregate the total revenue by summing the 'total_value' field of all sales made last month
        total_revenue = self.connect_to_db('sales').aggregate([
            {'$match': query},
            {'$group': {'_id': None, 'totalRevenue': {'$sum': '$total_value'}}}
        ])

        # Extract the total revenue value
        total_revenue_value = 0
        for result in total_revenue:
            total_revenue_value = result['totalRevenue']

        return total_revenue_value
    
    def load_button_connections(self):
        """load all the button connections"""
        self.search_pushButton.clicked.connect(lambda: self.search_button_clicked())
        self.back_pushButton.clicked.connect(lambda: self.handle_back_button())
        self.prev_pushButton.clicked.connect(lambda: self.update_sales_table(self.current_page - 1, self.rows_per_page))
        self.next_pushButton.clicked.connect(lambda: self.update_sales_table(self.current_page + 1, self.rows_per_page))
        self.create_sales_report_pushButton.clicked.connect(lambda: self.create_sales_report())
        self.time_period_comboBox.currentTextChanged.connect(lambda text: self.handle_time_period_comboBox(text))
        self.confirm_date_pushButton.clicked.connect(lambda: self.handle_confirm_date_pushButton())
        self.search_lineEdit.textChanged.connect(lambda: self.handle_search())

    def handle_confirm_date_pushButton(self):
        """handle confirm date pushButton click event"""
        self.update_sales_table()

    def handle_time_period_comboBox(self, current_text):
        """handle the time period combobox text changed event"""
        print(f'Current text: {current_text}')
        if current_text == 'Custom':
            self.custom_time_period_frame.show()
        else:
            self.custom_time_period_frame.hide()
            self.update_profit_label(time_period=current_text)
            self.update_revenue_label(time_period=current_text)
            self.update_sales_table()

    def load_filters(self):
        """load all the filters"""
        self.load_time_period_filter()

    def load_time_period_filter(self):
        """load the time period filter"""
        filters_dir = self.dirs.get_path('filters')
        with open(filters_dir, 'r') as f:
            data = json.load(f)

        # clear combo box
        self.time_period_comboBox.clear()

        for time in data['time_period']:
            self.time_period_comboBox.addItem(list(time.values())[0])

    def create_sales_report(self):
        """Create sales report"""
        try:
            # Fetch sales data
            sales_data = self.connect_to_db("sales").find()

            # Initialize PDF in landscape mode
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Title and Company Name
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(200, 10, txt="Magtibay LPG Trading", ln=True, align='C')  # Company Name
            pdf.ln(3)

            # Date (removing the time)
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%b. %d, %Y")  # "Jul. 20, 2020" format
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 5, txt=f"Date: {formatted_date}", ln=True, align='C')  # Current Date
            pdf.ln(10)

            # Title
            pdf.set_font("Arial", style='B', size=16)
            pdf.cell(200, 10, txt="Sales Report", ln=True, align='C')
            pdf.ln(10)

            # Table headers
            pdf.set_font("Arial", style='B', size=10)
            headers = ["Sale ID", "Customer Name", "Sale Date", "Product ID", "Product Name", "Cylinder Size", "Quantity", "Price/Unit", "Total Amount"]
            for header in headers:
                pdf.cell(30, 10, txt=header, border=1, align='C')  # Centered text
            pdf.ln()

            # Table data
            pdf.set_font("Arial", size=10)
            for sale in sales_data:
                sale_id = sale["sale_id"]
                customer_name = sale["customer_name"]
                
                # Check if sale_date is already a datetime object, if not, parse it
                sale_date = sale["sale_date"]
                if isinstance(sale_date, datetime):
                    formatted_sale_date = sale_date.strftime("%b. %d, %Y")  # Formatting the sale date
                else:
                    # If it's not a datetime object, then convert it using strptime()
                    sale_date = datetime.strptime(sale_date, "%Y-%m-%d")
                    formatted_sale_date = sale_date.strftime("%b. %d, %Y")  # Only include the date, no time

                # Iterate through the products_sold array
                for product in sale["products_sold"]:
                    product_id = product["product_id"]
                    product_name = product["product_name"]
                    cylinder_size = product["cylinder_size"]
                    quantity = product["quantity"]
                    price = product["price"]
                    total_amount = product["total_amount"]
                    
                    pdf.cell(30, 10, txt=sale_id, border=1, align='C')  # Sale ID
                    pdf.cell(30, 10, txt=customer_name, border=1, align='C')  # Customer Name
                    pdf.cell(30, 10, txt=formatted_sale_date, border=1, align='C')  # Sale Date
                    pdf.cell(30, 10, txt=product_id, border=1, align='C')  # Product ID
                    pdf.cell(30, 10, txt=product_name, border=1, align='C')  # Product Name
                    pdf.cell(30, 10, txt=cylinder_size, border=1, align='C')  # Cylinder Size
                    pdf.cell(30, 10, txt=str(quantity), border=1, align='C')  # Quantity
                    pdf.cell(30, 10, txt=f"{price:,.2f}", border=1, align='C')  # Price/Unit
                    pdf.cell(30, 10, txt=f"{total_amount:,.2f}", border=1, align='C')  # Total Amount
                    pdf.ln()

            # Open directory selection dialog
            folder = QFileDialog.getExistingDirectory(None, "Select Folder")

            if folder:
                # Save PDF with dynamic filename in the selected directory
                filename = f"{folder}/sales_report_{formatted_date.replace(' ', '_').replace('.', '')}.pdf"
                pdf.output(filename)
                CustomMessageBox.show_message('information', 'Success', f"Sales report generated successfully! Filename: {filename}")
                self.logs.record_log(event='sales_report')
            else:
                print("No folder selected.")
                CustomMessageBox.show_message('warning', 'Error', "No folder selected. Please select a folder to save the report.")
                
        except Exception as e:
            print(f'Error: {e}')
            CustomMessageBox.show_message('critical', 'Error', f"An error occurred while creating the sales report: {e}")

    def handle_search(self):
        """Handle the search functionality of the search bar"""
        if self.search_lineEdit.text() == "":
            self.update_sales_table()

    def search_button_clicked(self):
        """Handles the search button click event"""
        print(f"Search bar Text: {self.search_lineEdit.text()}")
        self.update_sales_table()

    def set_icons(self):
        """Set icons to buttons"""
        self.search_pushButton.setIcon(QIcon(self.dirs.get_path('search_icon')))

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

    def update_top_product(self):
        data = self.get_top_10_best_selling_products()

        if data:
            top_product_id: str = data[0]['product_id']
            top_product_name: str = data[0]['product_name']
            self.best_selling_label.setText(f"{top_product_id} ({top_product_name})")

    def update_best_selling_chart(self):
        layout = self.best_selling_prod_scrollAreaWidgetContents.layout()
        if layout is None:
            layout = QVBoxLayout() # Create new layout if no layout
        else:
            print(f'Layout exists')

        # Clear all existing widgets from the layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        top_products = self.get_top_10_best_selling_products()
        for product in top_products:
            best_selling_prod_item = BestSellingListItem(product)
            layout.addWidget(best_selling_prod_item)

    def get_top_10_best_selling_products(self):
        """
        Returns the top 10 best-selling products based on the quantity sold, including price.

        :return: List of dictionaries containing product details and total quantity sold
        """
        pipeline = [
            # Unwind the products_sold array
            {"$unwind": "$products_sold"},
            
            # Group by product_id, product_name, and cylinder_size, summing the quantities sold
            {
                "$group": {
                    "_id": {
                        "product_id": "$products_sold.product_id",
                        "product_name": "$products_sold.product_name",
                        "cylinder_size": "$products_sold.cylinder_size",
                        "price": "$products_sold.price"  # Assuming price exists here
                    },
                    "total_quantity_sold": {"$sum": "$products_sold.quantity"},
                    "total_value_sold": {"$sum": "$products_sold.total_amount"}
                }
            },
            
            # Sort by total_quantity_sold in descending order
            {"$sort": {"total_quantity_sold": -1}},
            
            # Limit to the top 10
            {"$limit": 10},
            
            # Format the result
            {
                "$project": {
                    "_id": 0,
                    "product_id": "$_id.product_id",
                    "product_name": "$_id.product_name",
                    "cylinder_size": "$_id.cylinder_size",
                    "total_quantity_sold": 1,
                    "total_value_sold": 1,
                    "price": "$_id.price"
                }
            }
        ]
        
        top_10_products = list(self.connect_to_db('sales').aggregate(pipeline))
        return top_10_products
    
    def load_inventory_monitor(self):
        # monitor for today sales
        self.sales_monitor = InventoryMonitor("sales")
        self.sales_monitor.start_listener_in_background()
        self.sales_monitor.data_changed_signal.connect(lambda: self.update_labels())

    def update_labels(self):
        # self.update_today_sales()
        # self.update_revenue_this_month()
        self.update_sales_table()
        self.update_sales_trend_chart()
        self.update_best_selling_chart()
        self.update_top_product()
        self.update_revenue_label()
        # self.load_bar_chart()
        
    def get_last_7_days_sales(self):
        pipeline = [
            {
                "$match": {
                    "sale_date": {
                        "$gte": datetime.now() - timedelta(days=7)
                    }
                }
            },
            {
                "$group": {
                    "_id": "$sale_date",
                    "sales": {"$sum": "$total_value"}
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
        Fetches sales data for the last 7 days.
        Returns a list of tuples (date, sales_amount).
        """
        # Get the current date and calculate 7 days ago
        today = datetime.now()
        seven_days_ago = today - timedelta(days=7)

        # Convert the dates to ISO format strings to match the database format
        today_str = today.strftime("%Y-%m-%d %H:%M:%S")
        seven_days_ago_str = seven_days_ago.strftime("%Y-%m-%d %H:%M:%S")

        # Query the database directly for sales within the last 7 days
        pipeline = [
            {
                "$match": {
                    "sale_date": {
                        "$gte": seven_days_ago_str,
                        "$lte": today_str
                    }
                }
            },
            {
                "$project": {
                    "sale_date": {
                        "$toDate": "$sale_date"  # Convert sale_date string to date object
                    },
                    "total_value": 1  # Include total_value in the output for summing up
                }
            },
            {
                "$group": {
                    "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$sale_date"}},  # Group by date only
                    "sales": {"$sum": "$total_value"}  # Sum the total_value for the day
                }
            },
            {
                "$sort": {
                    "_id": 1  # Sort by date in ascending order
                }
            }
        ]

        # Execute the aggregation pipeline directly on the database
        sales_data_from_db = list(self.connect_to_db("sales").aggregate(pipeline))

        # Initialize a dictionary to store sales summed by date
        sales_by_date = {}

        # Process the sales data
        for data in sales_data_from_db:
            # Assuming '_id' is a string representing the date
            date_str = data['_id']  # '_id' contains the date (e.g., "2025-01-13")
            print(f'date string: {date_str}')
            
            # Parse the string to a datetime object
            sale_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            print(f'Date datetime: {sale_date}')
            
            # Use the date as key, and sum the sales
            sales = data['sales']  # Sales for the given date
            print(f'Testing ng sales: {sales}')
            sales_by_date[sale_date] = sales_by_date.get(sale_date, 0) + sales
            print(f'sales by date: {sales_by_date}')

        # Prepare sales data for the last 7 days
        sales_data = []
        
        # Loop over the last 7 days
        for i in range(7):
            current_date = (today - timedelta(days=i)).date()  # Get date without time
            print(f'current date: {current_date}')
            # Fetch sales for this date, or use 0 if no sales data exists
            sales = sales_by_date.get(current_date, 0)
            sales_data.append((current_date.strftime("%Y-%m-%d"), sales))

        sales_data.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))

        print(f'Testing sales data: {sales_data}')
        return sales_data  # Reverse to have the oldest date first

    def create_sale_trend_chart(self, sales_data):
        chart = QChart()
        chart.setTitle("")
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
        # Get sales data
        sales_data = self.get_sales_data()
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
            header_dir = self.dirs.get_path('sales_header')

            # Settings directory
            settings_dir = self.dirs.get_path('settings')

            with open(header_dir, 'r') as f:
                header_labels = json.load(f)

            table.setColumnCount(len(header_labels))
            table.setHorizontalHeaderLabels(header_labels)

            header = self.sales_tableWidget.horizontalHeader()
            header.setSectionsMovable(True)
            header.setDragEnabled(True)
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            for column in range(table.columnCount()):
                table.setColumnWidth(column, 145)

            # Set uniform row height for all rows
            table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50

            header.setFixedHeight(40)
            table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
            table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

            # Clean the header labels
            self.header_labels = [self.clean_header(header) for header in header_labels]
            
            # query filter
            filter = {}

            if self.search_lineEdit.text().strip():  # Check if the input is not empty and strip any whitespace
                filter = {
                    "sale_id": {"$regex": self.search_lineEdit.text(), "$options": "i"}  # Case-insensitive match
                }

            today = datetime.now()
            time_period = self.time_period_comboBox.currentText()

            if time_period == "Today":
                today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
                today_end = today_start + timedelta(days=1)
                filter = {
                    "sale_date": {
                        "$gte": today_start.strftime('%Y-%m-%d %H:%M:%S'),
                        "$lt": today_end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            elif time_period == "This Week":
                week_start = today - timedelta(days=today.weekday())  # Monday of the current week
                week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                week_end = week_start + timedelta(days=7)  # End of the current week (next Monday 0:00)
                filter = {
                    "sale_date": {
                        "$gte": week_start.strftime('%Y-%m-%d %H:%M:%S'),
                        "$lt": week_end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            elif time_period == "This Month":
                month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                if today.month == 12:
                    month_end = datetime(today.year + 1, 1, 1, 0, 0, 0)
                else:
                    month_end = datetime(today.year, today.month + 1, 1, 0, 0, 0)
                filter = {
                    "sale_date": {
                        "$gte": month_start.strftime('%Y-%m-%d %H:%M:%S'),
                        "$lt": month_end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            elif time_period == "This Year":
                year_start = datetime(today.year, 1, 1, 0, 0, 0)
                year_end = datetime(today.year + 1, 1, 1, 0, 0, 0)
                filter = {
                    "sale_date": {
                        "$gte": year_start.strftime('%Y-%m-%d %H:%M:%S'),
                        "$lt": year_end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            elif time_period == "Last Month":
                if today.month == 1:
                    last_month_start = datetime(today.year - 1, 12, 1, 0, 0, 0)
                    last_month_end = datetime(today.year, 1, 1, 0, 0, 0)
                else:
                    last_month_start = datetime(today.year, today.month - 1, 1, 0, 0, 0)
                    last_month_end = datetime(today.year, today.month, 1, 0, 0, 0)
                filter = {
                    "sale_date": {
                        "$gte": last_month_start.strftime('%Y-%m-%d %H:%M:%S'),
                        "$lt": last_month_end.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            elif time_period == "Custom":
                start_date_qdate = self.start_date_dateEdit.date()
                end_date_qdate = self.end_date_dateEdit.date()
                start_date = start_date_qdate.toPyDate()
                end_date = end_date_qdate.toPyDate()
                start_date = datetime.combine(start_date, datetime.min.time())
                end_date = datetime.combine(end_date, datetime.max.time())
                filter = {
                    "sale_date": {
                        "$gte": start_date.strftime('%Y-%m-%d %H:%M:%S'),
                        "$lt": end_date.strftime('%Y-%m-%d %H:%M:%S')
                    }
                }

            # Get data from MongoDB
            data = list(self.connect_to_db('sales').find(filter).sort("_id", -1))
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

                        if header == 'totalvalue':
                            try:
                                if value:
                                    formatted_value = f"₱ {value:,.2f}"
                                    value = formatted_value

                            except Exception as e:
                                print(f"Error: {e}")

                        elif header == 'saledate':
                            try:
                                if value:
                                    # convert string to datetime object
                                    datetime_object = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                                    # convert back to string using strftime
                                    value = datetime_object.strftime("%Y-%m-%d")
                            except Exception as e:
                                print(f'May Error: {e}')                           

                        elif header == 'productssold':
                            # Ensure value is a list
                            if isinstance(value, list):
                                product_num = len(value)
                                
                                view_prod_pushButton = QPushButton('View Products')
                                view_prod_pushButton.clicked.connect(lambda _, v=value, r=row: self.handle_view_products_button(v, r))
                                # view_prod_pushButton.clicked.connect(lambda: self.handle_view_products_button())
                                view_prod_pushButton.setStyleSheet("""
                                color: #000;
                                border: 1px solid #000;
                                """)
                                self.sales_tableWidget.setCellWidget(row, column, view_prod_pushButton)

                                continue
                            else:
                                value = "Invalid product data"

                        # Add the value to the table as a QTableWidgetItem
                        table_item = QTableWidgetItem(str(value))
                        table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text

                        # Check if row index is even for alternating row colors
                        if row % 2 == 0:
                            table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                        
                        table.setItem(row, column, table_item)

    def load_view_products_table(self, products, page=0, rows_per_page=10):
        """Load the view products table with the products sold"""
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
        header_dir = self.dirs.get_path('view_products_header')
        # Settings directory
        settings_dir = self.dirs.get_path('settings')
        with open(header_dir, 'r') as f:
            header_labels = json.load(f)
        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)
        header = self.sales_tableWidget.horizontalHeader()
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
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

        if self.search_lineEdit.text().strip():  # Check if the input is not empty and strip any whitespace
            filter = {
                "product_name": {"$regex": self.search_lineEdit.text(), "$options": "i"}  # Case-insensitive match
            }

        # Get data from MongoDB
        # data = list(self.connect_to_db('sales').find(filter).sort("_id", -1))
        data = list(products)
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
                    if header == 'price':
                        try:
                            if value:
                                formatted_value = f"₱ {value:,.2f}"
                                value = formatted_value
                        except Exception as e:
                            print(f"Error: {e}")
                    elif header == 'totalamount':  
                        try:
                            if value:
                                formatted_value = f"₱ {value:,.2f}"
                                value = formatted_value
                        except Exception as e:
                            print(f"Error: {e}")
                    # Add the value to the table as a QTableWidgetItem
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
                    # Check if row index is even for alternating row colors
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))  # Change item's background color
                    
                    table.setItem(row, column, table_item)

    def handle_view_products_button(self, products, row):
        """Handle the 'View Products' button click event"""
        self.clear_sales_table()
        self.show_back_button()
        self.load_view_products_table(products)

    def handle_back_button(self):
        """Handle the 'Back' button click event"""
        self.update_sales_table()
        self.hide_back_button()

    def hide_back_button(self):
        """Hide back button"""
        self.frame_14.hide()
    
    def show_back_button(self):
        """Show back button"""
        self.frame_14.show()
    
    def clear_sales_table(self):
        """Clear sales table including the header"""
        table = self.sales_tableWidget
        table.clearContents()
        table.setRowCount(0)
        table.setColumnCount(0)

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
                    "sale_date": {
                        "$gte": first_day_of_month,  # Match documents from the start of the current month
                        "$lt": first_day_of_next_month  # Exclude documents from the next month
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {"$sum": "$total_value"}  # Sum the total_amount field
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

    def get_total_sales_today(self):
        # Define the start of the day (midnight) for today
        today_start = datetime.combine(datetime.now().date(), datetime.min.time())
        pipeline = [
            {
                "$match": {
                    "sale_date": {"$gte": today_start}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_sales": {"$sum": "$total_value"}
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
