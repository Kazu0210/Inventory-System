def loadAccounts(self):
        table = self.tableWidget
        table.setRowCount(0)  # Clear the table
        table.verticalHeader().hide()

        # Load table headers from JSON
        header_dir = "app/resources/config/table/accounts_tableHeader.json"
        with open(header_dir, 'r') as f:
            header_labels = json.load(f)
        table.setColumnCount(len(header_labels))
        table.setHorizontalHeaderLabels(header_labels)

        for column in range(table.columnCount()):
            table.setColumnWidth(column, 200)

        # Clean headers for use as dictionary keys
        self.header_labels = [self.clean_key(header) for header in header_labels]

        # Load and parse settings
        settings_dir = "app/resources/config/settings.json"
        with open(settings_dir, 'r') as f:
            settings = json.load(f)
        self.current_time_format = settings['time_date'][0]['time_format']

        # Get data from MongoDB with error handling
        try:
            data = list(self.db["account_archive"].find().sort("_id", -1))
        except pymongo.errors.PyMongoError as e:
            print(f"Error accessing MongoDB: {e}")
            return

        if not data:
            return  # Exit if the collection is empty
        
        # Populate table with data
        for row, item in enumerate(data):
            table.setRowCount(row + 1)  # Add a new row for each item
            for column, header in enumerate(self.header_labels):
                original_keys = [k for k in item.keys() if self.clean_key(k) == header]
                original_key = original_keys[0] if original_keys else None
                value = item.get(original_key)
                if value is not None:
                    # Format datetime if necessary
                    if header == 'lastlogin' and value:
                        date_time = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                        value = date_time.strftime(
                            "%Y-%m-%d %I:%M:%S %p" if self.current_time_format == "12hr" else "%Y-%m-%d %H:%M:%S"
                        )
                    table_item = QTableWidgetItem(str(value))
                    table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if row % 2 == 0:
                        table_item.setBackground(QBrush(QColor("#F6F6F6")))
                    table.setItem(row, column, table_item)