import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- STUDENT DATA (simple) ----------
student = {
    "name": "Student",
    "xp": 0,
    "questions": 0,
    "tests": 0,
    "premium": False
}

def level(xp):
    if xp < 100: return "Beginner"
    if xp < 300: return "Learner"
    if xp < 700: return "Scholar"
    return "Pro Student"

# ---------- PAGES ----------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/leaderboard")
def leaderboard_page():
    return render_template("leaderboard.html")

# ---------- APIs ----------
@app.route("/ask", methods=["POST"])
def ask():
    q = request.json["question"]
    student["xp"] += 2
    student["questions"] += 1

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":q}]
    )
    return jsonify({"answer": res.choices[0].message.content})

@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json["topic"]
    count = request.json["count"]
    student["xp"] += 10
    student["tests"] += 1

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role":"user",
            "content":f"Create {count} MCQs with answers on {topic}"
        }]
    )
    return jsonify({"quiz": res.choices[0].message.content})

@app.route("/student")
def student_data():
    return jsonify({
        "name": student["name"],
        "xp": student["xp"],
        "level": level(student["xp"]),
        "questions": student["questions"],
        "tests": student["tests"],
        "premium": student["premium"]
    })

@app.route("/leaderboard-data")
def leaderboard_data():
    return jsonify([{
        "rank": 1,
        "name": student["name"],
        "xp": student["xp"],
        "level": level(student["xp"])
    }])

@app.route("/toggle-premium")
def toggle_premium():
    student["premium"] = not student["premium"]
    return jsonify({"premium": student["premium"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

