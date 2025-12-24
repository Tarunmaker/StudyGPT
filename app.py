import os, json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from pypdf import PdfReader

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- ASK AI ----------------
@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question","")

    prompt = f"""
You are a friendly professional teacher.
Explain clearly with steps and one example.
End with encouragement.

Question:
{q}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"answer":res.choices[0].message.content})

# ---------------- QUIZ (TEXT) ----------------
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json["topic"]
    count = request.json["count"]
    mode = request.json["mode"]

    if mode == "with_answer":
        prompt = f"""
Create {count} MCQs on "{topic}".
Include options, correct answer and explanation.
"""
    else:
        prompt = f"""
Create {count} MCQs on "{topic}".
Only questions and options. No answers.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"quiz":res.choices[0].message.content})

# ---------------- REAL TEST MODE (JSON) ----------------
@app.route("/test", methods=["POST"])
def test():
    topic = request.json["topic"]
    count = request.json["count"]

    prompt = f"""
Create {count} MCQs on "{topic}".
Return ONLY valid JSON array like this:

[
 {{"question":"...","options":["A","B","C","D"],"answer":"A"}}
]
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return jsonify({"mcqs":res.choices[0].message.content})

# ---------------- SUMMARIZE ----------------
@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json["text"]

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":f"Summarize for exam revision:\n{text}"}]
    )
    return jsonify({"summary":res.choices[0].message.content})

# ---------------- PDF → TEST ----------------
@app.route("/pdf-test", methods=["POST"])
def pdf_test():
    pdf = request.files["pdf"]
    count = request.form["count"]

    reader = PdfReader(pdf)
    text = ""
    for p in reader.pages:
        text += p.extract_text() or ""

    prompt = f"""
From this study material create {count} MCQs with answers:

{text[:3500]}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )
    return jsonify({"quiz":res.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
