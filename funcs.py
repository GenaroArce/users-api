import re

def check_email(cursor, email):
    try:
        query_search = 'SELECT * FROM table_users WHERE email = ?'
        cursor.execute(query_search, (email,))
        check_email = cursor.fetchone()
        return check_email is not None
    except Exception as e:
        print("Error (CHECK_EMAIL): ", e)
        return False
    
def check_email_valid(email):
    if not re.match(r"[^@]+@(gmail|hotmail)\.com$", email):
        return False
    else:
        return True
    
def create_table(client, cursor):
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