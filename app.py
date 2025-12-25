import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from PyPDF2 import PdfReader

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

# ---------- ASK AI ----------
@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question","").strip()
    if not q:
        return jsonify({"error":"Question required"})

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a professional teacher. Explain step by step."},
            {"role":"user","content":q}
        ]
    )
    return jsonify({"answer":res.choices[0].message.content})

# ---------- QUIZ ----------
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("topic","").strip()
    if not topic:
        return jsonify({"error":"Topic required"})

    prompt = f"""
Create 5 MCQs on {topic}.
Give options, correct answer and explanation.
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"quiz":res.choices[0].message.content})

# ---------- REAL TEST ----------
@app.route("/real-test", methods=["POST"])
def real_test():
    topic = request.json.get("topic","")

    prompt = f"""
Create 5 MCQs on {topic}.
Return STRICT JSON ONLY:
[
  {{
    "q":"Question",
    "options":["A","B","C","D"],
    "answer":"A"
  }}
]
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"questions":res.choices[0].message.content})

# ---------- PDF TO TEST ----------
@app.route("/pdf-test", methods=["POST"])
def pdf_test():
    pdf = request.files.get("pdf")
    if not pdf:
        return jsonify({"error":"No PDF uploaded"})

    reader = PdfReader(pdf)
    text=""
    for p in reader.pages:
        if p.extract_text():
            text+=p.extract_text()

    prompt = f"""
Create 5 MCQs from this content:
{text[:3000]}
"""
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"quiz":res.choices[0].message.content})

if __name__ == "__main__":
    app.run(debug=True)
