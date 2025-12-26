from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
import os, random, datetime

app = Flask(__name__)
app.secret_key = "studygpt_secret_key"

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DUMMY DATABASE ----------------
USERS = {
    "student": "1234"
}

TEST_HISTORY = []   # [{date, score, total, percent}]

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if USERS.get(username) == password:
            session["user"] = username
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", history=TEST_HISTORY)

# ---------------- ASK AI ----------------
@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question required"})

    answer = f"""
👨‍🏫 Teacher Explanation

Your question: {question}

• Break the concept into basics  
• Understand definitions  
• Practice examples  

📌 Tip: Revise again tomorrow for better retention.
"""
    return jsonify({"answer": answer.strip()})

# ---------------- GENERATE MCQ TEST ----------------
@app.route("/generate-test", methods=["POST"])
def generate_test():
    data = request.json
    topic = data.get("topic", "General")
    count = int(data.get("count", 5))

    questions = []
    for i in range(count):
        correct = random.randint(0, 3)
        questions.append({
            "question": f"{topic} Question {i+1}",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": correct
        })

    return jsonify({"questions": questions})

# ---------------- SUBMIT TEST ----------------
@app.route("/submit-test", methods=["POST"])
def submit_test():
    data = request.json
    questions = data.get("questions", [])
    answers = data.get("answers", [])

    score = 0
    for i, q in enumerate(questions):
        if i < len(answers) and answers[i] == q["correct"]:
            score += 1

    total = len(questions)
    percent = round((score / total) * 100, 2) if total else 0

    TEST_HISTORY.append({
        "date": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "score": score,
        "total": total,
        "percent": percent
    })

    guidance = (
        "🌟 Excellent work! Try advanced questions."
        if percent >= 80 else
        "👍 Good attempt. Revise weak areas."
        if percent >= 50 else
        "⚠️ Start from basics and practice daily."
    )

    return jsonify({
        "score": score,
        "total": total,
        "percent": percent,
        "guidance": guidance
    })

# ---------------- PDF → TEST (SAFE) ----------------
@app.route("/pdf-test", methods=["POST"])
def pdf_test():
    file = request.files.get("pdf")
    if not file:
        return jsonify({"error": "No PDF uploaded"})

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return jsonify({
        "message": "PDF uploaded successfully",
        "preview": text[:300]
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
