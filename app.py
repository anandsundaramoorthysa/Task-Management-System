import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")  # Secure for production

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database Initialization
def init_db():
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )""")
        conn.commit()

init_db()

# User Class
class User(UserMixin):
    def __init__(self, id, username=None):
        self.id = id
        self.username = username

    @staticmethod
    def get_user_by_id(user_id):
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
            result = cur.fetchone()
            if result:
                return User(result[0], result[1])
        return None  # Return None if user is not found

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)

@app.route("/")
def home():
    return redirect(url_for("login"))

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                return redirect(url_for("login")) 
            except sqlite3.IntegrityError:
                return render_template("register.html", error="Username already exists!")
                
    return render_template("register.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            return render_template("login.html", message="Please fill in both username and password!", alert_type="danger")
        
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
            user = cur.fetchone()

            if user and bcrypt.check_password_hash(user[1], password):
                login_user(User(user[0], username))
                return redirect(url_for("dashboard"))
            else:
                return render_template("login.html", message="Invalid credentials!", alert_type="danger")

    return render_template("login.html")

from flask import redirect, url_for, session, flash

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.pop('user_id', None)  
    logout_user() 
    flash("Logged out successfully.", "info")  
    
    return redirect(url_for("login"))

# Dashboard (View Tasks)
@app.route("/dashboard")
@login_required
def dashboard():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, title, status FROM tasks WHERE user_id = ?", (current_user.id,))
        tasks = cur.fetchall()

    return render_template("dashboard.html", tasks=tasks, username=current_user.username)

# Add Task
@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "POST":
        title = request.form["title"]
        status = request.form.get("status", "Pending")

        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO tasks (user_id, title, status) VALUES (?, ?, ?)",
                        (current_user.id, title, status))
            conn.commit()

        flash("Task added successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("create_task.html")

# Edit Task
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, current_user.id))
        task = cur.fetchone()

    if not task:
        flash("Task not found!", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        title = request.form["title"]
        status = request.form["status"]

        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE tasks SET title = ?, status = ? WHERE id = ? AND user_id = ?",
                        (title,  status, task_id, current_user.id))
            conn.commit()

        flash("Task updated successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_task.html", task=task)

# Delete Task
@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, current_user.id))
        conn.commit()

    flash("Task deleted successfully!", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

