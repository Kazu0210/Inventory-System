from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]
sales_collection = db["sales"]

# Aggregation pipeline to calculate total sales per product
pipeline = [
    {"$group": {"_id": "$product_id", "total_quantity": {"$sum": "$quantity_sold"}}},
    {"$sort": {"total_quantity": -1}},  # Sort in descending order
    {"$limit": 10}  # Limit to top 10 products
]

top_products = list(sales_collection.aggregate(pipeline))

# Print results
for product in top_products:
    print(f"Product ID: {product['_id']}, Total Sold: {product['total_quantity']}")
