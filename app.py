import uuid
import os
import json
from flask import Flask, request, abort
from flask_cors import CORS
import sqlite3
from flask import g

FILENAME = "/data/todo.json" if "AMVERA" in os.environ else "todo.json"
DATABASE = "/data/my.db" if "AMVERA" in os.environ else "my.db"

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

def generate_uuid():
    str(uuid.uuid4())

if __name__ == "__main__":
   app.run(port=8080)