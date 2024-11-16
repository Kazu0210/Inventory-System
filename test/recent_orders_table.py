from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QApplication, QVBoxLayout, QWidget

def create_simple_orders_table():
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Order ID", "Customer", "Status"])
    table.setRowCount(3)  # Example with 3 rows of data
    
    # Example data
    recent_orders = [
        {"order_id": "ORD001", "customer_name": "John Doe", "status": "Pending"},
        {"order_id": "ORD002", "customer_name": "Jane Smith", "status": "Completed"},
        {"order_id": "ORD003", "customer_name": "Bob Johnson", "status": "Canceled"},
    ]
    
    for i, order in enumerate(recent_orders):
        table.setItem(i, 0, QTableWidgetItem(order["order_id"]))
        table.setItem(i, 1, QTableWidgetItem(order["customer_name"]))
        table.setItem(i, 2, QTableWidgetItem(order["status"]))
    
    return table

# Example usage
if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    recent_orders_table = create_simple_orders_table()
    layout.addWidget(recent_orders_table)
    window.setLayout(layout)
    window.show()
    app.exec()