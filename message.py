import json
from typing import List
import os

json_path = os.path.join(os.getcwd(), "json")
os.makedirs(json_path, exist_ok=True) 
messages_file = os.path.join(json_path, "messages.json")

class Message:
    id_counter = 0
    def __init__(self, user_id, member_name, avatar_path, text, file_path=None, type_visual=None, file_weight=None) -> None:
        
        self.id_message = Message.id_counter
        Message.id_counter += 1

        self.user_id = user_id
        self.text = text
        self.member_name = member_name
        self.avatar_path = avatar_path
        self.file_path = file_path
        self.type_visual = type_visual
        self.file_weight = file_weight

    def get_json(self):
        return self.__dict__
    
    @staticmethod
    def save_to_json(messages):
        with open(messages_file, "w") as file:
            json.dump( [message.get_json() for message in messages], file, indent=4)

    @staticmethod
    def from_json_to_list():
        with open(messages_file, "r") as file:
            messages = []
            for message in json.load(file):

                msg = Message(message["user_id"], message["member_name"], message["avatar_path"],
                               message["text"], message["file_path"], message["type_visual"], message["file_weight"])
                msg.id_message = message["id_message"]

                messages.append(msg)

        return messages
    
    # @staticmethod
    # def get_type_visual(file_path):
    #     files = {
    #         "docx": "word_icon.png",
    #         "txt": "text_icon.png",
    #         "mp4": "video_icon.png",
    #         "mov": "video_icon.png",
    #         "gif": "video_icon.png",
    #         "avi": "video_icon.png"
    #     }

    #     return files[file_path.split(".")[-1]] if file_path.split(".")[-1] in files else None
##########################

    @staticmethod
    def get_type_visual(file_path):
        print(f"file_path: {file_path}")
        if not file_path:
            return None

        files = {
            "docx": "word_icon.png",
            "txt": "text_icon.png",
            "mp4": "video_icon.png",
            "mov": "video_icon.png",
            "gif": "video_icon.png",
            "avi": "video_icon.png",
        }

        images = {"jpg", "jpeg", "png", "tiff", "webp", "svg", "heic", "jfif"}


        file_type = file_path.split(".")[-1].lower() if file_path else "None"
        print(f"file_type: {file_type}")

        if file_type in images:
            return None
        return files.get(file_type, "default_file_icon.png")

# return None if file_path.split(".")[-1].lower() in images else files.get(file_path.split(".")[-1].lower(), "default_file_icon.png")


# msg = Message("Abigail", "Hello")

# msg2 = Message("John", "Hello")
# msg3 = Message("John", "Hello")

# messages = [msg, msg2, msg3]

