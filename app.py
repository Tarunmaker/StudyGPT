from flask import Flask, render_template, request, jsonify
import random
import datetime

app = Flask(__name__)

# =========================
# In-memory storage (demo)
# =========================
TEST_HISTORY = []

# =========================
# HOME
# =========================
@app.route("/")
def index():
    return render_template("index.html")

# =========================
# ASK AI (Teacher Style)
# =========================
@app.route("/ask", methods=["POST"])
def ask_ai():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify(error="Question is empty")

    answer = f"""
👨‍🏫 Teacher Explanation:

Your question was: "{question}"

Think of it step-by-step:
1️⃣ Understand the concept  
2️⃣ Apply logic  
3️⃣ Practice with examples  

📌 Tip: Revise this topic again after 24 hours for strong memory.
"""

    return jsonify(answer=answer.strip())

# =========================
# GENERATE REAL MCQ TEST
# =========================
@app.route("/test", methods=["POST"])
def generate_test():
    data = request.json
    topic = data.get("topic", "General")
    count = int(data.get("count", 5))

    questions = []

    for i in range(count):
        correct = random.randint(0, 3)
        options = ["Option A", "Option B", "Option C", "Option D"]

        questions.append({
            "question": f"{topic} Question {i+1}",
            "options": options,
            "correct": correct
        })

    return jsonify({
        "topic": topic,
        "questions": questions
    })

# =========================
# SUBMIT TEST
# =========================
@app.route("/submit-test", methods=["POST"])
def submit_test():
    data = request.json
    answers = data.get("answers", [])
    questions = data.get("questions", [])

    score = 0
    result_detail = []

    for i, q in enumerate(questions):
        is_correct = answers[i] == q["correct"]
        if is_correct:
            score += 1

        result_detail.append({
            "question": q["question"],
            "correct": q["correct"],
            "selected": answers[i],
            "is_correct": is_correct
        })

    percentage = round((score / len(questions)) * 100, 2)

    guidance = teacher_guidance(percentage)

    history_entry = {
        "date": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "score": score,
        "total": len(questions),
        "percentage": percentage
    }

    TEST_HISTORY.append(history_entry)

    return jsonify({
        "score": score,
        "total": len(questions),
        "percentage": percentage,
        "guidance": guidance,
        "details": result_detail
    })

# =========================
# TEST HISTORY
# =========================
@app.route("/history")
def history():
    return jsonify(TEST_HISTORY)

# =========================
# TEACHER GUIDANCE LOGIC
# =========================
def teacher_guidance(percent):
    if percent >= 85:
        return "🌟 Excellent! You have strong command. Try advanced level questions."
    elif percent >= 60:
        return "👍 Good job! Revise weak areas and practice more MCQs."
    else:
        return "⚠️ Needs improvement. Start from basics and take short tests daily."

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
