from PyQt6.QtWidgets import QMainWindow, QStackedLayout
from ui.employee.employee_MainWindow import Ui_MainWindow
from pages.employee.profile_page import ProfilePage
from pages.employee.order_page import OrdersPage
from utils.Activity_logs import Activity_Logs as activity_logs
import os, json

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.account_username = username
        
        if self.account_username:
            self.username.setText(self.account_username) # set logged in account's username
        else:
            self.username.setText("Unknown User") # set logged in account's username

        self.logs = activity_logs()

        # layout
        self.content_window_layout = QStackedLayout(self.content_widget)

        self.order_section = OrdersPage(username, self) # index 0
        self.content_window_layout.addWidget(self.order_section)

        self.profile_section = ProfilePage(username, self)
        self.content_window_layout.addWidget(self.profile_section) # index 1

        self.buttons = [
            self.inventory_btn,
            self.orders_btn,
            self.profile_btn,
            self.settings_btn,
            self.logout_btn
        ]

        self.orders_btn.clicked.connect(lambda: self.button_clicked(self.orders_btn, 0))
        self.profile_btn.clicked.connect(lambda: self.button_clicked(self.profile_btn, 1))
        self.logout_btn.clicked.connect(self.logout_btn_clicked)

    def logout_btn_clicked(self):
        print("Application is closed")
        try:
            temp_data_dir = "app/resources/data/temp_user_data.json"
            if os.path.exists(temp_data_dir):
                with open(temp_data_dir, 'r') as file:
                    data = json.load(file)
                key = list(data.keys())[0]
                _id = data[key]

                print(f'Key: {key}, _id: {_id}')
                self.logs.logout(self.account_username)
                self.account_username = None

                data = {"_id": str("")}
                with open(temp_data_dir, 'w') as file:
                    json.dump(data, file, indent=4)

                self.close()
            else:
                print("File not found")
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Invalid JSON in file")

    def get_current_index(self):
        return self.content_window_layout.currentIndex()
    
    def button_clicked(self, button, index):
        self.reset_button_styles()
        self.set_active_button_style(button)
        if index is not None:
            self.content_window_layout.setCurrentIndex(index)
            print(f'Current Index: {self.get_current_index()}')
            # self.current_index_update()
        else:
            print(f"{button.objectName()} button clicked.")

    def reset_button_styles(self):
        for button in self.buttons:
            button.setStyleSheet("""
            QPushButton {
                color: #9E9BB9;
                border: none;
                padding: 10px 0;
                    font: 10pt "Inter";
                text-align:left;
            }
            QPushButton:hover { 
                color: #0D044E;
                border: none;
                padding: 10px 0;
                    font: 10pt "Inter";
            }	
        """)
            
    def set_active_button_style(self, button):
        button.setStyleSheet("""
            QPushButton{
                color: #0D044E;
                border: none;
                padding: 10px 0;
                    font: 10pt "Inter";
            }          
        """)