from flask import Flask, render_template, request, jsonify, session, redirect
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
app.secret_key = "studygpt_teacher_secret"
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

USERS = {}
PROGRESS = {}   # email -> stats

# ---------- AUTH ----------
@app.route("/")
def login_page():
    if "user" in session:
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    if email in USERS and USERS[email] == password:
        session["user"] = email
        PROGRESS.setdefault(email, {
            "ask": 0,
            "quiz": 0,
            "exam": 0
        })
        return redirect("/dashboard")
    return "Invalid login"

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    USERS[email] = password
    session["user"] = email
    PROGRESS[email] = {"ask": 0, "quiz": 0, "exam": 0}
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template(
        "dashboard.html",
        user=session["user"],
        progress=PROGRESS.get(session["user"], {})
    )

# ---------- ASK AI ----------
@app.route("/ask", methods=["POST"])
def ask_ai():
    q = request.json["question"]
    PROGRESS[session["user"]]["ask"] += 1

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional teacher. Explain step-by-step, exam-focused."
            },
            {"role": "user", "content": q}
        ]
    )
    return jsonify(answer=res.choices[0].message.content)

# ---------- SUMMARIZE ----------
@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json["text"]

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize notes for exam preparation in short clear points."
            },
            {"role": "user", "content": text}
        ]
    )
    return jsonify(summary=res.choices[0].message.content)

# ---------- QUIZ MODE ----------
@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json["topic"]
    PROGRESS[session["user"]]["quiz"] += 1

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Create 5 exam-oriented revision questions with answers."
            },
            {"role": "user", "content": topic}
        ]
    )
    return jsonify(result=res.choices[0].message.content)

# ---------- EXAM / FOCUS MODE ----------
@app.route("/exam", methods=["POST"])
def exam_mode():
    topic = request.json["topic"]
    PROGRESS[session["user"]]["exam"] += 1

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict exam tutor. Ask questions one by one. "
                    "Guide thinking process. Do not reveal full answers immediately. "
                    "Focus on accuracy, time management, and common mistakes."
                )
            },
            {"role": "user", "content": topic}
        ]
    )
    return jsonify(result=res.choices[0].message.content)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
