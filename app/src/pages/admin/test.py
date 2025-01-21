from datetime import datetime
import pymongo

# today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(today)

def connect_to_db(collection_name):
    connection_string = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(connection_string)
    db = "LPGTrading_DB"
    return client[db][collection_name]

today_date = datetime.now().strftime('%Y-%m-%d')
filter = {
    "sale_date": {
        "$regex": f"^{today_date}"
    }
}

today_sales = list(connect_to_db('sales').find(filter))

total_profit = 0
for sale in today_sales:
    for product in sale.get('products_sold', []):
        print(f'Product: {product}')
        # Calculate profit per product
        selling_price = product.get('price', 0)
        supplier_price = product.get('supplier_price', 0)
        quantity_sold = product.get('quantity', 0)
        

        print(f"Selling price: {selling_price}")
        profit = (selling_price - supplier_price) * quantity_sold
        total_profit += profit

        print(f'total profit: {total_profit}')