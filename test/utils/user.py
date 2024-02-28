from datetime import datetime

class User:
    def __init__(self, db) -> None:
        self.collection = db["User"]

    def _get_user(self, username) -> dict:
        return self.collection.find_one({"name": username})
    
    def _user_exists(self, username) -> bool:
        self._get_user(username) is not None

    def add_user(self, username: str) -> bool:
        if not self._user_exists(username):
            self.collection.insert_one({
                "name": username,
                "date_created": datetime.now()
            })
            return True
        return False
    
    def add_many_users(self, users: list):
        self.collection.insertMany(users)
    
    def get_userid(self, username):
        user = self._get_user(username)
        if user:
            return user["_id"]
        return None