from PyQt6.QtWidgets import *
from PyQt6.QtCore import QThread, pyqtSignal, QSize, QPropertyAnimation, Qt

from src.ui.ui_dashboard import Ui_Form as Ui_dashboard_page
from src.ui.final_ui.product_in_stock_item import Ui_Frame as Ui_prodStockItem
from src.ui.final_ui.product_in_stock_info import Ui_frame_info as Ui_prodStockInfo

from src.utils.Inventory_Monitor import InventoryMonitor
from src.utils.dir import ConfigPaths

from datetime import datetime, timedelta
from collections import defaultdict
import pymongo, json, re

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class ProductInStockItem(QFrame, Ui_prodStockItem):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class ProductInStockInfo(QFrame, Ui_prodStockInfo):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class Dashboard(QWidget, Ui_dashboard_page):
    def __init__(self, username, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window
        
        self.directory = ConfigPaths()

        self.load_collection_monitors()

        self.update_sales_widgets()
        self.load_sales_today_table()

        # Set up the layout for the QScrollArea
        cylinderContainerWidget = self.cylinderContainerLayout
        self.cylinderContainerLayout = QVBoxLayout(cylinderContainerWidget)
        self.cylinderTypes_scrollArea.setWidget(cylinderContainerWidget)

        self.labels = []

        self.update_stock_widgets()

        # Call the function to update the cylinder list
        self.update_cylinder_list()
        self.create_cylinder_sizes_tab()


    def get_today_total_orders(self):
        """
        Get the total number of orders placed today and display it in the label.
        
        Returns:
            int: Total number of orders placed today.
        """
        try:
            # Get today's date in the format 'YYYY-MM-DD'
            today_date = datetime.now().strftime('%Y-%m-%d')

            # Query the collection for orders with today's date
            total_orders = self.connect_to_db('orders').count_documents({"order_date": today_date})

            # update the label
            self.total_orders_label.setText(str(total_orders))
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def create_cylinder_sizes_tab(self):
        """ Get all the cylinder sizes and create a tab for each cylinder size """
        try:
            # Get distinct cylinder sizes
            cylinder_sizes = self.connect_to_db('products').distinct('cylinder_size')

            # Sort the cylinder sizes in descending order
            cylinder_sizes.sort(reverse=True)

            # initialize tab widget
            self.tab_widget = self.sizes_tabWidget
            self.tab_widget.clear()
            
            # Add a tab for each cylinder size
            for size in cylinder_sizes:
                # Create the tab widget for this size
                tab_widget = QWidget()

                # Create the Matplotlib figure and canvas
                self.figure, self.ax = plt.subplots(figsize=(5, 5))
                self.canvas = FigureCanvas(self.figure)

                # initialize layout for tab widget
                tab_widget_layout = QVBoxLayout()
                tab_widget_layout.addWidget(self.canvas) # insert pie chart canvas to the layout
                
                tab_widget.setLayout(tab_widget_layout) # add the layout to the tab widget

                # get data for the chart
                product_data = list(self.get_cylinder_brands(size))
                print(f'recevied product data {product_data}')

                brand = []
                quantity = []
                for data in product_data:
                    brand.append(data['product_name'])
                    quantity.append(data['quantity_in_stock'])

                print(f'pakening quantity: {quantity}')

                self.create_pie_chart(brand, quantity) # create pie chart

                # Add the tab to the tab widget
                self.tab_widget.addTab(tab_widget, f"{size}")

        except Exception as e:
            print(f"Error: {e}")

    def create_pie_chart(self, brand, quantity):
        """
        Create a pie chart for each cylinder size.
        
        Args:
            brand (list): Labels for the pie chart (e.g., cylinder sizes).
            quantity (list): Corresponding quantities for the pie chart.
        """
        # Check for data consistency
        if len(brand) != len(quantity):
            raise ValueError("The length of brand and quantity must be the same.")
        
        print(f"Received quantity: {quantity}, type: {type(quantity)}")

        # Convert quantities to numbers if needed
        quantity = [int(q) if isinstance(q, str) else q for q in quantity]

        # Define colors for the chart (expand or reuse if more data points exist)
        colors = ['gold', 'lightblue', 'lightgreen', 'coral', 'pink', 'gray']

        # Plot the pie chart
        self.ax.clear()  # Clear the plot if it was used before
        self.ax.pie(
            quantity,
            labels=brand,
            colors=colors[:len(brand)],  # Match colors to data length
            autopct=lambda pct: f"{int(pct * sum(quantity) / 100)}",
            startangle=140,
            textprops=dict(color="black"),  # Text styling
        )
        self.ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle

        # Refresh the canvas
        self.canvas.draw()

    def get_cylinder_brands(self, cylinder_size):
        """ Get all the cylinder brands for a given cylinder size and get their quantity """
        query = {'cylinder_size': cylinder_size}
        projection = {'product_name': 1, 'cylinder_size': 1, 'quantity_in_stock': 1, '_id': 0}
        result = list(self.connect_to_db('products').find(query, projection))
        
        return result

    def update_sales_widgets(self):
        """update all the widgets that uses sales data"""
        self.load_sales_today_table()
        self.udpate_sales_today_label()
        self.update_total_sales_in_table()

    def load_collection_monitors(self):
        """initialize the monitors for the collections"""
        self.sales_monitor = InventoryMonitor('sales')
        self.sales_monitor.start_listener_in_background()
        self.sales_monitor.data_changed_signal.connect(self.update_sales_widgets)

        # Initialize the products monitor to listen for changes
        self.products_monitor = InventoryMonitor('products')
        self.products_monitor.start_listener_in_background()
        self.products_monitor.data_changed_signal.connect(self.update_stock_widgets)

        # # Initialize orders monitor
        # self.order_monitor = InventoryMonitor('orders')
        # self.order_monitor.start_listener_in_background()
        # self.order_monitor.data_changed_signal.connect(self.orders_coll_change)

    def update_total_sales_in_table(self):
        """Update the total sales in the table"""
        # Get the data for today's sales
        data = self.get_products_sold_today()

        # Format the total sales amount as currency
        total_sale_amount = f"₱ {data['total_sales_amount']:,.2f}"
        print(f'total sale amount: {total_sale_amount}')

        # Update the label with the formatted total sales amount
        self.total_sale_table_label.setText(total_sale_amount)

    def load_sales_today_table(self):
        """load the sales today table"""
        table = self.sales_today_tableWidget
        table.setSortingEnabled(True)
        vertical_header = table.verticalHeader()
        vertical_header.hide()
        table.setRowCount(0)  # Clear the table
        table.setSelectionMode(table.SelectionMode.NoSelection)

        # header json directory
        header_dir = self.directory.get_path('sales_today_header')
        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        header = self.sales_today_tableWidget.horizontalHeader()
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setStretchLastSection(True)

        # # set width of all the columns
        # for column in range(table.columnCount()):
        #     table.setColumnWidth(column, 150)

        table.verticalHeader().setDefaultSectionSize(50)  # Set all rows to a height of 50
        # Set uniform row height for all rows
        header.setFixedHeight(40)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]
        print(f'header labels: {self.header_labels}')

        data = self.get_products_sold_today() # get data for the table
        products = data['products']

        if products:
            self.no_sales_frame.hide()
            self.sales_today_tableWidget.show()
        else:
            self.no_sales_frame.show()
            self.sales_today_tableWidget.hide()
        
        for row, item in enumerate(products):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                # Clean and match the keys
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)

                if value is not None:
                    # Check if the header is 'price'
                    if header == 'price':
                        
                        # Ensure the value is a float before formatting
                        if isinstance(value, (int, float)):
                            formatted_price = f"₱ {value:,.2f}"  # Format value as price with two decimals
                            print(f'Formatted price: {formatted_price}')
                            value = formatted_price
                        else:
                            print('Value is not a valid number')
                        
                    # For other columns
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, column, table_item)

    def get_products_sold_today(self):
        # Connect to the MongoDB instance
        # Get today's date
        today = datetime.now()
        start_of_day = datetime(today.year, today.month, today.day)
        end_of_day = start_of_day + timedelta(days=1)

        # Aggregation pipeline to ensure `sale_date` is converted to a date object
        pipeline = [
            {
                "$addFields": {
                    "sale_date": {
                        "$dateFromString": {
                            "dateString": "$sale_date",  # Assumes `sale_date` is stored as a string
                            "format": "%Y-%m-%d %H:%M:%S"  # Adjust format as per your database
                        }
                    }
                }
            },
            {
                "$match": {
                    "sale_date": {"$gte": start_of_day, "$lt": end_of_day}
                }
            }
        ]

        # Query to find all sales from today using the aggregation pipeline
        sales_today = list(self.connect_to_db('sales').aggregate(pipeline))

        # Dictionary to store product data, combining same product IDs
        products = defaultdict(lambda: {
            "product_name": "",
            "cylinder_size": "",
            "quantity": 0,
            "total_amount": 0
        })

        # Variable to track total sales amount
        total_sales_amount = 0

        # Process each sale
        for sale in sales_today:
            for product in sale.get("products_sold", []):
                product_id = product["product_id"]
                products[product_id]["product_name"] = product.get("product_name", "")
                products[product_id]["cylinder_size"] = product.get("cylinder_size", "")
                products[product_id]["quantity"] += product.get("quantity", 0)
                products[product_id]["total_amount"] += product.get("total_amount", 0)
                
                # Add the product's total amount to the overall total sales amount
                total_sales_amount += product.get("total_amount", 0)

        # Sort products by cylinder size (extract numeric value for sorting)
        def extract_size(cylinder_size):
            try:
                # Extract numeric part (e.g., '11' from '11kg')
                return int(''.join(filter(str.isdigit, cylinder_size)))
            except ValueError:
                # Default to a very high number if parsing fails (to sort unknown sizes last)
                return float('inf')

        sorted_products = sorted(products.values(), key=lambda x: extract_size(x["cylinder_size"]))

        # Return the processed product data as a list along with the total sales amount
        return {
            "products": [
                {
                    "brand": data["product_name"],
                    "size": data["cylinder_size"],
                    "quantity": data["quantity"],
                    "price": data["total_amount"]
                }
                for data in sorted_products
            ],
            "total_sales_amount": total_sales_amount
        }

    def udpate_sales_today_label(self):
        """update sales today label"""
        sales = self.get_today_sales()
        formatted = f"{sales:,.2f}"
        self.total_sales_label.setText(formatted)

    def orders_coll_change(self):
        """Update all the widgets with orders data related"""
        self.display_total_orders()
        self.update_total_orders()

    def update_total_orders(self):
        """Update total orders label (all orders in the system)."""
        try:
            # Count the total number of orders in the database
            total_orders = self.connect_to_db("orders").count_documents({})
            
            # Update the label with the total orders
            self.total_orders_label.setText(f"{total_orders:,}")
            print(f"Total orders: {total_orders}")
        except Exception as e:
            print(f"Error getting total orders: {e}")

    def get_today_sales(self):
        """Get data for today's sale (current sales today)"""
        # Define the start of the day (midnight) for today
        today_start = datetime.combine(datetime.now().date(), datetime.min.time())

        pipeline = [
            {
                "$addFields": {
                    "sale_date": {
                        "$dateFromString": {
                            "dateString": "$sale_date",  # Assuming `sale_date` is stored as a string
                            "format": "%Y-%m-%d %H:%M:%S"  # Adjust format as per your database
                        }
                    }
                }
            },
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

        # Run the pipeline and convert the result to a list for easier handling
        result = list(self.connect_to_db("sales").aggregate(pipeline))
        
        if result:  # If result is not empty
            total_sales = result[0].get("total_sales", 0)
            return total_sales
        else:
            return 0  # Default to 0 if no sales found

    def expand_total_prods(self):
        """Expand total products frame"""
        print(f'Expanding total products frame')

        self.frame_16.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Get current height of the frame
        current_height = self.frame_16.height()
        current_width = self.frame_16.width()

        min_h = self.frame_16.minimumHeight()
        max_h = self.frame_16.maximumHeight()

        # Toggle between small and large height
        if current_height >= 170:  # If the height is large, shrink it
            start_size = QSize(current_width, current_height)
            end_size = QSize(current_width, min_h)
        else:  # If the height is small, expand it
            start_size = QSize(current_width, current_height)
            end_size = QSize(current_width, max_h)

        # Create and start the animation for resizing frame_16
        self.animation = QPropertyAnimation(self.frame_16, b"size")
        self.animation.setDuration(150)  # Duration in milliseconds
        self.animation.setStartValue(start_size)
        self.animation.setEndValue(end_size)
        self.animation.start()

        # After the animation is finished, trigger layout recalculations
        self.frame.layout().invalidate()  # Invalidate the layout to force a reflow
        self.frame.layout().activate()  # Ensure layout recalculation
        self.frame.adjustSize()  # Adjust the size of frame to fit the child widgets
        self.frame.updateGeometry()  # Recalculate the geometry of frame
        self.frame.update()  # Force the parent layout to redraw

    def get_product_name_and_cylinder_size(self):
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": {"product_name": "$product_name", "cylinder_size": "$cylinder_size"},
                    }
                }
            ]
            result = self.connect_to_db("products").aggregate(pipeline)
            product_data = []
            for item in result:
                product_name = item['_id']['product_name']
                cylinder_size = item['_id']['cylinder_size']
                product_data.append({
                    "product_name": product_name,
                    "cylinder_size": cylinder_size
                })
            return product_data
        except Exception as e:
            print(f"Error getting product name and cylinder size: {e}")
            return []

    def update_total_products(self):
        """Update the total products label"""
        total_products = len(self.get_product_name_and_cylinder_size())
        print(f'result: {total_products}')
        self.totalItemStock_label.setText(str(total_products))

    def set_icons(self):
        """Add icons to buttons and labels"""
        # self.expand_total_prod_pushButton.setIcon(QIcon("app/resources/icons/expand.png"))
        pass

    def update_stock_widgets(self):
        self.update_cylinder_list()
        self.create_cylinder_sizes_tab()
        self.get_today_total_orders()

    def load_stock_level_chart(self):
        print(f'showing stock level chart')
        # get data from database

        processed_data = self.get_quantity_in_stock()
        print(processed_data)
        # for data in processed_data:
        #     cylinder_size = data['cylinder_size']
        #     total_quantity = data['total_quantity']

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
    
    def get_products_in_stock(self):
        """
        Retrieves total stock of each product size and provides a breakdown by product name, including quantities.

        Returns:
            dict: A dictionary with product sizes as keys and a summary as values.
        """
        pipeline = [
            {
                "$group": {
                    "_id": {"size": "$cylinder_size", "product_name": "$product_name"},
                    "quantity": {"$sum": "$quantity_in_stock"}
                }
            },
            {
                "$group": {
                    "_id": "$_id.size",
                    "total_stock": {"$sum": "$quantity"},
                    "suppliers": {
                        "$push": {
                            "product_name": "$_id.product_name",
                            "quantity": "$quantity"
                        }
                    }
                }
            },
            {
                "$sort": {"_id": 1}  # Sort by cylinder size
            }
        ]

        results = self.connect_to_db("products").aggregate(pipeline)
        products_in_stock = {}

        for item in results:
            size = item['_id']
            products_breakdown = {
                product['product_name']: product['quantity'] for product in item['suppliers']
            }
            products_in_stock[size] = {
                "total_stock": item['total_stock'],
                "products": products_breakdown
            }

        return products_in_stock
    
    def update_cylinder_list(self):
        processed_data = self.get_products_in_stock()
        self.display_cylinder_data(processed_data)

    def display_cylinder_data(self, processed_data):
        """
        Updates the scroll area with new cylinder data, including product name details.
        """
        # Clear existing labels
        for label in self.labels:
            self.cylinderContainerLayout.removeWidget(label)
            label.deleteLater()
        self.labels.clear()

        layout = self.cylinderContainerLayout.layout()
    
        # If the layout exists, iterate through all the items and remove them
        if layout:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget()
                
                # If the item is a widget, remove it
                if widget:
                    widget.deleteLater()  # This deletes the widget and removes it from the layout
                    
        # Create new labels based on processed data
        for size, details in processed_data.items():
            total_stock = details['total_stock']
            products = details['products']

            # Create an instance of ProductInStockItem (assumed to be a custom widget)
            list_item = ProductInStockItem()
            list_item.cylinder_size_label.setText(size)
            list_item.quantity_in_stock_label.setText(str(total_stock))

            # Add product-specific details to frame_6
            for product_name, quantity in products.items():
                # Create a new ProductInStockInfo (assumed to be a custom widget)
                prod_info = ProductInStockInfo()
                prod_info.prod_name_label.setText(f"{product_name}:")
                prod_info.quantity_label.setText(str(quantity))

                print(f"product name text: {prod_info.prod_name_label.text()}")

                # Make sure frame_6 has a layout set before adding widgets
                if not list_item.frame_6.layout():
                    list_item.frame_6.setLayout(QVBoxLayout())  # Example of setting a layout if not set

                # Add product info widget to the layout of frame_6
                list_item.frame_6.layout().addWidget(prod_info)

            # Add the list item widget (which holds product info) to cylinderContainerLayout
            self.cylinderContainerLayout.addWidget(list_item)

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
            # Run the aggregation pipeline on the "products" collection
            result = self.connect_to_db("products").aggregate(pipeline)

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
            total_stock = self.get_quantity_in_stock()
        try:
            # print(f'total quantity: {total_stock}')
            self.totalItemStock_label.setText(f'{total_stock}')
        except Exception as e:
            print(e)

    def get_total_stock(self):
        """Get the total quantity of all items in stock."""
        try:
            pipeline = [
                {
                    "$group": {
                        "total_quantity": {"$sum": "$price_per_unit"}  # Sum the quantities
                    }
                }
            ]
            result = self.connect_to_db("products").aggregate(pipeline)
            total_quantity = next(result, {}).get('total_quantity', 0)  # Get the total or default to 0
            print(f'Total quantity in stock: {total_quantity}')
            return total_quantity
        except Exception as e:
            print(f"Error getting total quantity in stock: {e}")
            return 0

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
            return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))