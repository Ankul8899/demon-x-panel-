from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def generate_sensitivity(phone, ram, dpi, mode, fire_button):
    dpi = int(dpi)
    fire_button = int(fire_button)
    ram = int(ram)

    # Base sensitivity
    if dpi < 350:
        base = 175
    elif dpi < 450:
        base = 185
    elif dpi < 550:
        base = 195
    else:
        base = 200

    # RAM adjustment
    if ram <= 3:
        base -= 8
    elif ram >= 8:
        base += 3

    # Mode adjustment
    if mode == "one_tap":
        general = base + 5
        red_dot = base
        scope_2x = base - 8
        scope_4x = base - 18
        sniper = base - 30
    elif mode == "drag":
        general = base
        red_dot = base - 5
        scope_2x = base - 12
        scope_4x = base - 22
        sniper = base - 35
    else:
        general = base
        red_dot = base - 3
        scope_2x = base - 10
        scope_4x = base - 20
        sniper = base - 32

    values = [
        general,
        red_dot,
        scope_2x,
        scope_4x,
        sniper
    ]

    values = [max(0, min(200, x)) for x in values]

    return {
        "phone": phone,
        "ram": f"{ram} GB",
        "dpi": dpi,
        "mode": mode,
        "fire_button": fire_button,
        "general": values[0],
        "red_dot": values[1],
        "scope_2x": values[2],
        "scope_4x": values[3],
        "sniper": values[4],
        "free_look": max(0, min(200, base + 10))
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    result = generate_sensitivity(
        data.get("phone", "Unknown"),
        data.get("ram", 4),
        data.get("dpi", 400),
        data.get("mode", "balanced"),
        data.get("fire_button", 50)
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

