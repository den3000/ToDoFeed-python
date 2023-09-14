import uuid
import os
import json
from flask import Flask, request, abort
from flask_cors import CORS
import sqlite3
from flask import g

FILENAME = "/data/todo.json" if "AMVERA" in os.environ else "todo.json"
USERS = "/data/users.json" if "AMVERA" in os.environ else "users.json"
TODOS = "/data/todos.json" if "AMVERA" in os.environ else "todos.json"
DATABASE = "/data/my.db" if "AMVERA" in os.environ else "my.db"

def generate_uuid():
   return str(uuid.uuid4())

def get_users():
   try:
         with open(USERS, "r", encoding="utf-8") as f:
            return json.load(f)
   except FileNotFoundError:
         return []

def save_users(data):
   with open(USERS, "w", encoding="utf-8") as f:
       json.dump(data, f)

def get_todos():
   try:
         with open(TODOS, "r", encoding="utf-8") as f:
            return json.load(f)
   except FileNotFoundError:
         return []

def save_todos(data):
   with open(TODOS, "w", encoding="utf-8") as f:
       json.dump(data, f)

def get_data():
   try:
       with open(FILENAME, "r", encoding="utf-8") as f:
           return json.load(f)
   except FileNotFoundError:
       return []

def save_data(data):
   with open(FILENAME, "w", encoding="utf-8") as f:
       json.dump(data, f)

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def index():
   return "TODO App"

@app.route("/register", methods=["POST"])
def register():
   body = request.json
   if body is None:
      abort(400)

   password = body['password']
   firstName = body['firstName']
   lastName = body['lastName']
   about = body['about']
   id = generate_uuid()
   token = generate_uuid() + ':' + id

   user = {
       "id" : id,
       "token" : token,
       "password" : password,
       "firstName" : firstName,
       "lastName" : lastName,
       "about" : about,
   }

   users = get_users()
   users.append(user)
   save_users(users)

   del user["password"]
   
   return user

@app.route("/login", methods=["POST"])
def login():
   body = request.json
   if body is None:
      abort(400)

   password = body['password']

   users = get_users()

   index  = [index for (index, item) in enumerate(users) if item['password'] == password][0]
   user = users[index]

   del user['password']
   
   return user

@app.route("/get_all_users")
def get_all_users():
   print('get_all_users')
   token = request.args.get('token')
   print('token ' + token)
   
   userId = token.split(':')[1]

   users = get_users()
   indexs  = [index for (index, item) in enumerate(users) if item['userId'] == userId]
   if len(indexs) != 1:
       return []
   
   for user in users:
      del user['token']
      del user['password']

   return users

@app.route("/edit_profile", methods=["POST"])
def edit_profile():
   body = request.json
   if body is None:
      abort(400)

   token = body['token']
   firstName = body['firstName']
   lastName = body['lastName']
   about = body['about']

   userId = token.split(':')[1]

   users = get_users()

   index  = [index for (index, item) in enumerate(users) if item['id'] == userId][0]
   user = users[index]

   user['firstName'] = firstName
   user['lastName'] = lastName
   user['about'] = about

   users[index] = user
   save_users(users)

   del user['token']
   del user['password']
   
   return user

@app.route("/erase_all")
def erase_all():
   save_users([])
   save_todos([])

   return json.dumps({
      "result":"ok"
   })

@app.route("/add_todo", methods=["POST"])
def add_todo():
   body = request.json
   if body is None:
      abort(400)
   
   id = generate_uuid()
   userId = body['token'].split(':')[1]
   title = body['title']
   description = body['description']
   status = body['status']
   visibility = body['visibility']

   todo = {
       "id" : id,
       "userId" : userId,
       "title" : title,
       "description" : description,
       "status" : status,
       "visibility" : visibility,
   }

   todos = get_todos()
   todos.append(todo)
   save_todos(todos)
   
   return todo

@app.route("/get_my_todos", methods=["POST"])
def get_my_todos():
   body = request.json
   if body is None:
      abort(400)

   userId = body['token'].split(':')[1]

   todos = get_todos()

   myTodos  = [item for (index, item) in enumerate(todos) if item['userId'] == userId]
   
   return myTodos

@app.route("/get_my_and_public_todos", methods=["POST"])
def get_my_and_public_todos():
   body = request.json
   if body is None:
      abort(400)

   userId = body['token'].split(':')[1]

   todos = get_todos()

   myAndPubTodos  = [item for (index, item) in enumerate(todos) if (item['userId'] == userId or item['visibility'] == 'public')]
   
   return myAndPubTodos

@app.route("/edit_todo", methods=["POST"])
def edit_todo():
   body = request.json
   if body is None:
      abort(400)

   userId = body['token'].split(':')[1]
   id = body['id']
   title = body['title']
   description = body['description']
   status = body['status']
   visibility = body['visibility']

   todos = get_todos()

   index  = [index for (index, item) in enumerate(todos) if (item['userId'] == userId and item['id'] == id)][0]
   todo = todos[index]

   todo['title'] = title
   todo['description'] = description
   todo['status'] = status
   todo['visibility'] = visibility

   todos[index] = todo
   save_todos(todos)

   return todo

# ----------------------------------------------------------------------------

@app.route("/todo")
def get_all_todo():
   con = get_db()
   return get_data()

@app.route("/todo/<int:id>")
def get_single_todo(id):
   data = get_data()
   if id < 0 or id >= len(data):
       abort(404)
   return data[id]

@app.route("/todo", methods=["POST"])
def add_new_todo():
   new_todo = request.json
   if new_todo is None:
       abort(400)
   data = get_data()
   data.append(new_todo)
   save_data(data)
   return json.dumps({
      "result":"ok", 
      "uuid": generate_uuid()
   }), 201
   
@app.route("/todo/<int:id>", methods=["PUT"])
def update_todo(id):
   data = get_data()
   if id < 0 or id >= len(data):
       abort(404)
   updated_todo = request.json
   if updated_todo is None:
       abort(400)
   data[id] = updated_todo
   save_data(data)
   return json.dumps({
      "result":"ok", 
      "uuid": generate_uuid()
   })

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
   app.run(port=8080)