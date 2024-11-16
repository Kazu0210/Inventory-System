from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout

def create_simple_card(title, value):
    card = QFrame()
    card.setStyleSheet("border: 1px solid #ccc; border-radius: 10px; padding: 10px;")
    layout = QVBoxLayout(card)
    
    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
    layout.addWidget(title_label)
    
    value_label = QLabel(str(value))
    value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #3498db;")
    layout.addWidget(value_label)
    
    return card

# Example usage
if __name__ == "__main__":
    app = QApplication([])
    total_orders_card = create_simple_card("Total Orders", 120)
    pending_orders_card = create_simple_card("Pending Orders", 35)
    completed_orders_card = create_simple_card("Completed Orders", 80)
    total_orders_card.show()
    pending_orders_card.show()
    completed_orders_card.show()
    app.exec()