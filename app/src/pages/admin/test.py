    # def get_today_sales(self):
    #     """Get data for today's sale (current sales today)"""
    #     # Define the start of the day (midnight) for today
    #     today_start = datetime.combine(datetime.now().date(), datetime.min.time())

    #     pipeline = [
    #         {
    #             "$addFields": {
    #                 "sale_date": {
    #                     "$dateFromString": {
    #                         "dateString": "$sale_date",  # Assuming `sale_date` is stored as a string
    #                         "format": "%Y-%m-%d %H:%M:%S"  # Adjust format as per your database
    #                     }
    #                 }
    #             }
    #         },
    #         {
    #             "$match": {
    #                 "sale_date": {"$gte": today_start}
    #             }
    #         },
    #         {
    #             "$group": {
    #                 "_id": None,
    #                 "total_sales": {"$sum": "$total_value"}
    #             }
    #         }
    #     ]

    #     # Run the pipeline and convert the result to a list for easier handling
    #     result = list(self.connect_to_db("sales").aggregate(pipeline))
        
    #     if result:  # If result is not empty
    #         total_sales = result[0].get("total_sales", 0)
    #         return total_sales
    #     else:
    #         return 0  # Default to 0 if no sales found
        


    #         def get_products_sold_today(self):
    #     # Connect to the MongoDB instance
    #     # Get today's date
    #     today = datetime.now()
    #     start_of_day = datetime(today.year, today.month, today.day)
    #     end_of_day = start_of_day + timedelta(days=1)

    #     # Aggregation pipeline to ensure `sale_date` is converted to a date object
    #     pipeline = [
    #         {
    #             "$addFields": {
    #                 "sale_date": {
    #                     "$dateFromString": {
    #                         "dateString": "$sale_date",  # Assumes `sale_date` is stored as a string
    #                         "format": "%Y-%m-%d %H:%M:%S"  # Adjust format as per your database
    #                     }
    #                 }
    #             }
    #         },
    #         {
    #             "$match": {
    #                 "sale_date": {"$gte": start_of_day, "$lt": end_of_day}
    #             }
    #         }
    #     ]

    #     # Query to find all sales from today using the aggregation pipeline
    #     sales_today = list(self.connect_to_db('sales').aggregate(pipeline))

    #     # Dictionary to store product data, combining same product IDs
    #     products = defaultdict(lambda: {
    #         "product_name": "",
    #         "cylinder_size": "",
    #         "quantity": 0,
    #         "total_amount": 0
    #     })

    #     # Variable to track total sales amount
    #     total_sales_amount = 0

    #     # Process each sale
    #     for sale in sales_today:
    #         for product in sale.get("products_sold", []):
    #             product_id = product["product_id"]
    #             products[product_id]["product_name"] = product.get("product_name", "")
    #             products[product_id]["cylinder_size"] = product.get("cylinder_size", "")
    #             products[product_id]["quantity"] += product.get("quantity", 0)
    #             products[product_id]["total_amount"] += product.get("total_amount", 0)
                
    #             # Add the product's total amount to the overall total sales amount
    #             total_sales_amount += product.get("total_amount", 0)

    #     # Sort products by cylinder size (extract numeric value for sorting)
    #     def extract_size(cylinder_size):
    #         try:
    #             # Extract numeric part (e.g., '11' from '11kg')
    #             return int(''.join(filter(str.isdigit, cylinder_size)))
    #         except ValueError:
    #             # Default to a very high number if parsing fails (to sort unknown sizes last)
    #             return float('inf')

    #     sorted_products = sorted(products.values(), key=lambda x: extract_size(x["cylinder_size"]))

    #     # Return the processed product data as a list along with the total sales amount
    #     return {
    #         "products": [
    #             {
    #                 "brand": data["product_name"],
    #                 "size": data["cylinder_size"],
    #                 "quantity": data["quantity"],
    #                 "price": data["total_amount"]
    #             }
    #             for data in sorted_products
    #         ],
    #         "total_sales_amount": total_sales_amount
    #     }
# from datetime import datetime

# # Current date and time
# current_datetime = datetime.now()
# print(current_datetime)

dir = r"C:\Users\dmfls\Downloads\InventoryBackup_2025-01-22\sales_backup.json"
collection_name = [
    'account_archive',
    'accounts',
    'logs',
    'order_archive',
    'orders',
    'price_history',
    'product_archive',
    'products',
    'sales',
]
for name in collection_name:
    if name in dir:
        print('meron', f'collection name: {name}')
    else:
        print('wala')