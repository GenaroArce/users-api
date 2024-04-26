from flask import Flask, request, jsonify, g
from funcs import *
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'users.db'

def get_db():
    """Get the connection to the database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the connection to the database."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/add-user', methods=["POST"])
def add_user_route():
    """Add a user."""
    try:
        msg = read_json()

        email = request.args.get('email')
        name = request.args.get('name')
        lastname = request.args.get('lastname')
        age = request.args.get('age')

        if not email or not name or not lastname or not age:
            return jsonify({"error": msg["errors"]["missingFields"]}), 400

        cursor = get_db().cursor()
        add = add_user(get_db(), cursor, email, name, lastname, age)

        if add:
            return jsonify({"message": msg["messages"]["addUser"]}), 200
        else:
            return jsonify({"message": msg["errors"]["emailExist"]}), 200
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": msg["errors"]["error"]}), 500

@app.route('/search-user', methods=["GET"])
def search_user_route():
    """Search for a user by email."""
    try:
        msg = read_json()

        email = request.args.get('email')

        if not email:
            return jsonify({"error": msg["errors"]["missingFields"]}), 400
        
        cursor = get_db().cursor()
        search = search_user(get_db(), cursor, email)

        return jsonify({"message": f"{search}"})
    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": msg["errors"]["error"]}), 500

@app.route('/remove-user', methods=["DELETE"])
def remove_user_route():
    """Delete a user by email."""
    try:
        msg = read_json()
        email = request.args.get('email')

        if not email:
            return jsonify({"error": msg["errors"]["missingFields"]}), 400
        
        cursor = get_db().cursor()
        remove = remove_user(get_db(), cursor, email)
        return jsonify({"message": f"{msg["messages"]["removedUser"]} -> {remove}"})

    except Exception as e:
        print("Error: ", e)
        return jsonify({"error": msg["errors"]["error"]}), 500
    
if __name__ == "__main__":
    app.run(debug=True)
