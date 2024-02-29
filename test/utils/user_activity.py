from datetime import datetime
from utils.user import User

class UserActivity:
    def __init__(self, db) -> None:
        self.collection = db["UserActivity"]
        self.user_collection = User(db)
    
    def _gen_query(self, username, date):
        query_date_start = datetime(date.year, date.month, date.day)
        query_date_end = datetime(date.year, date.month, date.day+1)

        user_id = self.user_collection.get_userid(username)

        query = {
            "date_active": {
                "$gte": query_date_start,
                "$lte": query_date_end
            },
            "user_id": user_id
        }
        
        return query
    
    def _get_activity(self, username, date):

        query = self._gen_query(username, date)
        return self.collection.find_one(query)
        
    def _activity_exists(self, username, date):
        return self._get_activity(username, date) is not None
    
    def _update_activity(self, hours, date, username):
        query = self._gen_query(username, date)
        current_hours = self._get_activity(username, date)["hours"]

        update = {
            "$set": {
                "hours": current_hours + hours
            }
        }
        self.collection.update_one(query, update)
        print("Activity updated")

    def add_user_activity(self, hours, date, username):
        user_id = self.user_collection.get_userid(username)

        if not self._activity_exists(username, date):
            if user_id is not None:
                self.collection.insert_one({
                    "hours": hours,
                    "date_active": date,
                    "user_id": user_id
                })
                print("New activity added")
            else:
                print("User Id not found")
        else: 
            self._update_activity(hours, date, username)
    
    def clear_collection(self):
        self.collection.delete_many({})
        print("Deleted successfully")
        