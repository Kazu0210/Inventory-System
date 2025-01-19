import pymongo, datetime, random, string

class Logs:
    def __init__(self):
        pass

    def get_event(self, event:str):
        event_type = {
            'login_closed': f'Login Window Closed',
        }
        data = {
            'event_type': event,
            'description': event_type[event]
        }
        return data

    def record_log(self, **kwargs):
        """record the event to the collection"""
        log_id = self.generate_log_id()
        timestamp = self.get_time_stamp()
        user_id = kwargs.get('user_id', 'Null')
        username = kwargs.get('username', 'Null')
        event_type = kwargs.get('event_type', 'Null')
        description = kwargs.get('description', 'Null')
        try:
            document = {
                'log_id': log_id,
                'timestamp': timestamp,
                'user_id': user_id,
                'username': username,
                'event_type': event_type,
                'description': description
            }
            result = self.connect_to_db('logs').insert_one(document)

            if result:
                print(f'Logs Successfully Saved.')
            else:
                print('An Error Occured While Saving Logs')
        except Exception as e:
            print(f'Error: {e}')

    def generate_log_id():
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
    
logs = Logs()
logs.record_log()