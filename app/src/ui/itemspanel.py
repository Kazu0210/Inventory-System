import datetime
from bson import ObjectId
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QComboBox, QLineEdit, QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QSpinBox, QLabel
from PyQt6.QtCore import Qt
from pymongo import MongoClient
import sys

# MongoDB connection setup
connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)
db = client["items"]
collection = db["productItems"]

# Initialize the application
app = QApplication(sys.argv)

# Load the main window UI
window = uic.loadUi("ui/items.ui")

# Function to show the add item form
def show_add_item_form():
    add_item_dialog = QDialog(window)  # Make sure the dialog is a child of the main window
    add_item_dialog.setWindowTitle("Add Item")

    # Load the add item UI elements
    add_item_layout = QVBoxLayout()
    add_item_dialog.setLayout(add_item_layout)
    
    item_name_input = QLineEdit()
    item_name_input.setPlaceholderText("Product Name")
    
    item_quantity_input = QSpinBox()
    item_quantity_input.setRange(0, 10000)  # Set appropriate range for your use case
    
    item_category_dropdown = QComboBox()
    item_category_dropdown.addItems(["5 KG", "9 KG", "14.2 KG", "15 KG"])  # Add your category options here

    item_details_input = QLineEdit()
    item_details_input.setPlaceholderText("Details")
    
    submit_button = QPushButton("Submit")
    cancel_button = QPushButton("Cancel")
    
    add_item_layout.addWidget(item_name_input)
    add_item_layout.addWidget(item_quantity_input)
    add_item_layout.addWidget(item_category_dropdown)
    add_item_layout.addWidget(item_details_input)
    add_item_layout.addWidget(submit_button)
    add_item_layout.addWidget(cancel_button)

    # Handle the submit button click
    def submit_item():
        item_name = item_name_input.text()
        item_quantity = item_quantity_input.value()  # Get value from QSpinBox
        item_category = item_category_dropdown.currentText()  # Retrieve the selected category
        item_details = item_details_input.text()

        # Insert the item into the database
        document = {
            "name": item_name,
            "quantity": item_quantity,
            "category": item_category,
            "timestamp": datetime.datetime.now().isoformat(),
            "details": item_details
        }
        collection.insert_one(document)

        # Close the dialog
        add_item_dialog.accept()

        # Refresh the item list
        list_item_view()

    # Handle the cancel button click
    def cancel_item():
        add_item_dialog.reject()  # This closes the dialog without saving

    # Connect buttons to their handlers
    submit_button.clicked.connect(submit_item)
    cancel_button.clicked.connect(cancel_item)

    # Show the dialog
    add_item_dialog.exec()

