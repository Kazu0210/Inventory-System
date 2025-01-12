import datetime, json
from bson.objectid import ObjectId

from src.utils.DB_checker import db_checker

class Activity_Logs:
    def __init__(self):
        self.db_name = "LPGTrading_DB"
        self.collection_name = "logs"
        self.checker = db_checker("mongodb://localhost:27017/", self.db_name)
        self.connect_to_db()

    def connect_to_db(self):
        self.checker.connect_to_client()
        self.checker.check_db_exist()
        self.checker.connect_to_db()

    def last_login(self, username, last_login_time):
        collection_name = "accounts"
        filter = {"username": username}
        try:
            document = self.checker.db[collection_name].find_one(filter) # get document
            
            if document and "last_login" in document:
                # when "login_key" exist on the data
                self.checker.db[collection_name].update_one(filter, {"$set": {"last_login": last_login_time}})
            elif document and "last_login" not in document:
                # add "last_login" key when it doesn't exist on the data
                self.checker.db[collection_name].update_one(filter, {"$set": {"last_login": last_login_time}})
            else:
                print("Document not found")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def record(self, username, status, event, reason, timestamp, item_entity, category, details, last_login):
        collection_name = "accounts"
        filter = {"username": username}
        document = self.checker.db[collection_name].find_one(filter)

        if document:
            job = document.get("job")
        else:
            job = ""

        document = {
            'Date/Time': timestamp,
            'User': username,
            'Activity Type': event,
            'Job': job,
            'Item/Entity': item_entity,
            'Category': category,
            'Details': details,
            'status': status
        }
        self.checker.insert_document(self.collection_name, document)

    def log_event(self, username, event_type, status, **kwargs):
        deleted_account_username = kwargs.get("deleted_account_username")
        # details = kwargs.get("details")
        category = kwargs.get("category")
        item_entity = kwargs.get("item_entity")
        new_account_username = kwargs.get("new_account_username")
        time_format = kwargs.get("time_format")
        reason = kwargs.get("reason")
        last_login = kwargs.get("last_login")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        event_messages = {
            "Login attempt success": f"Login attempt successful: {username}",
            "Login attempt failed": f"Login attempt failed: {username}",
            "Logout": f"Logout successful: {username}",
            "Exit Application": f"Quit Application: {username}",
            "Create account": f"Account {new_account_username} has been created by {username}",
            "Delete account": f"Account {deleted_account_username} has been deleted by {username}",
            "Edit account": f"Account {item_entity}'s information has been edited by {username}",
            "Time Format Changed": f"Time format changed to {time_format} by {username}",
            
            # INVENTORY
            "New Item Category Added": f"User {username} added a new product category"
            # Add more event types and messages as needed
        }

        # Read logs categories from json file
        logs_dir = "D:/Inventory-System/app/resources/data/logs.json"
        with open(logs_dir, 'r') as f:
            category_data = json.load(f)

        category_key = category

        category = next((category[category_key] for category in category_data["categories"] if category_key in category), None)

        print(event_messages[event_type])
        self.record(username, status, event_type, reason, timestamp, item_entity, category, event_messages[event_type], last_login)

    def login_attempt_success(self, username):
        last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_event(username, "Login attempt success", "Success", category="Login Activity")
        self.last_login(username, last_login)


    def login_attempt_failed(self, username):
        self.log_event(username, "Login attempt failed", "Failed", category="Failed Login Attempt")

    def logout(self, username):
        self.log_event(username, "Logout", "Success", category="Logout Activity")
    
    def quit(self, _id):
        print(_id)

        # collection name of accounts
        collection_name = "accounts"

        object_id = ObjectId(_id)
        filter = {"_id": object_id}
        document = self.checker.db[collection_name].find_one(filter)

        if document:
            username = document.get("username")
            _id = str(document.get("_id"))
            print(f"Found document: id {_id}, username: {username}")

            self.log_event(username, "Exit Application", "Success", category="User Exit")
            # print(f"role: {document.get("job")}")

    def create_account(self, username, new_account_username):
        self.log_event(username, "Create account", "Success", category="Create Account", new_account_username=new_account_username, item_entity=new_account_username)

    def delete_account(self, username, deleted_account_username):
        self.log_event(username, "Delete account", "Success", deleted_account_username=deleted_account_username, category="Delete Account", item_entity=deleted_account_username)

    def edit_account(self, username, edited_account_username):
        self.log_event(username, "Edit account", "Success", category="Edit Account", item_entity=edited_account_username)

    def added_item_category(self, account_username, new_category_name):
        self.log_event(account_username, "New Item Category Added", "Success", "", "", "Item", new_category_name, "")
        # NOT DONE

    def check_time_format_changed(self, account_username, time_format):
        self.log_event(account_username, "Time Format Changed", "Success", "")
        # NOT DONE