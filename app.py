from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-deployment")

def database():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

database().close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if len(username) < 3 or len(password) < 8:
        return jsonify({"error": "Username needs 3 characters and password 8 characters"}), 400

    conn = database()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        session["username"] = username
        return jsonify({"message": "Account created"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    conn = database()
    user = conn.execute(
        "SELECT password FROM users WHERE username = ?",
        (data.get("username", "").strip(),)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user[0], data.get("password", "")):
        session["username"] = data.get("username").strip()
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid username or password"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route("/me")
def me():
    if "username" not in session:
        return jsonify({"logged_in": False}), 401
    return jsonify({"logged_in": True, "username": session["username"]})

@app.route("/generate", methods=["POST"])
def generate():
    if "username" not in session:
        return jsonify({"error": "Please login first"}), 401

    data = request.get_json() or {}
    style = data.get("style", "balanced")
    dpi = int(data.get("dpi", 400))

    if not 200 <= dpi <= 800:
        return jsonify({"error": "DPI must be 200-800"}), 400

    presets = {
        "balanced": [185, 175, 165, 155, 100],
        "rush": [195, 190, 180, 170, 100],
        "precision": [175, 165, 155, 145, 50]
    }

    settings = presets.get(style, presets["balanced"])
    variation = random.randint(-3, 3)

    return jsonify({
        "general": max(0, min(200, settings[0] + variation)),
        "red_dot": max(0, min(200, settings[1] + variation)),
        "scope_2x": max(0, min(200, settings[2] + variation)),
        "scope_4x": max(0, min(200, settings[3] + variation)),
        "fire_button": settings[4]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

