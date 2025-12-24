import os
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

# 🧠 Ask AI (Teacher Mode)
@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")

    prompt = f"""
    You are a professional teacher.
    Explain clearly with examples:
    {question}
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"answer": res.choices[0].message.content})

# ✂️ Summarize Notes
@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text")

    prompt = f"""
    Summarize these notes clearly for exam revision:
    {text}
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"summary": res.choices[0].message.content})

# 📝 Quiz / Test Generator
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json["topic"]
    mode = request.json["mode"]
    count = request.json["count"]

    if mode == "with_answer":
        prompt = f"""
        You are a professional teacher.
        Create {count} MCQs on "{topic}".
        Include correct answers and short explanations.
        """
    else:
        prompt = f"""
        You are an exam paper setter.
        Create {count} MCQs on "{topic}".
        Do NOT include answers.
        """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"quiz": res.choices[0].message.content})

# 📄 PDF → Test Converter
@app.route("/pdf-test", methods=["POST"])
def pdf_test():
    file = request.files.get("pdf")
    count = request.form.get("count", "5")
    mode = request.form.get("mode", "with_answer")

    if not file:
        return jsonify({"error": "No PDF uploaded"}), 400

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    text = text[:4000]

    if mode == "with_answer":
        prompt = f"""
        You are a professional teacher.
        Create {count} MCQs from this content.
        Include answers and explanations.

        Content:
        {text}
        """
    else:
        prompt = f"""
        You are an exam paper setter.
        Create {count} MCQs from this content.
        Do NOT give answers.

        Content:
        {text}
        """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"quiz": res.choices[0].message.content})

# 📊 Result Analytics
@app.route("/analyze-result", methods=["POST"])
def analyze():
    total = int(request.json["total"])
    correct = int(request.json["correct"])

    percent = round((correct / total) * 100, 2)

    if percent >= 80:
        feedback = "🌟 Excellent performance!"
    elif percent >= 50:
        feedback = "👍 Good effort. Revise weak areas."
    else:
        feedback = "📘 Needs improvement. Practice more."

    return jsonify({
        "total": total,
        "correct": correct,
        "wrong": total - correct,
        "percentage": percent,
        "feedback": feedback
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
