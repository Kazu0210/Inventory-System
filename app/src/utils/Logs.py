import pymongo, datetime, random, string

class Logs:
    def __init__(self):
        pass

    def get_event(self, event, **kwargs):
        username = kwargs.get('username', '')
        order_id = kwargs.get('order_id', '')
        product_name = kwargs.get('product_name', '')
        product_id = kwargs.get('product_id', '')
        account_id = kwargs.get('account_id', '')
        event_types = {
            'login_closed': 'Login Window Closed',
            'login_failed': 'Login Attempt Failed',
            'default_admin_login_success': 'Default Admin Successfully Logged In',
            'default_admin_login_failed': 'Default Admin Logged In Failed',
            'account_inactive': 'Account is currently inactive',
            'account_pending': 'Account is currently pending',
            'account_blocked': 'Account is currently blocked',
            'user_login_success': 'User Successfully Logged In',
            'user_logout_success': 'User Successfully Logged Out',
            'password_change_success': f"Password Successfully Changed{f' for account: {username}' if username else ''}",
            'password_change_failed': f"Password Changed Failed{f' for account: {username}' if username else ''}",

            'order_placed': 'Order Successfully Placed',
            'payment_status_updated': f"Payment Status Updated{f' for order: {order_id}' if order_id else ''}",
            'order_status_updated': f"Order Status Updated{f' for order: {order_id}' if order_id else ''}",

            'product_added': f"Product Successfully Added{f' for product: {product_name}' if product_name else ''}",
            'product_updated': f"Product Successfully Updated{f' for product: {product_id}' if product_id else ''}",
            'product_archived': f"Product Successfully Archived{f' for product: {product_id}' if product_id else ''}",

            'inventory_report': 'Inventory Report Successfully Generated',
            'sales_report': 'Sales Report Successfully Generated',
            'entire_system_backup': 'Entire System Backup Successfully Completed',

            'archived_account_restored': f"Archived Account Successfully Restored{f' for account: {account_id}' if account_id else ''}",
            'archived_product_restored': f"Archived Product Successfully Restored{f' for account: {product_id}' if product_id else ''}",
            
            'account_archived': f"Account Successfully Archived{f' for account: {account_id}' if account_id else ''}"
        }
        description = event_types.get(event, 'Unknown Event')
        return {
            'event': event,
            'description': description
        }

    def record_log(self, **kwargs):
        """Record the event to the collection. (user_id, username, event)"""
        log_id = self.generate_log_id()
        timestamp = self.get_time_stamp()
        user_id = kwargs.get('user_id', 'Null')
        username = kwargs.get('username', 'Null')
        event = kwargs.get('event', 'Null')
        order_id = kwargs.get('order_id')
        product_name = kwargs.get('product_name')
        product_id = kwargs.get('product_id')
        account_id = kwargs.get('account_id')

        # Get event details
        event_details = self.get_event(event, 
                                       username=username, 
                                       order_id=order_id,
                                       product_name=product_name,
                                       product_id=product_id,
                                       account_id=account_id
                                       )
        
        created_at = datetime.datetime.now()

        try:
            document = {
                'log_id': log_id,
                'timestamp': timestamp,
                'user_id': user_id,
                'username': username,
                'event_type': event_details['event'],
                'description': event_details['description'],
                'created_at': created_at
            }
            result = self.connect_to_db('logs').insert_one(document)

            if result.inserted_id:
                print('Logs Successfully Saved.')
            else:
                print('An Error Occurred While Saving Logs')
        except Exception as e:
            print(f'Error: {e}')

    def generate_log_id(self):
        # Get the current time in a short format (e.g., 20250119_153012)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        return f"{timestamp}_{random_string}"

    def get_time_stamp(self):
        """get current time stamp"""
        return datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]