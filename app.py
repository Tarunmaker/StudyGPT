import os, json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# simple in-memory stats
stats = {
    "questions": 0,
    "tests": 0,
    "correct": 0,
    "total": 0
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# -------- ASK AI --------
@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question","")
    stats["questions"] += 1

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a friendly teacher. Explain clearly."},
            {"role":"user","content":q}
        ]
    )
    return jsonify({"answer":res.choices[0].message.content})

# -------- REAL TEST --------
@app.route("/test", methods=["POST"])
def test():
    topic = request.json.get("topic")

    prompt = f"""
Create 5 MCQs on {topic}.
Return STRICT JSON:
[
  {{
    "q":"question",
    "options":["A","B","C","D"],
    "answer":"A"
  }}
]
"""

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"test":res.choices[0].message.content})

# -------- DASHBOARD DATA --------
@app.route("/stats")
def get_stats():
    accuracy = 0
    if stats["total"] > 0:
        accuracy = round(stats["correct"]/stats["total"]*100,2)
    return jsonify({
        "questions":stats["questions"],
        "tests":stats["tests"],
        "accuracy":accuracy
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
