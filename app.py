import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

# student stats (simple)
stats = {
    "questions": 0,
    "quizzes": 0,
    "pdf_tests": 0
}

@app.route("/")
def home():
    return render_template("index.html")

# -------- ASK AI --------
@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question", "").strip()
    if not q:
        return jsonify({"error": "Question required"})

    stats["questions"] += 1

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional teacher. Explain clearly."},
            {"role": "user", "content": q}
        ]
    )
    return jsonify({"answer": res.choices[0].message.content})

# -------- QUIZ --------
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Topic required"})

    stats["quizzes"] += 1

    prompt = f"""
Create 5 MCQs on "{topic}".
Give options, correct answer and short explanation.
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"quiz": res.choices[0].message.content})

# -------- PDF TO TEST --------
@app.route("/pdf-test", methods=["POST"])
def pdf_test():
    pdf = request.files.get("pdf")
    if not pdf:
        return jsonify({"error": "No PDF uploaded"})

    stats["pdf_tests"] += 1

    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    prompt = f"""
Create 5 MCQs from the following content:
{text[:3000]}
"""

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"quiz": res.choices[0].message.content})

# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
