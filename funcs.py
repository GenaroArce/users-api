import re
import json

def read_json():
    """Read the messages.json file and load the default messages."""
    with open('messages.json', 'r') as f:
        messages = json.load(f)
    return messages

def check_email(cursor, email):
    """Check if the email is in the database."""
    try:
        query_search = 'SELECT * FROM table_users WHERE email = ?'
        cursor.execute(query_search, (email,))
        check_email = cursor.fetchone()
        return check_email is not None
    except Exception as e:
        print("Error (CHECK_EMAIL): ", e)
        return False

def check_email_valid(email):
    """Check if the email is valid (gmail.com or hotmail.com)."""
    if not re.match(r"[^@]+@(gmail|hotmail)\.com$", email):
        return False
    else:
        return True

def create_table(client, cursor):
    """Create table 'table_users' if it does not exist."""
    try:
        query_table = '''
            CREATE TABLE IF NOT EXISTS table_users (
                "id_user" INTEGER PRIMARY KEY AUTOINCREMENT,
                "email" TEXT,
                "name" TEXT,
                "lastname" TEXT,
                "age" INTEGER
            );
        '''
        cursor.execute(query_table)
        client.commit()
        return True
    except Exception as e:
        print("Error (CREATE TABLE): ", e)
        return False

def add_user(client, cursor, email, name, lastname, age):
    """Add a user to the database."""
    try:
        create_table(client, cursor)
        checkemail = check_email(cursor, email)
        if not checkemail:
            query_adduser = '''
            INSERT INTO table_users (email, name, lastname, age) VALUES (?, ?, ?, ?)
            '''
            cursor.execute(query_adduser, (email, name, lastname, age))
            client.commit()
        else:
            return False

        return True
    except Exception as e:
        print("Error (ADD USER): ", e)

def search_user(client, cursor, email):
    """Search for a user in the database by email."""
    try:
        msg = read_json()
        valid_email = check_email_valid(email)
        if valid_email:
            cursor.execute('SELECT name, lastname, email, age FROM table_users WHERE email = ?', (email,))
            user_data = cursor.fetchone()
            if user_data:
                name, lastname, email, age = user_data
                return {
                    "name": name,
                    "lastname": lastname,
                    "email": email,
                    "age": age
                }
            else:
                return msg["errors"]["userExist"] 
        else:
            return msg["errors"]["validEmail"] 
    except Exception as e:
        print("Error (SEARCH USER): ", e)

def remove_user(client, cursor, email):
    """Delete a user from the database by email."""
    try:
        msg = read_json()
        valid_email = check_email_valid(email)
        if valid_email:
            email_in_db = check_email(cursor, email)
            if email_in_db:
                cursor.execute('DELETE FROM table_users WHERE email = ?', (email,)) 
                client.commit()
                return msg["messages"]["removedUser"] 
            else:
                return msg["errors"]["userExist"]
        else:
            return msg["errors"]["validEmail"] 
    except Exception as e:
        print("Error (REMOVE USER): ",e)