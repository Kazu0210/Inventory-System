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


from pymongo import MongoClient

def get_top_10_best_selling_products(collection):
    """
    Returns the top 10 best-selling products based on the quantity sold.

    :param collection: MongoDB collection object
    :return: List of dictionaries containing product details and total quantity sold
    """
    pipeline = [
        # Unwind the products_sold array
        {"$unwind": "$products_sold"},
        
        # Group by product_id, product_name, and cylinder_size, summing the quantities sold
        {
            "$group": {
                "_id": {
                    "product_id": "$products_sold.product_id",
                    "product_name": "$products_sold.product_name",
                    "cylinder_size": "$products_sold.cylinder_size"
                },
                "total_quantity_sold": {"$sum": "$products_sold.quantity"},
                "total_value_sold": {"$sum": "$products_sold.total_amount"}
            }
        },
        
        # Sort by total_quantity_sold in descending order
        {"$sort": {"total_quantity_sold": -1}},
        
        # Limit to the top 10
        {"$limit": 10},
        
        # Format the result
        {
            "$project": {
                "_id": 0,
                "product_id": "$_id.product_id",
                "product_name": "$_id.product_name",
                "cylinder_size": "$_id.cylinder_size",
                "total_quantity_sold": 1,
                "total_value_sold": 1
            }
        }
    ]
    
    # Execute the aggregation pipeline
    top_10_products = list(collection.aggregate(pipeline))
    return top_10_products


# Example usage
client = MongoClient('mongodb://localhost:27017/')
db = client['LPGTrading_DB']
sales_collection = db['sales']
top_10 = get_top_10_best_selling_products(sales_collection)
print(top_10)

top_products = get_top_10_best_selling_products(sales_collection)
for product in top_products:
    print(f'Product: {product}')
    print(f'Prouct Name: {product.get("product_name", "N/A")}')