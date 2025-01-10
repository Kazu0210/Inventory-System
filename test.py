import json
import pymongo
from datetime import datetime

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
# db = client['LPGTrading_DB']
# collection = db['accounts']

def connect_to_db(collection_name):
    connection_string = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(connection_string)
    db = "LPGTrading_DB"
    return client[db][collection_name]

# # Fetch all documents from the collection
# data = list(collection.find())

# # Convert ObjectId to string for JSON serialization
# for document in data:
#     document['_id'] = str(document['_id'])

# # Save data to a JSON file
# with open('collection_backup.json', 'w') as file:
#     json.dump(data, file, indent=4)

# print("Collection saved to collection_backup.json")

# total_doc = collection.count_documents({})
# print(f'total document: {total_doc}')

# def convert_datetime(obj):
#     """Custom function to convert datetime objects to string."""
#     if isinstance(obj, datetime):
#         return obj.isoformat()  # Convert datetime to ISO 8601 string
#     raise TypeError("Type not serializable")  # Raise error for unsupported types

# collection_names = [
#     'account_archive',
#     'accounts',
#     'cart',
#     'logs',
#     'order_archive',
#     'orders',
#     'price_history',
#     'prices',
#     'product_archive',
#     'sales'
# ]

# for collection in collection_names:
#     print(f'Collection: {collection}')
    
#     # Fetch all documents from the collection
#     data = list(connect_to_db(collection).find())

#     # Convert ObjectId to string for JSON serialization
#     for document in data:
#         document['_id'] = str(document['_id'])
        
#         # Check for datetime fields and convert them
#         for key, value in document.items():
#             if isinstance(value, datetime):
#                 document[key] = value.isoformat()

#     # Save data to a JSON file
#     file_name = f'{collection}_backup.json'
#     with open(file_name, 'w') as file:
#         json.dump(data, file, indent=4, default=convert_datetime)

#     print(f"Collection '{collection}' saved to {file_name}")

#     # total_doc = collection.count_documents({})
#     # print(f'total document: {total_doc}')

client = pymongo.MongoClient('mongodb://localhost:27017/')
# Access your database
db = client['LPGTrading_DB']  # Replace with your database name

# Get a list of all collection names
collection_names = db.list_collection_names()

# Print collection names
print(collection_names) 
print(type(collection_names))

for collection in collection_names:
    print(collection)

    if collection == "logs":
        collection_names.remove('logs')
        collection_names.append('hatdog')

print(collection_names)