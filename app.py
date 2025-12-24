import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# OpenAI API key ENV se lega
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ASK AI ----------------
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question required"})

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly professional teacher. Explain clearly with steps and example."
                },
                {"role": "user", "content": question}
            ]
        )
        return jsonify({"answer": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------- QUIZ ----------------
@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    topic = data.get("question", "").strip()

    if not topic:
        return jsonify({"error": "Topic required"})

    prompt = f"""
Create 5 MCQs on "{topic}".
Give options, correct answer and short explanation.
"""

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return jsonify({"answer": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

# ---------------- SUMMARIZE ----------------
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text required"})

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Summarize for exam revision:\n{text}"}
            ]
        )
        return jsonify({"summary": res.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
