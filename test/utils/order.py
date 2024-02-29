import random
from datetime import datetime, timedelta
from utils.user import User

class Order:
    def __init__(self, db) -> None:
        self.collection = db["Order"]
        self.user_collection = User(db)

    def add_order(
        self,
        username,
        date_cancelled,
        date_completed,
        address,
        city,
        order_type,
        date_ordered = datetime.now()
    ):
        user_id = self.user_collection.get_userid(username)
        if (user_id is not None):
            price = round(random.uniform(150, 2000), 2)
            order = {
                "date_ordered": date_ordered,
                "date_cancelled": date_cancelled,
                "date_completed": date_completed,
                "address": address,
                "city": city,
                "order_type": order_type,
                "order_price": price,
                "user_id": user_id
            }
            self.collection.insert_one(order)
            print(f"Order added for user {username}")
        else:
            print(f"User with username {username} not found.")
    
    def add_complete_order(self, username, address, city, order_type):
        date = datetime.now() - timedelta(seconds=600)
        order_date = datetime - timedelta(days=random.randint(0, 10))
        self.add_order(username, None, date, address, city, order_type, order_date)
    
    def add_incomplete_order(self, username, address, city, order_type):
        date = datetime.now() - timedelta(seconds=600)
        self.add_order(username, None, None, address, city, order_type, date)
    
    def add_cancelled_order(self, username, address, city, order_type, date_cancelled):
        date_ordered = date_cancelled - timedelta(days=random.randint(0, 10))
        self.add_order(username, date_cancelled, None, address, city, order_type, date_ordered)
    
    def add_many_complete_orders(self, username, address, city, days_before):
        order_types = ["sale", "service"]

        date_and_time = datetime.now()
        start_date_and_time = date_and_time - timedelta(days=days_before)
        start_date = datetime(
            start_date_and_time.year, 
            start_date_and_time.month, 
            start_date_and_time.day
        )

        for i in range(1, days_before+1): #Add orders for each day leading up to present
            order_type = order_types[random.randint(0, 1)]
            temp_date = start_date + timedelta(days=i)

            num_orders = random.randint(0, 10) #Add between 0 and 10 orders per day
            for j in range(0, num_orders):
                self.add_order(
                    username, 
                    None, 
                    temp_date, 
                    address, 
                    city,
                    order_type,
                    temp_date - timedelta(days=random.randint(0, 30))
                )

    def add_many_cancelled_orders(self, username, address, city, days_before):
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

            num_orders = random.randint(0, 10)
            for j in range(0, num_orders):
                self.add_order(
                    username, 
                    temp_date, 
                    None,
                    address, 
                    city,
                    order_type, 
                    temp_date - timedelta(days=random.randint(0, 30))
                )
    
    def clear_collection(self):
        self.collection.delete_many({})
        print("Deleted successfully")
        