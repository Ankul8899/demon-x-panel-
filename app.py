
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

settings = {
    "general": 190,
    "red_dot": 180,
    "scope_2x": 170,
    "scope_4x": 160,
    "fire_button": 50
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/settings", methods=["GET", "POST"])
def update_settings():
    if request.method == "POST":
        data = request.get_json()
        for key in settings:
            if key in data:
                settings[key] = max(0, min(200, int(data[key])))
        return jsonify(settings)

    return jsonify(settings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



