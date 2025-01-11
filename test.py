import json
import pymongo
from datetime import datetime
from datetime import timedelta
from collections import defaultdict


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

# client = pymongo.MongoClient('mongodb://localhost:27017/')
# # Access your database
# db = client['LPGTrading_DB']  # Replace with your database name

# # Get a list of all collection names
# collection_names = db.list_collection_names()

# # Print collection names
# print(collection_names) 
# print(type(collection_names))

# for collection in collection_names:
#     print(collection)

#     if collection == "logs":
#         collection_names.remove('logs')
#         collection_names.append('hatdog')

# print(collection_names)
def get_products_sold_today():
    # Connect to the MongoDB instance
    # Get today's date
    today = datetime.utcnow()
    start_of_day = datetime(today.year, today.month, today.day)
    end_of_day = start_of_day + timedelta(days=1)

    # Query to find all sales from today
    sales_today = connect_to_db('sales').find({
        "sale_date": {"$gte": start_of_day, "$lt": end_of_day}
    })

    # Dictionary to store product data, combining same product ids
    products = defaultdict(lambda: {
        "product_name": "",
        "cylinder_size": "",
        "quantity": 0,
        "total_amount": 0
    })

    # Process each sale
    for sale in sales_today:
        for product in sale.get("products_sold", []):
            product_id = product["product_id"]
            products[product_id]["product_name"] = product["product_name"]
            products[product_id]["cylinder_size"] = product["cylinder_size"]
            products[product_id]["quantity"] += product["quantity"]
            products[product_id]["total_amount"] += product["total_amount"]

    # Return the processed product data as a list
    return [
        {
            "product_name": data["product_name"],
            "cylinder_size": data["cylinder_size"],
            "quantity": data["quantity"],
            "total_amount": data["total_amount"]
        }
        for data in products.values()
    ]

# Example usage
sold_products = get_products_sold_today()
for product in sold_products:
    print(product)