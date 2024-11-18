import pymongo

def generate_sales_id():
    new_sales_id = str(connect_to_db('sales').estimated_document_count() + 1).zfill(3)
    return f"SALES{new_sales_id}"

def connect_to_db(collectionN):
    connection_string = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(connection_string)
    db = "LPGTrading_DB"
    collection_name = collectionN
    return client[db][collection_name]

print(f'sales id: {generate_sales_id()}')