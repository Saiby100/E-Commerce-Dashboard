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
        "date_created": datetime.utcnow()
    }
    user_collection.insert_one(user)

    print(f"User {username} added successfully.")

def add_user_activity(username: str, hours: float):
    user_id = get_user_id(username)
    if (user_id):
        user_activity_collection.insert_one({
            "hours": hours,
            "user_id": user_id,
            "date_created": datetime.utcnow()
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
):
    user_id = get_user_id(username)

    if (user_id):
        order_price = random.uniform(150, 2000)
        order = {
            "date_ordered": datetime.utcnow(),
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
    add_order(username, False, datetime.utcnow(), address, order_type)

def add_order_incomplete(username, address, order_type):
    add_order(username, False, None, address, order_type)

def add_order_cancelled(username, address, order_type):
    add_order(username, True, None, address, order_type)

client.close()