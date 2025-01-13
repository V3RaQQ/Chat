import json
import os

json_path = os.path.join(os.getcwd(), "json")
users_file = os.path.join(json_path, "users.json")
os.makedirs(json_path, exist_ok=True)

class User:
    user_id = 0
    def __init__(self, name, password, avatar_path = None) -> None:
        self.name = name
        self.avatar_path = avatar_path or "profile_icon.png"
        self.password = password
        self.user_id = User.user_id
        User.user_id += 1


    def get_json(self):
        return self.__dict__

    @staticmethod
    def save_to_json(users):
        with open(users_file, "w") as file:
            json.dump([user.get_json() for user in users], file, indent=4)

    @staticmethod
    def from_json_to_list():
        users = []
        if os.path.exists(users_file):
            with open(users_file, "r") as file:
                for user in json.load(file):
                    user_name = user["name"]
                    password = user["password"]
                    avatar_path = user.get("avatar_path", "profile_icon.png")
                    user_id = int(user["user_id"])

                    user = User(user_name, password, avatar_path)
                    user.user_id = user_id
                    users.append(user)
        return users
    
    @staticmethod
    def get_user_by_id(user_id, users):
        for user in users:
            if user.user_id == user_id:
                return user
        return None