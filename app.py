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

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a good teacher. "
                    "Explain step by step. "
                    "Focus on understanding and exam clarity."
                )
            },
            {"role": "user", "content": q}
        ]
    )
    return jsonify(answer=res.choices[0].message.content)

@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("topic")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Create 5 revision questions with answers."
            },
            {"role": "user", "content": topic}
        ]
    )
    return jsonify(result=res.choices[0].message.content)

@app.route("/exam", methods=["POST"])
def exam():
    topic = request.json.get("topic")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an exam tutor. "
                    "Create 5 MCQ questions. "
                    "Provide options A,B,C,D and correct answer index."
                )
            },
            {"role": "user", "content": topic}
        ]
    )
    return jsonify(result=res.choices[0].message.content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
