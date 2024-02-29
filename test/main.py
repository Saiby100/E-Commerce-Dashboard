import random
from dotenv import load_dotenv
import os
import pymongo
from utils.user_activity import UserActivity
from utils.user import User
from utils.order import Order
from utils.date import Date

load_dotenv()

client = pymongo.MongoClient(os.environ.get("LOWDEFY_SECRET_DATABASE_URL"))
db = client["e_commerce_lowdefy"]

cities = ["Cape Town", "Durban", "Pretoria", "East London", "Johannesburg", "Stellenbosch"]
order_type = ["sale", "service"]

users = ["Salahuddin", "Ellie", "John", "Amanda"]

order = Order(db)
activity = UserActivity(db)
user = User(db)

def add_random_complete_orders():
    for i in range(1, 28):
        r = random.randint(3, 7)
        for j in range(0, r):
            date = Date(2024, 2, i)
            order.add_order(
                users[random.randint(0, len(users) - 1)],
                None,
                date.get_date(),
                "Street Address",
                cities[random.randint(0, len(cities) - 1)],
                order_type[random.randint(0, 1)],
                date.get_earlier(random.randint(1, 10))
            )

def add_random_cancelled_orders():
    for i in range(1, 28):
        r = random.randint(3, 7)
        for j in range(0, r):
            date = Date(2024, 2, i)
            order.add_order(
                users[random.randint(0, len(users) - 1)],
                date.get_date(),
                None,
                "Street Address",
                cities[random.randint(0, len(cities) - 1)],
                order_type[random.randint(0, 1)],
                date.get_earlier(random.randint(1, 10))
            )
    
def add_random_activity():
    for i in range (1, 28):
        date = Date(2024, 2, i)
        r = round(random.uniform(1, 10), 2)
        activity.add_user_activity(r, date.get_date(), users[random.randint(0, len(users) - 1)])


if __name__ == "__main__":
    # add_random_activity()
    # activity.clear_collection()

    client.close()