import os

class ConfigPaths:
    def __init__(self):
        # Set the base directory dynamically
        self.base_dir = os.path.abspath(os.getcwd())
        print(f"Base Directory: {self.base_dir}")

        # Define directory mappings
        self.directories = {
            "accounts_header": ["../", "app", "resources", "config", "table", "accounts_tableHeader.json"],
            "activity_logs_header": ["../", "app", "resources", "config", "table", "activity_logs_tableHeader.json"],
            "cart_header": ["../", "app", "resources", "config", "table", "cart_tableHeader.json"],
            "item_header": ["../", "app", "resources", "config", "table", "items_tableHeader.json"],
            "order_header": ["../", "app", "resources", "config", "table", "order_tableHeader.json"],
            "price_history_header": ["../", "app", "resources", "config", "table", "priceHistory_tableHeader.json"],
            "price_header": ["../", "app", "resources", "config", "table", "prices_tableHeader.json"],
            "product_header": ["../", "app", "resources", "config", "table", "product_tableHeader.json"],
            "sales_header": ["../", "app", "resources", "config", "table", "sales_tableHeader.json"],
            "sales_today_header": ["../", "app", "resources", "config", "table", "sales_today_tableHeader.json"],
            "view_products_header": ["../", "app", "resources", "config", "table", "view_products_tableHeader.json"],
            "product_selection_header": ["../", "app", "resources", "config", "table", "product_selection_tableHeader.json"],
            "settings": ["../", "app", "resources", "config", "settings.json"],
            "filters_box": ["../", "app", "resources", "config", "filters_box.json"],
            "filters": ["../", "app", "resources", "config", "filters.json"],
            "logs": ["../", "app", "resources", "data", "logs.json"],
            "job_title": ["../", "app", "resources", "data", "job_titles.json"],
            
            "user_icon": ["../", "app", "resources", "icons", "black-theme", "user.png"],
            "system_icon": ["../", "app", "resources", "icons", "system-icon.png"],
            "dashboard_icon": ["../", "app", "resources", "icons", "black-theme", "dashboard.png"],
            "price_icon": ["../", "app", "resources", "icons", "black-theme", "price.png"],
            "inventory_icon": ["../", "app", "resources", "icons", "black-theme", "inventory.png"],
            "orders_icon": ["../", "app", "resources", "icons", "black-theme", "booking.png"],
            "file_icon": ["../", "app", "resources", "icons", "black-theme", "file.png"],
            "sales_icon": ["../", "app", "resources", "icons", "black-theme", "sales.png"],
            "restore_icon": ["../", "app", "resources", "icons", "black-theme", "restore.png"],
            "settings_icon": ["../", "app", "resources", "icons", "black-theme", "settings.png"],
            "archive_icon": ["../", "app", "resources", "icons", "black-theme", "archive.png"],
            "logout_icon": ["../", "app", "resources", "icons", "black-theme", "logout.png"],
            "close_icon": ["../", "app", "resources", "icons", "black-theme", "close.png"],
            "search_icon": ["../", "app", "resources", "icons", "black-theme", "search.png"]
        }

    def get_path(self, key):
        """
        Dynamically retrieve the path for a given key.
        :param key: Name of the directory key in self.directories
        :return: Absolute path as a string
        """
        if key in self.directories:
            return os.path.join(self.base_dir, *self.directories[key])
        else:
            raise ValueError(f"Invalid path key: {key}")