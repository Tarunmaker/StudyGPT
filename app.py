from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "Question required"})

    # TEMP AI LOGIC (later OpenAI connect hoga)
    answer = f"This is a clear explanation for: {question}"

    history.insert(0, {
        "question": question,
        "answer": answer
    })

    return jsonify({"answer": answer, "history": history[:5]})

@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("topic", "")

    quiz_text = f"""
1. What is {topic}?
Answer: {topic} is an important concept.

2. Explain basics of {topic}.
Answer: Basics include definition and examples.
"""

    history.insert(0, {
        "question": f"Quiz on {topic}",
        "answer": quiz_text
    })

    return jsonify({"quiz": quiz_text, "history": history[:5]})

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text", "")
    summary = text[:150] + "..."

    history.insert(0, {
        "question": "Summarize Notes",
        "answer": summary
    })

    return jsonify({"summary": summary, "history": history[:5]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