# Function to show the update item form
def show_update_item_form(item_id):
    # print(f"Item ID: {item_id}")
    update_item_dialog = QDialog(window)  # Make sure the dialog is a child of the main window
    update_item_dialog.setWindowTitle("Update Item")

    # Load the update item UI elements
    update_item_layout = QVBoxLayout()
    update_item_dialog.setLayout(update_item_layout)
    
    item_name_label = QLabel("Product Name:")
    item_name_value = QLineEdit()
    
    item_quantity_label = QLabel("Quantity:")
    item_quantity_value = QLineEdit()
    
    item_category_label = QLabel("Category:")
    item_category_value = QLineEdit()
    
    item_details_label = QLabel("Details:")
    item_details_value = QLineEdit()

    # Convert item_id to ObjectId
    item_object_id = ObjectId(item_id)

    # Retrieve the item from the database
    item = collection.find_one({"_id": item_object_id})

    if item:
        item_name_value.setText(item.get("name", ""))
        item_quantity_value.setText(str(item.get("quantity", "")))
        item_category_value.setText(item.get("category", ""))
        item_details_value.setText(item.get("details", ""))

    # Add widgets to the layout
    update_item_layout.addWidget(item_name_label)
    update_item_layout.addWidget(item_name_value)
    update_item_layout.addWidget(item_quantity_label)
    update_item_layout.addWidget(item_quantity_value)
    update_item_layout.addWidget(item_category_label)
    update_item_layout.addWidget(item_category_value)
    update_item_layout.addWidget(item_details_label)
    update_item_layout.addWidget(item_details_value)

    # Add buttons for update and cancel
    submit_button = QPushButton("Submit")
    cancel_button = QPushButton("Cancel")
    update_item_layout.addWidget(submit_button)
    update_item_layout.addWidget(cancel_button)
    
    # Handle the submit button click
    def submit_update():
        item_name = item_name_value.text()
        item_quantity = int(item_quantity_value.text()) if item_quantity_value.text().isdigit() else 0
        item_category = item_category_value.text()
        item_details = item_details_value.text()

        # Update the item in the database
        collection.update_one(
            {"_id": item_object_id},
            {"$set": {
                "name": item_name,
                "quantity": item_quantity,
                "category": item_category,
                "details": item_details
            }}
        )

        # Close the dialog
        update_item_dialog.accept()

        # Refresh the item list
        list_item_view()

    # Handle the cancel button click
    def cancel_update():
        update_item_dialog.reject()  # This closes the dialog without saving

    # Connect buttons to their handlers
    submit_button.clicked.connect(submit_update)
    cancel_button.clicked.connect(cancel_update)

    # Show the dialog
    update_item_dialog.exec()

# Function to list items in a table view
def list_item_view():
    items = collection.find()

    # Find the table widget and clear existing rows
    table_widget = window.findChild(QTableWidget, "tableWidget")
    table_widget.setRowCount(0)

    # Set table column headers
    table_widget.setColumnCount(6)
    table_widget.setHorizontalHeaderLabels(["Name", "Quantity", "Category", "Timestamp", "Details", "Actions"])

    # Populate the table with items from the database
    for item in items:
        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)

        name_item = QTableWidgetItem(item.get("name", ""))
        name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table_widget.setItem(row_position, 0, name_item)

        quantity_item = QTableWidgetItem(str(item.get("quantity", "")))
        quantity_item.setFlags(quantity_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table_widget.setItem(row_position, 1, quantity_item)

        category_item = QTableWidgetItem(item.get("category", ""))
        category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table_widget.setItem(row_position, 2, category_item)

        timestamp_item = QTableWidgetItem(item.get("timestamp", ""))
        timestamp_item.setFlags(timestamp_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table_widget.setItem(row_position, 3, timestamp_item)

        details_item = QTableWidgetItem(item.get("details", ""))
        details_item.setFlags(details_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table_widget.setItem(row_position, 4, details_item)

        # Create Update and Delete buttons
        update_button = QPushButton("Update")
        delete_button = QPushButton("Delete")

        # Set up the actions for the buttons
        def update_item(item_object_id=item["_id"]):
            show_update_item_form(str(item_object_id))

        def delete_item(item_object_id=item["_id"]):
            collection.delete_one({"_id": ObjectId(item_object_id)})
            list_item_view()

        update_button.clicked.connect(lambda _, id=item["_id"]: update_item(id))
        delete_button.clicked.connect(lambda _, id=item["_id"]: delete_item(id))

        # Add the buttons to the table
        action_layout = QHBoxLayout()
        action_widget = QWidget()
        action_layout.addWidget(update_button)
        action_layout.addWidget(delete_button)
        action_widget.setLayout(action_layout)
        table_widget.setCellWidget(row_position, 5, action_widget)

# Connect the add button to the function
add_button = window.findChild(QPushButton, "setItems")
if add_button:
    add_button.clicked.connect(show_add_item_form)
else:
    print("Error: 'setItems' button not found in the UI.")

# Show the main window
window.show()

# Display items when the application starts
list_item_view()

# Execute the application
sys.exit(app.exec())
