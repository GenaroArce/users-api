### API - Users Management

This is a simple API created with Flask for managing users.

#### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/GenaroArce/users-api.git
```

2. **Install dependencies:**

```bash
pip install Flask
```


#### Usage

Start the Flask server by running the following command in the terminal:

```bash
python api.py
```

#### Endpoints
- **Search User**
- Endpoint: `/search-user`
- Method: GET
- Description: Search for a user by email.
- Example:
```bash
curl -X GET http://127.0.0.1:5000/search-user?email="test@example.com"
```

- **Add User**
- Endpoint: `/add-user`
- Method: POST
- Description: Add a new user.

- Parameters:
- email: User's email address (required)
- name: User's first name (required)
- lastname: User's last name (required)
- age: User's age (required)

- Example:
```bash
curl -X POST "http://127.0.0.1:5000/add-user?email=test@gmail.com&name=test&lastname=testing&age=20"
```

- **Remove User**
- Endpoint: `/remove-user`
- Method: DELETE
- Description: Remove a user by email.

- Parameters:
- email: User's email address (required)

- Example:
```bash
curl -X DELETE "http://127.0.0.1:5000/remove-user?email=test@gmail.com"
```

### Need Help or Want to Propose an Idea?

If you need help understanding the code or want to propose an idea, don't hesitate to contact me.

#### Contact

- Email: genaroarcee@gmail.com
