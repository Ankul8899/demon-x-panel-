
from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "change-this-secret-before-deployment"
)

DEFAULTS = {
    "general": 190,
    "red_dot": 180,
    "scope_2x": 170,
    "scope_4x": 160,
    "sniper": 100,
    "free_look": 120,
    "fire_button": 50,
    "dpi": 450
}

def db():
    con = sqlite3.connect("users.db", timeout=30)
    con.execute("PRAGMA busy_timeout=30000")
    return con

def setup():
    con = db()
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            username TEXT,
            setting TEXT,
            value INTEGER,
            PRIMARY KEY(username, setting)
        )
    """)
    con.commit()
    con.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if len(username) < 3 or len(password) < 8:
        return jsonify(error="Username min 3 and password min 8 characters."), 400

    con = db()
    try:
        con.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (username, generate_password_hash(password))
        )
        con.commit()
        return jsonify(message="Registration successful!"), 201
    except sqlite3.IntegrityError:
        return jsonify(error="Username already exists."), 409
    finally:
        con.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    con = db()
    try:
        user = con.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        ).fetchone()
    finally:
        con.close()

    if not user or not check_password_hash(user[0], password):
        return jsonify(error="Invalid username or password."), 401

    session.clear()
    session["username"] = username
    return jsonify(message="Login successful!")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify(message="Logged out.")

@app.route("/generate", methods=["POST"])
def generate():
    if not session.get("username"):
        return jsonify(error="Please login first."), 401

    data = request.get_json(silent=True) or {}

    phone = str(data.get("phone", "")).strip()
    brand = str(data.get("brand", "Other")).strip()
    ram = str(data.get("ram", "4 GB"))
    style = str(data.get("style", "balanced"))

    if not phone or len(phone) > 80:
        return jsonify(error="Enter a valid phone model."), 400

    presets = {
        "balanced": {
            "general": (185, 195),
            "red_dot": (175, 185),
            "scope_2x": (165, 175),
            "scope_4x": (150, 165),
            "sniper": (90, 110),
            "free_look": (110, 130),
            "fire_button": (45, 55),
            "dpi": (400, 480)
        },
        "one-tap": {
            "general": (190, 200),
            "red_dot": (180, 195),
            "scope_2x": (170, 185),
            "scope_4x": (155, 170),
            "sniper": (90, 110),
            "free_look": (115, 135),
            "fire_button": (48, 58),
            "dpi": (420, 500)
        },
        "rush": {
            "general": (185, 200),
            "red_dot": (175, 195),
            "scope_2x": (165, 185),
            "scope_4x": (150, 170),
            "sniper": (85, 105),
            "free_look": (120, 140),
            "fire_button": (50, 60),
            "dpi": (400, 500)
        },
        "sniper": {
            "general": (165, 180),
            "red_dot": (155, 170),
            "scope_2x": (145, 160),
            "scope_4x": (135, 150),
            "sniper": (80, 100),
            "free_look": (100, 120),
            "fire_button": (42, 52),
            "dpi": (380, 460)
        }
    }

    if style not in presets:
        return jsonify(error="Invalid gaming style."), 400

    result = {
        key: random.randint(low, high)
        for key, (low, high) in presets[style].items()
    }

    return jsonify(
        message="Recommendations generated!",
        phone=phone,
        brand=brand,
        ram=ram,
        style=style,
        **result
    )

@app.route("/settings", methods=["GET", "POST"])
def update_settings():
    username = session.get("username")
    if not username:
        return jsonify(error="Please login."), 401

    con = db()
    try:
        if request.method == "POST":
            data = request.get_json(silent=True) or {}

            for key in DEFAULTS:
                if key in data:
                    try:
                        value = int(data[key])
                        if not 0 <= value <= 200:
                            raise ValueError
                    except (ValueError, TypeError):
                        return jsonify(error="Invalid setting value."), 400

                    con.execute(
                        "INSERT OR REPLACE INTO settings VALUES (?,?,?)",
                        (username, key, value)
                    )
            con.commit()

        saved = dict(con.execute(
            "SELECT setting,value FROM settings WHERE username=?",
            (username,)
        ).fetchall())

        return jsonify({
            key: saved.get(key, value)
            for key, value in DEFAULTS.items()
        })
    finally:
        con.close()

@app.route("/reset", methods=["POST"])
def reset():
    username = session.get("username")
    if not username:
        return jsonify(error="Please login."), 401

    con = db()
    try:
        con.execute(
            "DELETE FROM settings WHERE username=?",
            (username,)
        )
        con.commit()
        return jsonify(message="Settings reset.")
    finally:
        con.close()

setup()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)







