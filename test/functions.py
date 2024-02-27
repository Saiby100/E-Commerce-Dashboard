import random
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pymongo

load_dotenv()

client = pymongo.MongoClient(os.environ.get("LOWDEFY_SECRET_DATABASE_URL"))
db = client["e_commerce_lowdefy"]

user_collection = db["User"]
user_activity_collection = db["UserActivity"]
order_collection = db["Order"]
product_collection = db["Product"]
ordered_product_collection = db["OrderedProduct"]

def get_user_id(username: str):
    user = user_collection.find_one({"name": username})
    if user:
        return user["_id"]
    return None

def add_user(username):
    user = {
        "name": username,
        "date_created": datetime.now()
    }
    user_collection.insert_one(user)

    print(f"User {username} added successfully.")

def add_user_activity(username: str, hours: float):
    user_id = get_user_id(username)
    if (user_id):
        user_activity_collection.insert_one({
            "hours": hours,
            "user_id": user_id,
            "date_created": datetime.now()
        })
        print(f"Activity added for {username}.")
    else:
        print("User not found")
    
def add_order(
    username: str, 
    order_cancelled: bool, 
    date_completed: datetime,
    address: str, 
    order_type: str, 
    date_ordered: datetime = datetime.now()
):
    user_id = get_user_id(username)

    if (user_id):
        order_price = round(random.uniform(150, 2000), 2)
        order = {
            "date_ordered": date_ordered,
            "order_cancelled": order_cancelled,
            "date_completed": date_completed,
            "address": address,
            "order_type": order_type,
            "order_price": order_price,
            "user_id": user_id
        }
        order_collection.insert_one(order)
        print(f"Order added for user {username}")
    else:
        print(f"User with username {username} not found.")

def add_order_complete(username, address, order_type):
    add_order(username, False, datetime.now(), address, order_type)

def add_order_incomplete(username, address, order_type):
    add_order(username, False, None, address, order_type)

def add_order_cancelled(username, address, order_type):
    add_order(username, True, None, address, order_type)

def add_many_complete_orders(username, address, days_before):
    date_and_time = datetime.now()
    start_date_and_time = date_and_time - timedelta(days=days_before)
    order_types = ["sale", "service"]

    start_date = datetime(
        start_date_and_time.year, 
        start_date_and_time.month, 
        start_date_and_time.day)

    for i in range(1, days_before+1):
        order_type = order_types[random.randint(0, 1)]
        temp_date = start_date + timedelta(days=i)
        add_order(username, False, temp_date, address, order_type)
    
def clear_orders():
    order_collection.delete_many({})
    print("Deleted successfully")

if __name__ == "__main__":

    client.close()