import re
import json
import pymongo
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

class Validator:
    def __init__(self):
        self.settings_dir = "resources/config/settings.json"
        with open(self.settings_dir, 'r') as f:
            setting = json.load(f)
        
        self.username_minLength = setting["create_account_validation"][0]['username_min_lenght']
        self.username_maxLength = setting["create_account_validation"][1]['username_max_lenght']
    
    # Username validation
    def validate_username(self, username):
        return (self.check_length(username, self.username_minLength, self.username_maxLength) and
                self.allowed_characters(username) and
                self.first_character_is_letter(username) and
                self.no_spaces(username) and
                self.check_username_uniqueness(username))
    
    # Email validation
    def validate_email(self, email):
        return self.valid_email_format(email)
    
    # Password validation
    def validate_password(self, password):
        return (self.check_length(password, 8, 32) and
                self.has_uppercase(password) and
                self.has_lowercase(password) and
                self.has_digit(password) and
                self.has_special_character(password))
    
    # Common length checker for username and password
    def check_length(self, field, min_len, max_len):
        return min_len <= len(field) <= max_len
    
    # Allowed characters (alphanumeric + underscore) for username
    def allowed_characters(self, username):
        return re.match(r'^[a-zA-Z0-9_]+$', username) is not None
    
    # Username must start with a letter
    def first_character_is_letter(self, username):
        if not username:
            return False
        return username[0].isalpha()
    
    # No spaces in username
    def no_spaces(self, username):
        return " " not in username
    
    # Placeholder for checking username uniqueness (e.g., database check)
    def check_username_uniqueness(self, username):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["LPGTrading_DB"]
        self.collection = self.db["accounts"]
        return self.collection.find_one({"username": username}) is None
    
    # Email format validation using regex
    def valid_email_format(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None
    
    # Password must contain at least one uppercase letter
    def has_uppercase(self, password):
        return any(char.isupper() for char in password)
    
    # Password must contain at least one lowercase letter
    def has_lowercase(self, password):
        return any(char.islower() for char in password)
    
    # Password must contain at least one digit
    def has_digit(self, password):
        return any(char.isdigit() for char in password)
    
    # Password must contain at least one special character
    def has_special_character(self, password):
        special_characters = "!@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~"
        return any(char in special_characters for char in password)
    
    def string_only_validator(self, obj):
        regex = QRegularExpression("[a-zA-Z ]+")
        validator = QRegularExpressionValidator(regex)
        obj.setValidator(validator)

    def validate_account_id(self, account_id):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["LPGTrading_DB"]
        self.collection = self.db["accounts"]
        return self.collection.find_one({"username": account_id}) is None

# Example usage:
validator = Validator()

# # Validate username
# print(validator.validate_username("User_123"))  # True

# # Validate email
# print(validator.validate_email("user@example.com"))  # True

# # Validate password
print(validator.validate_password("StrongPass1!"))  # True