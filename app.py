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
def ask_ai():
    question = request.json.get("question")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Explain clearly like a good teacher. Step by step."
            },
            {"role": "user", "content": question}
        ]
    )
    return jsonify(answer=res.choices[0].message.content)

@app.route("/quiz", methods=["POST"])
def quiz():
    topic = request.json.get("question")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Create 5 exam-style questions with answers."
            },
            {"role": "user", "content": topic}
        ]
    )
    return jsonify(answer=res.choices[0].message.content)

@app.route("/summarize", methods=["POST"])
def summarize():
    text = request.json.get("text")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize notes into short, clear exam-friendly points."
            },
            {"role": "user", "content": text}
        ]
    )
    return jsonify(summary=res.choices[0].message.content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
