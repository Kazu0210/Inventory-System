from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QTimer
import pymongo
from ui.employee.orderPage import Ui_Form as Ui_order_page
# from ui.employee.update_order_form import Ui_Frame as Ui_update_form
# from ui.employee.add_order_item import Ui_Frame as Ui_add_form

from pages.employee.new_order_page import AddOrderForm
from pages.employee.update_order_page import UpdateOrderForm
import json
import re

class OrdersPage(QWidget, Ui_order_page):
    def __init__(self, username, dashboard_mainWindow=None):
        super().__init__()
        self.setupUi(self)
        
        self.update_filters()

        self.dashboard_mainWindow = dashboard_mainWindow

        self.setWindowTitle("Main Window")
        self.open_form_button = QPushButton("Open Form")
        self.open_form_button.clicked.connect(lambda: self.on_open_form_clicked(order_id=None)) 
        self.add_form_button.clicked.connect(lambda: self.on_add_form_clicked(order_id=None)) 

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.open_form_button)
        container = QWidget()
        container.setLayout(layout)

        # Connect to MongoDB
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)

        try:
            client.admin.command('ping')
            print("Connected to MongoDB successfully.")
        except pymongo.errors.ConnectionError as e:
            print(f"Connection error: {e}")
            return

        db = client["LPGTrading_DB"]
        collection_name = "orders"
        self.collection = db[collection_name]

        self.selected_row = None
        # self.add_form_button.clicked.connect(self.onCreateOrderBtnClicked)
        self.tableWidget.itemSelectionChanged.connect(self.on_row_clicked)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(100)

        self.update_processing_count()

    def update_all(self):
        self.update_table()

    def update_processing_count(self):
        # Retrieve the current processing count from the database
        processing_count = self.collection.count_documents({"order_status": "Processing"})
        self.count_label.setText(f"Processing Count: {processing_count}")

    def get_order_table(self):
        return self.tableWidget

    def on_row_clicked(self):
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if selected_rows:
            row_index = selected_rows[0].row()
            print(f"Row {row_index} clicked")
            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_index, column)
                row_data.append(item.text() if item else "")

            # Assuming `order_id` is in the first column (adjust if needed)
            order_id = row_data[0]
            print(f"Querying for order_id: {order_id}")

            # Attempt to find the document using the correct field
            document = self.collection.find_one({'order_id': order_id})
            print(f'DOCUMENT {document}')
            if document:
                print(f"Found document: {document}")
                self.selected_row = row_index
                self._id = order_id

                # Set the labels in the UI (adjust label setting as necessary)
                self.customer_label.setText(document.get('customer_name', ''))
                self.order_label.setText(document.get('order_date', ''))
                self.product_label.setText(document.get('product_name', ''))
                self.cylinder_label.setText(document.get('cylinder_size', ''))
                self.quantity_label.setText(str(document.get('quantity', '')))
                self.price_label.setText(str(document.get('price', '')))
                self.amount_label.setText(str(document.get('total_amount', '')))
                self.ostatus_label.setText(document.get('order_status', ''))
                self.paymentS_label.setText(document.get('payment_status', ''))
                self.address_label.setText(document.get('delivery_address', ''))
                self.contact_info.setText(str(document.get('contact_info', '')))
                self.note_label.setText(document.get('order_note', ''))
                print(f'ORDER ID {order_id}')

                # Disconnect previous connections to avoid multiple triggers
                try:
                    self.edit_btn.clicked.disconnect()
                    self.delete_btn.clicked.disconnect()
                except TypeError:
                    pass
                # Connect the edit button click event, passing the correct `order_id`
                self.edit_btn.clicked.connect(lambda: self.on_open_form_clicked(order_id))
                self.delete_btn.clicked.connect(lambda: self.delete_order(order_id))
            else:
                print("Document not found for the given order_id.")
        else:
            self.selected_row = None
            print("No row is selected")

    def show_form_frame(self, order_id):
        # Create and display the QFrame as a popup
        self.form_frame = UpdateOrderForm(order_id)
        self.form_frame.show()

    def on_open_form_clicked(self, order_id):
        self.show_form_frame(order_id)

    def on_add_form_clicked(self, order_id):
        # self.show_add_frame(order_id)
        self.addorderform = AddOrderForm(order_id)
        self.addorderform.show()

    def delete_order(self, order_id):
        print(f'Selected Order ID: {order_id}')

        if not order_id:
            print('Order ID is empty')
            return

        # Confirm deletion
        reply = QMessageBox.question(
            self, "Delete Order", "Are you sure you want to delete this order?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_result = self.collection.delete_one({'order_id': order_id})

                if delete_result.deleted_count == 0:
                    QMessageBox.warning(self, "Delete Error", "Order could not be deleted. It may not exist.")
                    print("Order deletion failed or order not found in the database.")
                    return

                # Remove the row from the table widget
                self.tableWidget.removeRow(self.selected_row)
                self.selected_row = None

                # Refresh the table after deletion
                self.update_table()

                print("Order deleted successfully.")
            except Exception as e:
                print(f"Error during deletion: {e}")
                QMessageBox.critical(self, "Delete Error", "An error occurred while trying to delete the order.")

    def payment_status_filter(self):
        filter_dir = "app/resources/config/filters.json"

        with open(filter_dir, 'r') as f:
            data = json.load(f)

        self.paymentStatus.clear()
        for status in data['payment_status']:
            self.paymentStatus.addItem(list(status.values())[0])

    def order_status_filter(self):
        filter_dir = "app/resources/config/filters.json"

        with open(filter_dir, 'r') as f:
            data = json.load(f)

        self.orderStatus.clear()
        for status in data['order_status']:

            self.orderStatus.addItem(list(status.values())[0])

    def update_filters(self):
        self.payment_status_filter()
        self.order_status_filter()

    def update_table(self):
        table = self.tableWidget
        table.setRowCount(0)  # Clear the table

        header_dir = "app/resources/config/table/order_tableHeader.json"

        # Read header labels from the JSON file
        with open(header_dir, 'r') as f:
            header_labels = json.load(f)

        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        # Clean the header labels
        self.header_labels = [self.clean_header(header) for header in header_labels]

        filter_query = {}
        order_filter = self.orderStatus.currentText()
        paymentStatus_filter = self.paymentStatus.currentText()

        if order_filter != "Show All":
            filter_query['order_status'] = order_filter

        if paymentStatus_filter != "Show All":
            filter_query['payment_status'] = paymentStatus_filter

        data = list(self.collection.find(filter_query).sort("_id", -1))
        if not data:
            return  # Exit if the collection is empty

        # Populate table with data
        for row, item in enumerate(data):
            table.setRowCount(row + 1)
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)
                if value is not None:
                    table.setItem(row, column, QTableWidgetItem(str(value)))

    def clean_key(self, key):
        return re.sub(r'[^a-z0-9]', '', key.lower().replace(' ', '').replace('_', ''))

    def clean_header(self, header):
        return re.sub(r'[^a-z0-9]', '', header.lower().replace(' ', '').replace('_', ''))

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     Form = QWidget()
#     ui = OrdersPage(None, None) 
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec())