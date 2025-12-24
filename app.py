from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Load API key from environment variable (Render Dashboard → Environment → OPENAI_API_KEY)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "<h1>StudyGPT Running ✅</h1><p>Your Flask app is live.</p>"


# 1️⃣ ASK AI / EXPLAIN FEATURE
@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.json
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )

        return jsonify({"result": response.choices[0].message["content"].strip()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2️⃣ SUMMARIZE NOTES FEATURE
@app.route("/summarize", methods=["POST"])
def summarize_notes():
    try:
        data = request.json
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        prompt = f"Summarize the following notes in simple and short bullet points:\n\n{text}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message["content"].strip()
        return jsonify({"result": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3️⃣ TEST / QUIZ FEATURE
@app.route("/test", methods=["POST"])
def test_generator():
    try:
        data = request.json
        topic = data.get("topic", "")

        if not topic:
            return jsonify({"error": "No topic provided"}), 400

        prompt = f"""
        Create 5 multiple-choice questions (MCQs) from the topic below.
        Include 4 options for each and mark the correct answer.

        Topic:
        {topic}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        quiz = response.choices[0].message["content"].strip()
        return jsonify({"result": quiz})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4️⃣ REQUIRED FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
