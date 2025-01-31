from pymongo import MongoClient
from src.utils.dir import ConfigPaths
from src.utils.Hashpassword import HashPassword
import json, pymongo

class createDefaultAdmin:
    def __init__(self):
        pass

        # self.dirs = ConfigPaths()

        # self.settings_dir = self.dirs.get_path('settings')
        # with open(self.settings_dir, 'r') as f:
        #     self.data = json.load(f)

        # self.client = MongoClient(self.data['db'][1]['db_url'])
        # self.db = self.client[self.get_db_name()]

        # if not self.isDatabaseExist():
        #     self.client[self.get_db_name()]

        # if not self.isCollectionExist():
        #     self.db.create_collection(self.get_collection_name())

        # # check if database and collection doesn't exist
        # if not self.isDatabaseExist() and not self.isCollectionExist():
        #     self.client[self.get_db_name()]
        #     self.db.create_collection(self.get_collection_name())

        # if not self.isAdminExist():
        #     self.create_default_admin()
        
    # def create_default_admin(self):
    #     default_username = self.data['default_admin'][0]['username']
    #     default_password = self.data['default_admin'][1]['password']

    #     data = {
    #         "username": default_username,
    #         "password": default_password,
    #         "role": "Admin",
    #         "job": ""
    #     }

    #     collection = self.db[self.get_collection_name()]
    #     collection.insert_one(data)

    # def isAdminExist(self):
    #     default_username = self.data['default_admin'][0]['username']
        
    #     collection_name = self.get_collection_name()
    #     collection = self.db[collection_name]
    #     if collection.find_one({"username": default_username}):
    #         return True
    #     else:
    #         return False

    # def isCollectionExist(self):
    #     collection_name = self.get_collection_name()

    #     # check if collection exist
    #     if collection_name in self.db.list_collection_names():
    #         return True
    #     else:
    #         return False

    # def isDatabaseExist(self):
    #     db_name = self.get_db_name()

    #     # check if database exist
    #     if db_name in self.client.list_database_names():
    #         return True
    #     else:
    #         return False
        
    # def get_collection_name(self):
    #     collection_name = self.data['db'][3]["default_account_collection_name"]
    #     return collection_name
        
    # def get_db_name(self):
    #     db_name = self.data['db'][0]['db_name']
    #     return db_name

    def connect_to_db(self, collection_name):
        connection_string = "mongodb://localhost:27017/"
        client = pymongo.MongoClient(connection_string)
        db = "LPGTrading_DB"
        return client[db][collection_name]
    
    # make data for default admin account
    def create_default_admin(self):
        """create default admin account"""
        password = 'admin123'
        hash = HashPassword(password)
        hashed_password = hash.hash_password()

        account_data = {
            'username': 'admin',
            'email': '',
            'password': hashed_password,
            'account_id': '',
            'user_type': 'Admin',
            'job': '',
            'status': '',
            'first_name': '',
            'last_name': '',
            'address': '',
            'last_login': '',
        }
    # check if account exists
        is_accounts_exist = list(self.connect_to_db('accounts').find({'username': 'admin'}))
        if is_accounts_exist:
            return
        else:
            self.connect_to_db('accounts').insert_one(account_data)
    # if not insert to collection
    
admin = createDefaultAdmin()
admin.create_default_admin()