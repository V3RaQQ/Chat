from flask import Flask, render_template, url_for, request, redirect, make_response, send_from_directory, send_file
from typing import List
from message import Message
import json
import os
from user import User


app = Flask(__name__)

messages: List[Message] = []


# if os.path.exists("messages.json"):
#     messages = Message.from_json_to_list()

# else:
#     with open("messages.json", "w") as file:
#         json.dump([], file)

# if os.path.exists("users.json"):
#     users: List[User] = User.from_json_to_list()
# else:
#     with open("users.json", "w") as file:
#         json.dump([], file)

json_path = os.path.join(os.getcwd(), "json")
os.makedirs(os.path.join(os.getcwd(), "json"), exist_ok=True)

if os.path.exists(os.path.join(json_path, "messages.json")):
    messages = Message.from_json_to_list()
else:
    with open(os.path.join(json_path, "messages.json"), "w") as file:
        json.dump([], file)

if os.path.exists(os.path.join(json_path, "users.json")):
    users: List[User] = User.from_json_to_list()
else:
    with open(os.path.join(json_path, "users.json"), "w") as file:
        json.dump([], file)


@app.route('/download/<file_name>')
def download(file_name):
    print(file_name)
    return send_from_directory('static', f'temp/{file_name}', as_attachment=True)


@app.route("/")
def home():
    if is_logged():
        user_id = request.cookies.get("user_id")
        #check -> user_id in users
        if user_id and any(user.user_id == int(user_id) for user in users):
            user = User.get_user_by_id(int(user_id), users)
            return render_template("index.html", messages=messages, user=user)

        response = make_response(render_template("index.html", messages=messages, user=None))
        response.delete_cookie("user_id")
        return response 
        #to prevent bug with user_id.

    response = make_response(render_template("index.html", messages=messages, user=None))
    response.delete_cookie("user_id")
    return response

    #     return render_template("index.html", messages=messages, user= User.get_user_by_id(int(request.cookies.get("user_id")), users))
    
    # response = make_response(render_template("index.html", messages=messages, user=None))
    # if request.cookies.get("user_id"):
    #     response.delete_cookie("user_id") 
    # return response


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
            messages.append(Message(user.user_id, user.name, user.avatar_path, text, user_file.filename if user_file else None, 
                                    Message.get_type_visual(user_file.filename), get_file_weight(user_file.filename)))

        else:
            if user_file:
                user_file.save(rf".\static\temp\{user_file.filename}")

            messages.append(Message(-1, "Ghost", "profile_icon.png", text, user_file.filename if user_file else None, 
                                    Message.get_type_visual(user_file.filename), get_file_weight(user_file.filename)))

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

    
        # with open(url_for("json", "users.json"), "w") as file:
        #     json.dump([user.__dict__ for user in users], file, indent=4)
        with open(os.path.join(os.path.join(os.getcwd(), "json"), "users.json"), "w") as file:
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

def get_file_weight(filename):
    folder_path = os.path.join(os.getcwd(), "static", "temp")
    try:
        if not os.path.isdir(folder_path):
            print("os path dir error")
            return None

        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            print(os.path.getsize(file_path))
            return round(os.path.getsize(file_path) / (1024 * 1024), 3) #from bites to mb
        else:
            print("os path is file eorror")
            return None

    except Exception:
        print("exception erorr")
        return None 
    #add logs.

app.run(debug=True)