from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import os
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'evranoo-secret-2024')
CORS(app)

PASSWORD = "E210"
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "savings": {"balance": 0, "target": 10000000, "history": []},
            "habits": {"items": [], "logs": {}},
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Auth ──────────────────────────────────────────────────────────────────────

@app.route("/api/login", methods=["POST"])
def login():
    body = request.get_json()
    if body.get("password") == PASSWORD:
        session["auth"] = True
        return jsonify({"ok": True})
    return jsonify({"ok": False, "msg": "Password salah"}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True})

def require_auth():
    return session.get("auth") is True

# ── Main page ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

# ── Savings ───────────────────────────────────────────────────────────────────

@app.route("/api/savings", methods=["GET"])
def get_savings():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = load_data()
    return jsonify(data["savings"])

@app.route("/api/savings/transaction", methods=["POST"])
def transaction():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json()
    amount = int(body.get("amount", 0))
    t_type = body.get("type")  # "add" or "sub"
    note = body.get("note", "")

    data = load_data()
    if t_type == "add":
        data["savings"]["balance"] += amount
    elif t_type == "sub":
        data["savings"]["balance"] = max(0, data["savings"]["balance"] - amount)

    data["savings"]["history"].append({
        "type": t_type,
        "amount": amount,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_data(data)
    return jsonify(data["savings"])

@app.route("/api/savings/target", methods=["POST"])
def set_target():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json()
    data = load_data()
    data["savings"]["target"] = int(body.get("target", 10000000))
    save_data(data)
    return jsonify(data["savings"])

# ── Habits ────────────────────────────────────────────────────────────────────

@app.route("/api/habits", methods=["GET"])
def get_habits():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = load_data()
    today = date.today().isoformat()
    return jsonify({
        "items": data["habits"]["items"],
        "logs": data["habits"]["logs"],
        "today": today
    })

@app.route("/api/habits/item", methods=["POST"])
def add_habit():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json()
    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "Name required"}), 400
    data = load_data()
    data["habits"]["items"].append({"id": str(int(datetime.now().timestamp()*1000)), "name": name})
    save_data(data)
    return jsonify(data["habits"]["items"])

@app.route("/api/habits/item/<item_id>", methods=["DELETE"])
def delete_habit(item_id):
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    data = load_data()
    data["habits"]["items"] = [i for i in data["habits"]["items"] if i["id"] != item_id]
    save_data(data)
    return jsonify(data["habits"]["items"])

@app.route("/api/habits/log", methods=["POST"])
def log_habit():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json()
    item_id = body.get("id")
    today = date.today().isoformat()
    data = load_data()
    if today not in data["habits"]["logs"]:
        data["habits"]["logs"][today] = []
    logs_today = data["habits"]["logs"][today]
    if item_id in logs_today:
        logs_today.remove(item_id)
    else:
        logs_today.append(item_id)
    save_data(data)
    return jsonify({"date": today, "checked": data["habits"]["logs"][today]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
