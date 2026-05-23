from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    message_type = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        # Validation checks
        if not username or not email or not password:
            message = "All fields are required"
            message_type = "error"
            return render_template("register.html", message=message, message_type=message_type)

        if len(username) < 3:
            message = "Username must be at least 3 characters long"
            message_type = "error"
            return render_template("register.html", message=message, message_type=message_type)

        if len(password) < 6:
            message = "Password must be at least 6 characters long"
            message_type = "error"
            return render_template("register.html", message=message, message_type=message_type)

        if "@" not in email or "." not in email:
            message = "Please enter a valid email address"
            message_type = "error"
            return render_template("register.html", message=message, message_type=message_type)

        # Check if username already exists
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                conn.close()
                message = "Username already exists. Please choose a different one."
                message_type = "error"
                return render_template("register.html", message=message, message_type=message_type)
            
            # Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                conn.close()
                message = "Email already registered. Please use a different email or login."
                message_type = "error"
                return render_template("register.html", message=message, message_type=message_type)
            
            # Insert new user
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
            conn.commit()
            conn.close()
            
            message = "Account created successfully! Please login."
            message_type = "success"
            return render_template("register.html", message=message, message_type=message_type)
        except Exception as e:
            message = f"An error occurred. Please try again."
            message_type = "error"

    return render_template("register.html", message=message, message_type=message_type)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    message_type = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            message = "Username and password are required"
            message_type = "error"
            return render_template("login.html", message=message, message_type=message_type)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode("utf-8"), user[3]):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            message = "Invalid username or password"
            message_type = "error"

    return render_template("login.html", message=message, message_type=message_type)

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)