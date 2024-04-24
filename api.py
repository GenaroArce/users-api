from flask import Flask, request, jsonify, g
from funcs import *
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/add-user', methods=["POST"])
def adduser():
    try:
        data = request.get_json()
        email = data["email"]
        name = data["name"]
        lastname = data["lastname"]
        age = data["age"]

        if not email or not name or not lastname or not age:
            return jsonify({"error": "Missing required fields"}), 400

        cursor = get_db().cursor()
        add = add_user(get_db(), cursor, email, name, lastname, age)

        if add:
            return jsonify({"message": "User added successfully"}), 200
        else:
            return jsonify({"message": "A user with that email already exists."}), 200
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": "Bad request"}), 500

if __name__ == "__main__":
    app.run(debug=True)
