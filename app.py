from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


PHONE_PROFILES = {
    "oppo_a16": {
        "name": "OPPO A16",
        "base": 120
    },
    "oppo_a6x_5g": {
        "name": "OPPO A6x 5G",
        "base": 135
    },
    "redmi_note": {
        "name": "Redmi Note Series",
        "base": 130
    },
    "realme_c": {
        "name": "realme C Series",
        "base": 125
    },
    "samsung_a": {
        "name": "Samsung A Series",
        "base": 120
    },
    "other": {
        "name": "Other Phone",
        "base": 120
    }
}


def clamp(value):
    return max(0, min(200, round(value)))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    phone = data.get("phone", "other")
    ram = int(data.get("ram", 4))
    mode = data.get("mode", "balanced")

    profile = PHONE_PROFILES.get(
        phone,
        PHONE_PROFILES["other"]
    )

    base = profile["base"]

    # RAM adjustment
    if ram >= 8:
        base += 8
    elif ram == 6:
        base += 4
    elif ram <= 3:
        base -= 8

    # Play style adjustment
    if mode == "one_tap":
        base += 12
    elif mode == "drag":
        base += 7
    else:
        base += 0

    result = {
        "general": clamp(base + 20),
        "red_dot": clamp(base + 10),
        "scope_2x": clamp(base),
        "scope_4x": clamp(base - 12),
        "sniper": clamp(base - 28),
        "free_look": clamp(base + 15)
    }

    return jsonify({
        "phone": profile["name"],
        "ram": f"{ram} GB",
        "mode": mode.replace("_", " ").title(),
        "settings": result
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

