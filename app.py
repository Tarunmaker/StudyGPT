from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

# OpenAI client (Render ENV se key lega)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Home
@app.route("/")
def index():
    return render_template("index.html")

# Chat / Ask GPT
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("question", "")

    if not user_input:
        return jsonify({"error": "No question provided"}), 400

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful study assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

# Simple Test Generator
@app.route("/generate-test", methods=["POST"])
def generate_test():
    data = request.json
    topic = data.get("topic", "")

    prompt = f"Create a 5-question test for the topic: {topic}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"test": response.choices[0].message.content})

# Render compatible run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
