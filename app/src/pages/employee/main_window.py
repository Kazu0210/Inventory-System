from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from src.ui.employee.main_window import Ui_MainWindow
from src.pages.admin.activity_logs import Activity_Logs
from src.pages.admin.accountsPage import AccountsPage
from src.pages.admin.dashboard_page import Dashboard
from src.pages.admin.itemsPage import ItemsPage
from src.pages.admin.settings_page import settingsPage
from src.pages.admin.order_page import OrderPage
from src.pages.admin.archive_page import ArchivePage
from src.pages.admin.sales_report_page import SalesReportPage
from src.pages.admin.prices_page import PricesPage
from src.pages.admin.profile_page import ProfilePage
from src.custom_widgets.message_box import CustomMessageBox
from src.utils.Activity_logs import Activity_Logs as activity_logs
from src.utils.Graphics import AddGraphics
from src.utils.Logs import Logs
from src.utils.dir import ConfigPaths

import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username):
        super(MainWindow, self).__init__()  # Initialize the main window
        self.setupUi(self)  # Set up the user interface

        # Store logged-in account's username
        self.account_username = username

        self.dir = ConfigPaths()  # Initialize configuration paths
        self.add_graphics()

        # Initialize activity logs
        self.logs = activity_logs()

        # Load pages and connect buttons
        self.load_pages(username)
        self.load_btn_connections()

        # Additional UI and setup methods
        self.get_current_index()
        self.set_current_page_name()
        self.set_username_label()

    def load_pages(self, username):
        """load pages for the dashboard"""
        self.content_window_layout = QStackedLayout(self.content_widget)

        dashboard_section = Dashboard(username, self) # index 0
        self.content_window_layout.addWidget(dashboard_section)

        order_section = OrderPage(self) # index 1
        self.content_window_layout.addWidget(order_section)

        self.profile_page = ProfilePage(username, self) # index 2
        self.content_window_layout.addWidget(self.profile_page)

    def load_btn_connections(self):
        """load connection of buttons"""
        self.buttons = [
            self.dashboard_pushButton,
            self.logout_pushButton,
            self.orders_pushButton,
        ]

        self.parent_widgets = [
            self.frame_4,
            self.frame_7,
        ]
        self.dashboard_pushButton.clicked.connect(lambda: self.button_clicked(self.dashboard_logo, self.frame_4, self.dashboard_pushButton, 0))
        self.orders_pushButton.clicked.connect(lambda: self.button_clicked(self.orders_logo, self.frame_7, self.orders_pushButton, 1))
        self.profile_pushButton.clicked.connect(lambda: self.profile_btn_clicked())
        self.logout_pushButton.clicked.connect(self.logout_btn_clicked)

    def profile_btn_clicked(self):
        """handle click event for profile button"""
        self.content_window_layout.setCurrentIndex(2)
        print(f'Current index when profile button is clicked: {self.get_current_index()}')
        self.set_current_page_name()

    def set_username_label(self):
        """set label to current account's username"""
        try:
            if self.account_username:
                self.username_label.setText(self.account_username) # set username in the dashboard
            else:
                self.username_label.setText("Unknown User") # set username in the dashboard
        except Exception as e:
            print(e)
            
    def set_current_page_name(self):
        """Set label to current page"""
        current_index = self.get_current_index()
        match current_index:
            case 0:
                self.current_page_label.setText("DASHBOARD")
            case 1:
                self.current_page_label.setText("ORDERS")
            case 2:
                self.current_page_label.setText("PROFILE")

    def set_profile_icon(self):
        """Add icon to profile button"""
        self.profile_pushButton.setIcon(QIcon(self.dir.get_path('user_icon')))
        self.profile_pushButton.setIconSize(QSize(17, 17))

    def add_graphics(self):
        """Add graphics to widgets (shadows, icons, others effects etc.)"""
        
        self.set_btn_icons()

        self.set_system_logo()

        self.set_profile_icon()

        graphics = AddGraphics()
        graphics.shadow_effect(self.frame, blur=10, x=-4, y=4, alpha=50)
        graphics.shadow_effect(self.profile_pushButton, blur=4, x=0, y=0, alpha=50)

    def set_system_logo(self):
        logo = QPixmap(self.dir.get_path('system_icon'))
        min_height = 150
        max_height = 180
        current_height = self.logo.height()
        height_to_use = max(min_height, min(max_height, current_height))
        scaled_logo = logo.scaledToHeight(height_to_use, Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(scaled_logo)
        self.logo.setScaledContents(True)

    def logout_btn_clicked(self):
        try:
            confirmation = CustomMessageBox.show_message('question', 'Logout', 'Are you sure you want to logout')
            if confirmation == 1:
                logs = Logs()
                logs.record_log(usersname=self.account_username, event='user_logout_success')
                self.close()
        except Exception as e:
            print(f'An error occured: {e}')

    def get_current_index(self):
        return self.content_window_layout.currentIndex()

    def button_clicked(self, icon_widget, parent_widget, button, index):
        self.reset_button_styles()
        self.reset_parent_widget()
        self.reset_icon()
        self.set_active_icon(icon_widget)
        self.set_active_button_style(button)
        self.set_active_frame_style(parent_widget)
        if index is not None:
            self.content_window_layout.setCurrentIndex(index)
            self.set_current_page_name()
        else:
            print(f"{button.objectName()} button clicked.")

    def reset_button_styles(self):
        for button in self.buttons:
            button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
            QPushButton:hover { 
                background-color: #A8D5BA;
                color: #000;
            }	
        """)
    
    def reset_parent_widget(self):
        for widget in self.parent_widgets:
            widget.setStyleSheet("""
            QFrame{
                background-color: transparent;
            }
            QFrame:hover{
                background-color: #A8D5BA;
            }
            """)

    def reset_icon(self):
        self.set_btn_icons()

    def set_active_icon(self, icon_widget):
        file_name = icon_widget.file_name
        print(f'Pakening file name: {file_name}')
        base_dir = os.path.abspath(os.getcwd())
        file_path = f"{base_dir}/../app/resources/icons/{file_name}"
        icon = QPixmap(file_path)
        icon_widget.file_name = os.path.basename(file_path)
        icon_widget.setPixmap(icon)
        icon_widget.setScaledContents(True)

    def set_active_frame_style(self, parent_widget):
        parent_widget.setStyleSheet("""
            QFrame{
                color: #fff;
                background-color: #228B22;
            }
        """)
            
    def set_active_button_style(self, button):
        button.setStyleSheet("""
            QPushButton{
                color: #fff;
                background-color: #228B22;
            }
        """)
        
    def set_btn_icons(self):
        """Set icons for the buttons"""
        dashboard_icon = QPixmap(self.dir.get_path('dashboard_icon'))
        self.dashboard_logo.file_name = os.path.basename(self.dir.get_path('dashboard_icon'))
        self.dashboard_logo.setPixmap(dashboard_icon)
        self.dashboard_logo.setScaledContents(True)

        orders_icon = QPixmap(self.dir.get_path('orders_icon'))
        self.orders_logo.file_name = os.path.basename(self.dir.get_path('orders_icon'))
        self.orders_logo.setPixmap(orders_icon)
        self.orders_logo.setScaledContents(True)
        
        logout_icon = QPixmap(self.dir.get_path('logout_icon'))
        self.logout_logo.file_name = os.path.basename(self.dir.get_path('logout_icon'))
        self.logout_logo.setPixmap(logout_icon)
        self.logout_logo.setScaledContents(True)