import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

# 🧠 Ask Doubt (Teacher Mode)
@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question", "").strip()
    if not q:
        return jsonify({"error": "Empty question"}), 400

    prompt = f"""
You are a friendly professional teacher.
Explain simply, step-by-step, with a quick example.
End with 1 motivating line.

Question:
{q}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"answer": res.choices[0].message.content})

# 📝 Quiz / Test
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("topic","")
    mode = request.json.get("mode","with_answer")
    count = request.json.get("count","5")

    if not topic:
        return jsonify({"error":"Topic required"}), 400

    if mode == "with_answer":
        prompt = f"""
You are a teacher.
Create {count} MCQs on "{topic}".
Include options, correct answer, and a short explanation.
"""
    else:
        prompt = f"""
You are an exam setter.
Create {count} MCQs on "{topic}".
Only questions and options. No answers.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"quiz": res.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
