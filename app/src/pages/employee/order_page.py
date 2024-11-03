from PyQt6.QtWidgets import *
import pymongo
from ui.employee.orderPage import Ui_Form as Ui_order_page
from ui.employee.update_order_form import Ui_Frame as Ui_update_form
# from order_update_page import OrderUpdatePage
import json
import re
from PyQt6 import uic

class FormFrame(QFrame, Ui_update_form):
    def __init__(self, order_id):
        super().__init__()
        self.setupUi(self)  # Sets up the UI from Ui_update_form

        # Set up the form with the provided order_id
        self.order_id = order_id
        self.quantity_box.valueChanged.connect(self.calculate_total_amount)
        self.price_input.textChanged.connect(self.calculate_total_amount)
        # Initialize the database connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
        self.db = self.client["LPGTrading_DB"]  # Replace with your database name
        self.collection = self.db["orders"]  # Replace with your collection name

        # Load data for the given order_id and populate the form
        self.load_data()

        # Connect the submit button
        # self.delete_btn.clicked.connect(self.delete_order)
        self.cancel_Btn.clicked.connect(self.close_form)
        self.save_Btn.clicked.connect(self.submit_form)

    def calculate_total_amount(self):
        try:
            quantity = self.quantity_box.value()
            price = float(self.price_input.text()) if self.price_input.text() else 0.0

            total_amount = quantity * price

            self.amount_input.setText(f"{total_amount:.2f}")
        except ValueError:
            self.amount_input.setText("0.00")
    def close_form(self):
        self.close()
    def delete_order(self, order_id):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this order?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Proceed with deletion
            result = self.collection.delete_one({"order_id": self.order_id})

            if result.deleted_count > 0:
                QMessageBox.information(self, "Deleted", "Order deleted successfully!")
                self.close()  # Close the form after deletion
            else:
                QMessageBox.warning(self, "Error", "Failed to delete the order.")


    def load_data(self):
        # Query the database to get the document with the given order_id
        order_data = self.collection.find_one({"order_id": self.order_id})
        
        if order_data:
            # Populate the form fields with data from the database
            self.name_input.setText(order_data.get("customer_name", ""))
            self.order_input.setText(order_data.get("order_date", ""))
            self.productname_input.setText(order_data.get("product_name", ""))
            self.cylindersize_box.setCurrentText(order_data.get("cylinder_size", ""))
            self.quantity_box.setValue(order_data.get("quantity", ""))
            self.price_input.setText(str(order_data.get("price", "")))
            self.amount_input.setText(str(order_data.get("total_amount", "")))
            self.status_box.setCurrentText(order_data.get("status", ""))
            self.address_input.setText(order_data.get("delivery_address",""))
            self.payment_box.setCurrentText(order_data.get("payment_status",""))
            self.info_input.setText(order_data.get("contact_info",""))
            self.note_input.setText(order_data.get("order_note",""))
        else:
                print("Order not found in database")    

            # Add other fields as needed
        # else:
        #     QMessageBox.warning(self, "Error", f"No data found for Order ID: {self.order_id}")

    def submit_form(self):
        try:
            # Retrieve the input data from form fields
            customer_name = self.name_input.text()
            order_date = self.order_input.text()
            product_name = self.productname_input.text()
            cylinder_size = self.cylindersize_box.currentText()
            quantity = self.quantity_box.value()
            price_text = self.price_input.text()
            amount_text = self.amount_input.text()
            status = self.status_box.currentText()
            delivery_address = self.address_input.text()
            payment_status = self.payment_box.currentText()
            contact_info = self.info_input.text()
            order_note = self.note_input.text()

            # Ensure price and total_amount can be converted to float
            price = float(price_text) if price_text else 0.0
            total_amount = float(amount_text) if amount_text else 0.0

            # Create the order data dictionary
            order_data = {
                "order_id": self.order_id,
                "customer_name": customer_name,
                "order_date": order_date,
                "product_name": product_name,
                "cylinder_size": cylinder_size,
                "quantity": quantity,
                "price": price,
                "total_amount": total_amount,
                "status": status,
                "delivery_address": delivery_address,
                "payment_status": payment_status,
                "contact_info": contact_info,
                "order_note": order_note
            }

            # Perform the database update (or insert if not found)
            result = self.collection.update_one(
                {"order_id": self.order_id},  # Find the document by order_id
                {"$set": order_data},  # Update with new data
                upsert=True  # Insert if no document found
            )

            # Show confirmation message
            if result.upserted_id:
                QMessageBox.information(self, "Form Submitted", "New order inserted successfully!")
                self.close()
            else:
                QMessageBox.information(self, "Form Submitted", "Order updated successfully!")
                self.load_data()
                self.close()
        
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for price and total amount.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred while saving the order: {e}")

class OrdersPage(QWidget, Ui_order_page):
    def __init__(self, username, dashboard_mainWindow=None):
        super().__init__()
        self.setupUi(self)
        self.dashboard_mainWindow = dashboard_mainWindow

        self.setWindowTitle("Main Window")
        self.open_form_button = QPushButton("Open Form")
        self.open_form_button.clicked.connect(lambda: self.on_open_form_clicked(order_id=None)) 

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
        self.order_btn.clicked.connect(self.onCreateOrderBtnClicked)
        self.tableWidget.itemSelectionChanged.connect(self.on_row_clicked)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.update_table()

    def get_order_table(self):
        return self.tableWidget

    def create_order(self):
        if self.dashboard_mainWindow:
            self.dashboard_mainWindow.content_window_layout.setCurrentIndex(3)

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
                self.ddate_label.setText(document.get('delivery_date', ''))
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

    def on_open_form_clicked(self, order_id):
        # Create and display the QFrame as a popup
        self.form_frame = FormFrame(order_id)
        self.form_frame.show()


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

                # Clear UI labels after deletion
                self.clear_labels()

                # Refresh the table after deletion
                self.update_table()

                print("Order deleted successfully.")
            except Exception as e:
                print(f"Error during deletion: {e}")
                QMessageBox.critical(self, "Delete Error", "An error occurred while trying to delete the order.")

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

        data = list(self.collection.find())
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

    def clear_labels(self):
        """ Clears all the labels in the UI after deleting an order. """
        self.customer_label.clear()
        self.order_label.clear()
        self.product_label.clear()
        self.cylinder_label.clear()
        self.quantity_label.clear()
        self.amount_label.clear()
        self.order_label_2.clear()
        self.address_label.clear()
        self.contact_info.clear()
        self.note_label.clear()

    def onCreateOrderBtnClicked(self):
        print("Create Order button CLICKED")
        if self.dashboard_mainWindow:
            self.dashboard_mainWindow.content_window_layout.setCurrentIndex(3)
        
        # Refresh the table after creating a new order
        self.update_table()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = OrdersPage(None, None)  # Pass 'None' if no username or dashboard is used
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
