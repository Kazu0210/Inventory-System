from PyQt6.QtWidgets import QApplication, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget

def create_summary_card(title, value, color):
    card = QFrame()
    card.setStyleSheet(f"background-color: {color}; border-radius: 10px; padding: 10px;")
    layout = QVBoxLayout()
    card.setLayout(layout)
    
    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
    layout.addWidget(title_label)
    
    value_label = QLabel(str(value))
    value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
    layout.addWidget(value_label)
    
    return card

def main():
    app = QApplication([])
    
    main_window = QWidget()
    main_window.setWindowTitle("Summary Cards")
    main_window.setGeometry(100, 100, 800, 600)
    
    main_layout = QHBoxLayout()
    main_window.setLayout(main_layout)
    
    total_orders_card = create_summary_card("Total Orders", 120, "#3498db")
    pending_orders_card = create_summary_card("Pending Orders", 35, "#f39c12")
    completed_orders_card = create_summary_card("Completed Orders", 80, "#2ecc71")
    canceled_orders_card = create_summary_card("Canceled Orders", 5, "#e74c3c")
    
    main_layout.addWidget(total_orders_card)
    main_layout.addWidget(pending_orders_card)
    main_layout.addWidget(completed_orders_card)
    main_layout.addWidget(canceled_orders_card)
    
    main_window.show()
    app.exec()

if __name__ == "__main__":
    main()