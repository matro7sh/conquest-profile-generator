from flask import Flask, render_template, request, jsonify
from generator import generate_profile_by_name, TEMPLATE_NAMES

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", templates=TEMPLATE_NAMES)
    
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    name = data.get("template")

    if name not in TEMPLATE_NAMES:
        return jsonify({"error": "invalid template"}), 400

    left = generate_profile_by_name(name)
    right = generate_profile_by_name(name)

    return jsonify({
        "left": left,
        "right": right
    })

if __name__ == "__main__":
    app.run(debug=True)