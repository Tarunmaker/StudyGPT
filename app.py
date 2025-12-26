from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

# ---------- 1) NORMAL ASK AI ----------
@app.route("/ask", methods=["POST"])
def ask_ai():
    q = request.json.get("message")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Explain like a good teacher. "
                    "First give a simple explanation, then step by step. "
                    "Keep it clear and exam-oriented."
                )
            },
            {"role": "user", "content": q}
        ]
    )
    return jsonify(reply=res.choices[0].message.content)

# ---------- 2) QUIZ MODE (NORMAL) ----------
@app.route("/quiz", methods=["POST"])
def quiz_mode():
    topic = request.json.get("topic")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Create 5 exam-oriented questions WITH answers. "
                    "After each answer, give a 1-2 line explanation."
                )
            },
            {"role": "user", "content": topic}
        ]
    )
    return jsonify(result=res.choices[0].message.content)

# ---------- 3) EXAM / FOCUS MODE ----------
@app.route("/exam", methods=["POST"])
def exam_mode():
    topic = request.json.get("topic")
    student_answer = request.json.get("answer", "")

    prompt = (
        "You are an exam tutor. "
        "Ask ONE question at a time from the topic. "
        "If a student answer is given, evaluate it, explain mistakes or improvements, "
        "then ask the NEXT question. "
        "Do not reveal full answers immediately. "
        "Focus on thinking process."
    )

    user_content = f"Topic: {topic}\nStudent answer: {student_answer}"

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_content}
        ]
    )
    return jsonify(reply=res.choices[0].message.content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
