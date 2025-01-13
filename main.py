from flask import Flask, render_template, url_for, request, redirect, make_response, send_from_directory, send_file
from typing import List
from message import Message
import json
import os
from user import User

#json.dump() json.load()

# if os.path.exists("C:\Users\ivand\OneDrive\Рабочий стол\Chat\data.json"):
#     json.load("C:\Users\ivand\OneDrive\Рабочий стол\Chat\data.json", )





app = Flask(__name__)

messages: List[Message] = []


if os.path.exists("messages.json"):
    messages = Message.from_json_to_list()

else:
    with open("messages.json", "w") as file:
        json.dump([], file)

if os.path.exists("users.json"):
    users: List[User] = User.from_json_to_list()
else:
    with open("users.json", "w") as file:
        json.dump([], file)


@app.route('/download/<file_name>')
def download(file_name):
    print(file_name)
    return send_from_directory('static', f'temp/{file_name}', as_attachment=True)


@app.route("/")
def home():
    if is_logged():
        return render_template("index.html", messages=messages, user= User.get_user_by_id(int(request.cookies.get("user_id")), users))
            
    return render_template("index.html", messages=messages, user=None)


@app.route("/profile")
def profile():
    if is_logged():
        return render_template("profile.html", user=User.get_user_by_id(int(request.cookies.get("user_id")), users))
    return redirect(url_for('home'))
    # return render_template("profile.html")
# d = {"a":3}
# d["b"]
# d.get("b", )

@app.route("/change_file", methods=['POST'])
def change_file():
    if is_logged():

        file_user = request.files["file_form"]
        file_user.save(f".\static\images\{file_user.filename}")

        user = User.get_user_by_id(int(request.cookies.get('user_id')), users)
        user.avatar_path = file_user.filename

        User.save_to_json(users)

    return redirect(url_for('profile'))

# {'name': "pupka", 'products':[{'name':'burger', 'price':300}, {'name': 'free', 'price':30}]}

@app.route("/change_name", methods=['POST'])
def change_name():
    if is_logged():
        user = User.get_user_by_id(int(request.cookies.get('user_id')), users)
        user.name = request.form.get('name')
        User.save_to_json(users)
        return redirect(url_for('profile'))
        
@app.route("/send", methods=['POST'])
def send():
    text = request.form["text"].strip()
    user_file = request.files["user_file"]

    if text or user_file:

        if is_logged():

            if user_file:
                
                user_file.save(rf".\static\temp\{user_file.filename}")

            user = User.get_user_by_id(int(request.cookies.get("user_id")), users)
            messages.append(Message(user.user_id, user.name, user.avatar_path, text, user_file.filename if user_file else None, Message.get_type_visual(user_file.filename)))

        else:
            messages.append(Message(-1, "Ghost", "icon.png", text))

        Message.save_to_json(messages)
    return redirect(url_for("home"))
   ###################

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register_submit", methods=['POST'])
def register_submit():
    name = request.form.get("name")
    password = request.form.get("password")


    if name and password:
        for user in users:
            if user.name == name and user.password == password:
                return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            
        users.append(User(name, password))

    
        with open("users.json", "w") as file:
            json.dump([user.__dict__ for user in users], file, indent=4)
                

    return redirect(url_for("home"))

@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/auth_submit", methods=['POST'])
def auth_submit():
    name = request.form.get("name")
    password = request.form.get("password")

    for user in users:
        if user.name == name and user.password == password:

            response = make_response(redirect(url_for("home")))
            response.set_cookie("user_id", str(user.user_id))
            return response
        
    return redirect(url_for("home"))

def is_logged():
    return request.cookies.get("user_id", False)

app.run(debug=True)