from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# 🧠 OpenAI API Key (enter your own)
openai.api_key = "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"

@app.route("/")
def index():
    return render_template("index.html")


# 💬 General Question (Ask AI)
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and knowledgeable AI study assistant that explains concepts clearly with examples."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message["content"]
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🧩 Generate Quiz
@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json()
    topic = data.get("question", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a quiz generator that creates interesting and challenging multiple-choice questions."},
                {"role": "user", "content": f"Create a 5-question quiz on the topic: {topic}. Each question should have 4 options and indicate the correct answer."}
            ]
        )
        quiz_text = response.choices[0].message["content"]
        return jsonify({"answer": quiz_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✂️ Summarize Notes
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize long notes into short, easy-to-understand bullet points."},
                {"role": "user", "content": f"Summarize the following notes:\n\n{text}"}
            ]
        )
        summary = response.choices[0].message["content"]
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
