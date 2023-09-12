import os
import json
from flask import Flask, request, abort
from flask_cors import CORS

FILENAME = "/data/todo.json" if "AMVERA" in os.environ else "todo.json"

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
   return "OK", 201
   
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
   return "OK"

if __name__ == "__main__":
   app.run(port=8080)