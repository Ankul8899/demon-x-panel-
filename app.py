
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    phone = data.get("phone", "normal")
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

    # Small variation for personalized starting presets
    variation = random.randint(-3, 3)

    result = {
        "general": max(0, min(200, settings[0] + variation)),
        "red_dot": max(0, min(200, settings[1] + variation)),
        "scope_2x": max(0, min(200, settings[2] + variation)),
        "scope_4x": max(0, min(200, settings[3] + variation)),
        "fire_button": settings[4]
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)




