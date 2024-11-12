from PyQt6.QtWidgets import QFrame, QMessageBox
from PyQt6.QtCore import QDate

from ui.employee.update_order_form import Ui_Frame as Ui_update_form

import pymongo

class UpdateOrderForm(QFrame, Ui_update_form):
    def __init__(self, order_id):
        super().__init__()
        self.setupUi(self)  # Sets up the UI from Ui_update_form    

        # Initialize the database connection
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
        self.db = self.client["LPGTrading_DB"]  # Replace with your database name
        self.collection = self.db["orders"]  # Replace with your collection name

        # Initialize the form with the provided order_id
        self.order_id = order_id
        self.load_data()

        # Connect signals to slots
        self.quantity_box.valueChanged.connect(self.calculate_total_amount)
        self.price_input.textChanged.connect(self.calculate_total_amount)

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

    def delete_order(self):
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this order?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            result = self.collection.delete_one({"order_id": self.order_id})
            if result.deleted_count > 0:
                QMessageBox.information(self, "Deleted", "Order deleted successfully!")
                self.close()  # Close the form after deletion
            else:
                QMessageBox.warning(self, "Error", "Failed to delete the order.")

    def load_data(self):
        order_data = self.collection.find_one({"order_id": self.order_id})

        order_date = order_data.get("order_date", "")
        date = QDate.fromString(order_date, "yyyy-MM-dd")

        # self.data.setSelectedDate(date)
        # self.order_input.setText(date)

        if order_data:
            # Populate fields with data from the database
            self.name_input.setText(order_data.get("customer_name", ""))
            # self.order_input.selectedDate(order_data.get("order_date", ""))
            self.order_input.setText(order_data.get("order_date", ""))
            
            self.productname_input.setText(order_data.get("product_name", ""))
            self.cylindersize_box.setCurrentText(order_data.get("cylinder_size", ""))
            self.quantity_box.setValue(order_data.get("quantity", 1))
            self.price_input.setText(str(order_data.get("price", 0.0)))
            self.amount_input.setText(str(order_data.get("total_amoun`t", 0.0)))
            self.status_box.setCurrentText(order_data.get("order_status", ""))
            self.address_input.setText(order_data.get("delivery_address", ""))
            self.payment_box.setCurrentText(order_data.get("payment_status", ""))
            self.info_input.setText(order_data.get("contact_info", ""))
            self.note_input.setText(order_data.get("order_note", ""))
        else:
            QMessageBox.warning(self, "Error", f"No data found for Order ID: {self.order_id}")

    def submit_form(self):
        try:
            # Retrieve the input data from form fields
            customer_name = self.name_input.text().strip()
            order_date = self.order_input.selectedDate().toString("yyyy-MM-dd")
            product_name = self.productname_input.text().strip()
            cylinder_size = self.cylindersize_box.currentText()
            quantity = self.quantity_box.value()
            price_text = self.price_input.text().strip()
            amount_text = self.amount_input.text().strip()
            status = self.status_box.currentText()
            delivery_address = self.address_input.text().strip()
            payment_status = self.payment_box.currentText()
            contact_info = self.info_input.text().strip()
            order_note = self.note_input.text().strip()

            # Convert price and total amount to float, handling potential ValueErrors
            price = float(price_text) if price_text else 0.0
            total_amount = float(amount_text) if amount_text else 0.0

            # Prepare data for update
            order_data = {
                "order_id": self.order_id,
                "customer_name": customer_name,
                "order_date": order_date,
                "product_name": product_name,
                "cylinder_size": cylinder_size,
                "quantity": quantity,
                "price": price,
                "total_amount": total_amount,
                "order_status": status,
                "delivery_address": delivery_address,
                "payment_status": payment_status,
                "contact_info": contact_info,
                "order_note": order_note
            }

            # Update or insert the order data
            result = self.collection.update_one(
                {"order_id": self.order_id},
                {"$set": order_data},
                upsert=True
            )

            # Show confirmation message
            if result.upserted_id:
                QMessageBox.information(self, "Form Submitted", "New order inserted successfully!")
            else:
                QMessageBox.information(self, "Form Submitted", "Order updated successfully!")
            self.close()
        
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numbers for price and total amount.")
        except Exception as e:
            # Print or log the exception for debugging
            print(f"An error occurred while saving the order: {e}")
            QMessageBox.critical(self, "Database Error", f"An error occurred while saving the order: {e}")