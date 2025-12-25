import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# API key ENV se lega
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

# ---------- ASK AI ----------
@app.route("/ask", methods=["POST"])
def ask_ai():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "Question required"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly professional teacher. Explain clearly with examples."},
            {"role": "user", "content": question}
        ]
    )
    return jsonify({"answer": response.choices[0].message.content})

# ---------- QUIZ ----------
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic required"})

    prompt = f"""
Create 5 MCQs on "{topic}".
Give options, correct answer and short explanation.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"quiz": response.choices[0].message.content})

# ---------- SUMMARIZE ----------
@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text required"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize these notes for exam revision:\n{text}"}]
    )
    return jsonify({"summary": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
