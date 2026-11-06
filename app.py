from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


# -----------------------------
# PHONE PROFILES
# -----------------------------
PHONE_PROFILES = {
    "oppo_a6x_5g": {
        "name": "OPPO A6x 5G",
        "dpi": (400, 520),
        "fire": (38, 52),
        "base": 190
    },

    "oppo_a16": {
        "name": "OPPO A16",
        "dpi": (380, 480),
        "fire": (42, 55),
        "base": 180
    },

    "redmi_note_13": {
        "name": "Redmi Note 13",
        "dpi": (420, 560),
        "fire": (38, 50),
        "base": 195
    },

    "realme_c55": {
        "name": "Realme C55",
        "dpi": (400, 520),
        "fire": (40, 53),
        "base": 188
    },

    "samsung_a15": {
        "name": "Samsung A15",
        "dpi": (390, 510),
        "fire": (40, 54),
        "base": 185
    }
}


# -----------------------------
# GENERATOR
# -----------------------------
def generate_settings(phone, ram, mode):

    profile = PHONE_PROFILES.get(phone)

    if not profile:
        profile = {
            "dpi": (400, 520),
            "fire": (40, 52),
            "base": 185
        }

    ram = int(ram)

    # Automatic DPI
    dpi_min, dpi_max = profile["dpi"]

    if ram >= 8:
        dpi = random.randint(dpi_min + 10, dpi_max)
    elif ram >= 6:
        dpi = random.randint(dpi_min, dpi_max - 10)
    else:
        dpi = random.randint(dpi_min, dpi_max - 20)

    # Automatic Fire Button
    fire_min, fire_max = profile["fire"]

    if mode == "one_tap":
        fire_min -= 2
        fire_max -= 2

    elif mode == "drag":
        fire_min += 1
        fire_max += 3

    fire_button = random.randint(fire_min, fire_max)

    # Base sensitivity
    base = profile["base"]

    if mode == "one_tap":
        general = base + random.randint(5, 10)
        red_dot = base + random.randint(3, 8)
        scope_2x = base - random.randint(0, 5)
        scope_4x = base - random.randint(5, 12)
        sniper = base - random.randint(20, 30)
        free_look = 190

    elif mode == "drag":
        general = base + random.randint(0, 7)
        red_dot = base + random.randint(0, 5)
        scope_2x = base - random.randint(3, 8)
        scope_4x = base - random.randint(8, 15)
        sniper = base - random.randint(15, 25)
        free_look = 185

    else:  # Balanced
        general = base + random.randint(0, 5)
        red_dot = base
        scope_2x = base - 5
        scope_4x = base - 10
        sniper = base - 20
        free_look = 180

    # Keep sensitivity between 0 and 200
    sensitivities = {
        "General": min(200, max(0, general)),
        "Red Dot": min(200, max(0, red_dot)),
        "2x Scope": min(200, max(0, scope_2x)),
        "4x Scope": min(200, max(0, scope_4x)),
        "Sniper Scope": min(200, max(0, sniper)),
        "Free Look": min(200, max(0, free_look))
    }

    return {
        "dpi": dpi,
        "fire_button": fire_button,
        "sensitivity": sensitivities
    }


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template(
        "index.html",
        phones=PHONE_PROFILES
    )


# -----------------------------
# GENERATE API
# -----------------------------
@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    phone = data.get("phone")
    ram = data.get("ram")
    mode = data.get("mode")

    if not phone or not ram or not mode:
        return jsonify({
            "success": False,
            "message": "Please select all options."
        }), 400

    result = generate_settings(phone, ram, mode)

    return jsonify({
        "success": True,
        **result
    })


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

