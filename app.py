from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json["message"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict but caring teacher. "
                    "Never just give answers. "
                    "Explain step by step. "
                    "Ask the student to think. "
                    "Highlight common mistakes. "
                    "Be exam-oriented."
                )
            },
            {"role": "user", "content": message}
        ]
    )

    return jsonify(reply=response.choices[0].message.content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
