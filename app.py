from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def generate_settings(phone, ram, mode, model):
    ram = int(ram)

    # Base values according to RAM
    if ram <= 3:
        base = 165
    elif ram <= 4:
        base = 175
    elif ram <= 6:
        base = 185
    elif ram <= 8:
        base = 195
    else:
        base = 200

    # Phone type adjustment
    phone_adjust = {
        "oppo": 2,
        "vivo": 2,
        "realme": 3,
        "samsung": 0,
        "xiaomi": 2,
        "oneplus": 4,
        "iqoo": 4,
        "other": 0
    }

    base += phone_adjust.get(phone.lower(), 0)

    # Mode adjustment
    mode_adjust = {
        "one_tap": 8,
        "drag": 3,
        "balanced": 0
    }

    base += mode_adjust.get(mode, 0)

    # Keep sensitivity inside 1-200
    base = max(1, min(base, 200))

    # Different sensitivity values
    sensitivity = {
        "general": base,
        "red_dot": max(1, min(base + 2, 200)),
        "2x": max(1, min(base - 5, 200)),
        "4x": max(1, min(base - 10, 200)),
        "sniper": max(1, min(base - 20, 200)),
        "free_look": max(1, min(base + 5, 200))
    }

    # DPI
    dpi = {
        "one_tap": 480,
        "drag": 430,
        "balanced": 400
    }.get(mode, 400)

    # RAM adjustment
    if ram >= 8:
        dpi += 20
    elif ram <= 3:
        dpi -= 20

    # Fire button
    fire_button = {
        "one_tap": 48,
        "drag": 52,
        "balanced": 50
    }.get(mode, 50)

    return {
        "phone": phone,
        "ram": ram,
        "model": model,
        "mode": mode,
        "dpi": dpi,
        "fire_button": fire_button,
        "sensitivity": sensitivity
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    phone = data.get("phone")
    ram = data.get("ram")
    mode = data.get("mode")
    model = data.get("model")

    result = generate_settings(
        phone,
        ram,
        mode,
        model
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)


