import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    mode = data.get("mode", "normal")

    if mode == "normal":
        system_prompt = "You are a helpful teacher. Explain simply."

    elif mode == "quiz":
        system_prompt = (
            "You are a teacher creating revision questions WITH answers. "
            "Keep it short and exam-oriented."
        )

    elif mode == "exam":
        system_prompt = (
            "You are an AI tutor helping a student prepare for exams. "
            "Ask ONE question at a time. "
            "Wait for student's answer, then give feedback and next question. "
            "Be strict but supportive."
        )

    else:
        system_prompt = "You are a helpful assistant."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7
        )

        return jsonify({
            "answer": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
