from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

# ---------------- ASK AI ----------------
@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.json
    q = data.get("question")

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional teacher helping students."},
                {"role": "user", "content": q}
            ]
        )
        return jsonify({"answer": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------- QUIZ WITH ANSWER ----------------
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("question")

    prompt = f"""
Create 5 MCQs on {topic}.
Give answer and explanation after each question.
"""

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"answer": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------- REAL TEST MODE ----------------
@app.route("/test", methods=["POST"])
def test():
    topic = request.json.get("topic")

    prompt = f"""
Create a real exam style MCQ test on {topic}.
5 questions.
Format STRICT JSON like this:
[
  {{
    "q": "question",
    "options": ["A","B","C","D"],
    "answer": "A"
  }}
]
"""

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"test": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
