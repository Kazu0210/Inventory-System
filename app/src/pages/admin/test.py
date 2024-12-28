import pymongo


def connect_to_db(collection_name):
    connection_string = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(connection_string)
    db = "LPGTrading_DB"
    return client[db][collection_name]

data_count = connect_to_db('cart').count_documents({})
print(f'Data count: {data_count}')

# data = connect_to_db('cart').find({}, {"_id": 0})

# products = {}

# for index, item in enumerate(data):
#     product_name = item.get("product_name", "N/A")
#     quantity = item.get("quantity", "N/A")

#     print(f'Product name: {product_name}')
#     print(f'Quantity: {quantity}')

#     # Use index as a unique key to store each product's details
#     products[index] = {
#         'product_name': product_name,
#         'quantity': quantity
#     }

# print(f'Products dictionary: {products}')

# products_sold = connect_to_db('cart').find({}, {"_id": 0})
# for item in products_sold:
#     print(item)

# print(f'Products sold: {products_sold}')
# Fetch all orders from the database (excluding _id)
# orders = connect_to_db('orders').find({}, {"_id": 0})

# # Initialize total quantity
# total_quantity = 0

# # Iterate over each order and calculate the total quantity
# for order in orders:
#     total_quantity += sum(product.get("quantity", 0) for product in order.get("products", []))

# print(f'Total quantity: {total_quantity}')


# pipeline = [
#     {
#         "$project": {
#             "sale_id": 1,  # Include the sale_id for reference
#             "products_count": {"$size": "$products_sold"}  # Count the items in the products_sold array
#         }
#     }
# ]

# # Run the aggregation
# result = list(connect_to_db('sales').aggregate(pipeline))

# # Print results
# for doc in result:
#     print(f"Sale ID: {doc['sale_id']}, Products Count: {doc['products_count']}")


            
pipeline = [
    {
        "$group": {  # Group all documents
            "_id": None,  # No grouping key; process all documents together
            "total_amount": {"$sum": "$total_amount"}  # Sum up the `quantity` field
        }
    }
]
result = list(connect_to_db('cart').aggregate(pipeline))
if result:
    total_quantity = result[0]["total_amount"]
    print(f"Total Quantity: {total_quantity}")
else:
    print("No data found.")