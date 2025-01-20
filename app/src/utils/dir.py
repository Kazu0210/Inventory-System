import os

class ConfigPaths:
    def __init__(self):
        # Set the base directory dynamically
        self.base_dir = os.path.abspath(os.getcwd())
        print(f"Base Directory: {self.base_dir}")

        # Define directory mappings
        self.directories = {
            "accounts_header": ["resources", "config", "table", "accounts_tableHeader.json"],
            "activity_logs_header": ["resources", "config", "table", "activity_logs_tableHeader.json"],
            "cart_header": ["resources", "config", "table", "cart_tableHeader.json"],
            "item_header": ["resources", "config", "table", "items_tableHeader.json"],
            "order_header": ["resources", "config", "table", "order_tableHeader.json"],
            "price_history_header": ["resources", "config", "table", "priceHistory_tableHeader.json"],
            "price_header": ["resources", "config", "table", "prices_tableHeader.json"],
            "product_header": ["resources", "config", "table", "product_tableHeader.json"],
            "sales_header": ["resources", "config", "table", "sales_tableHeader.json"],
            "sales_today_header": ["resources", "config", "table", "sales_today_tableHeader.json"],
            "view_products_header": ["resources", "config", "table", "view_products_tableHeader.json"],
            "product_selection_header": ["resources", "config", "table", "product_selection_tableHeader.json"],
            "settings": ["resources", "config", "settings.json"],
            "filters_box": ["resources", "config", "filters_box.json"],
            "filters": ["resources", "config", "filters.json"],
            "logs": ["resources", "data", "logs.json"],
            "job_title": ["resources", "data", "job_titles.json"],
            "user_icon": ["resources", "icons", "black-theme", "user.png"],
            "system_icon": ["resources", "icons", "system-icon.png"],
            "dashboard_icon": ["resources", "icons", "black-theme", "dashboard.png"],
            "price_icon": ["resources", "icons", "black-theme", "price-tag.png"],
            "inventory_icon": ["resources", "icons", "black-theme", "inventory.png"],
            "orders_icon": ["resources", "icons", "black-theme", "booking.png"],
            "file_icon": ["resources", "icons", "black-theme", "file.png"],
            "sales_icon": ["resources", "icons", "black-theme", "sales.png"],
            "restore_icon": ["resources", "icons", "black-theme", "restore.png"],
            "settings_icon": ["resources", "icons", "black-theme", "settings.png"],
            "archive_icon": ["resources", "icons", "black-theme", "archive.png"],
            "logout_icon": ["resources", "icons", "black-theme", "logout.png"],
            "close_icon": ["resources", "icons", "black-theme", "close.png"],
            "search_icon": ["resources", "icons", "black-theme", "search.png"]
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