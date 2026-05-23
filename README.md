# Secure-Login-System
# Secure Login System using Flask

## Project Overview
This project is a secure login web application developed using Flask. It allows users to register, login, access a protected dashboard, and logout securely. The system uses bcrypt password hashing, input validation, SQL injection protection, and session management.

## Key Features
- User registration
- User login
- Password hashing using bcrypt
- SQLite database
- Input validation
- Protection from SQL injection using parameterized queries
- Session management
- Logout functionality
- Protected dashboard page

## Technologies Used
- Python
- Flask
- SQLite
- bcrypt
- HTML
- CSS

## Project Structure
```text
Secure Login System/
│
├── app.py
├── database.db
├── requirements.txt
│
├── templates/
│   ├── register.html
│   ├── login.html
│   └── dashboard.html
│
└── static/
    └── style.css

How It Works
1.User registers with username, email, and password.
2.Password is hashed using bcrypt before storing in the database.
3.User logs in using username and password.
4.The entered password is compared with the hashed password.
5.If login is successful, a session is created.
6.User is redirected to the dashboard.
7.Logout clears the session.
8.Security Features

--Password Hashing

Passwords are not stored directly. bcrypt converts the password into a secure hash.

--SQL Injection Protection

Parameterized queries are used instead of directly inserting user input into SQL queries.

--Session Management

Flask sessions are used to maintain login state.

--Input Validation

Username, email, and password are validated before registration.
