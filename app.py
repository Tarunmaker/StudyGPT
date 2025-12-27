@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    topic = data.get("topic")
    mode = data.get("mode")
    count = data.get("count")

    if mode == "with_answer":
        prompt = f"""
        You are a professional teacher.
        Create {count} MCQ questions on topic "{topic}".
        Provide:
        - Question
        - 4 options
        - Correct answer
        - Short teacher explanation.
        """
    else:
        prompt = f"""
        You are an exam paper setter.
        Create {count} MCQ questions on topic "{topic}".
        Provide:
        - Question
        - 4 options
        - Do NOT give answers.
        """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"quiz": response.choices[0].message.content})
