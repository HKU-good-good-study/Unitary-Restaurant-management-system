from database import Database

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return self.password == password
    
    def save(self):
        db = Database()
        users_collection = db.database["users"]
        users_collection.insert_one({
            "username": self.username,
            "password": self.password
        })

    @classmethod
    def find_one(cls, username):
        db = Database()
        users_collection = db.database["users"]
        user_data = users_collection.find_one({"username": username})
        if user_data is None:
            return None
        return cls(user_data["username"], user_data["password"])