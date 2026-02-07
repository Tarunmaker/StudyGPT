 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app.py b/app.py
index 87727b46001f782732401ff60360f699be5ae14b..ebed372cceb62299147dc801060d2f5633490199 100644
--- a/app.py
+++ b/app.py
@@ -1,63 +1,202 @@
-from flask import Flask, render_template, request, jsonify
+from collections import Counter
+from flask import Flask, render_template, request, jsonify, send_file
+import io
 from flask_cors import CORS
 
 app = Flask(__name__)
 CORS(app)
 
 history = []
 
+def extract_topics(text):
+    topics = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
+    counts = Counter(topics)
+    return counts
+
+def generate_questions(topics, limit=12):
+    templates = [
+        "Explain the concept of {topic}.",
+        "Define {topic} with an example.",
+        "Compare and contrast {topic} with related ideas.",
+        "List key points about {topic}.",
+        "Solve a short problem on {topic}.",
+        "Write short notes on {topic}."
+    ]
+    questions = []
+    for topic in topics:
+        for template in templates:
+            questions.append(template.format(topic=topic))
+            if len(questions) >= limit:
+                return questions
+    return questions
+
+def build_pdf(lines):
+    sanitized = [line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") for line in lines]
+    content = "BT\n/F1 12 Tf\n50 760 Td\n"
+    for line in sanitized:
+        content += f"({line}) Tj\nT* \n"
+    content += "ET"
+    content_bytes = content.encode("utf-8")
+
+    objects = []
+    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
+    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
+    objects.append(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n")
+    objects.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
+    objects.append(f"5 0 obj\n<< /Length {len(content_bytes)} >>\nstream\n".encode("utf-8") + content_bytes + b"\nendstream\nendobj\n")
+
+    xref_positions = []
+    pdf = b"%PDF-1.4\n"
+    for obj in objects:
+        xref_positions.append(len(pdf))
+        pdf += obj
+    xref_start = len(pdf)
+    pdf += f"xref\n0 {len(objects) + 1}\n".encode("utf-8")
+    pdf += b"0000000000 65535 f \n"
+    for pos in xref_positions:
+        pdf += f"{pos:010d} 00000 n \n".encode("utf-8")
+    pdf += b"trailer\n"
+    pdf += f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode("utf-8")
+    pdf += b"startxref\n"
+    pdf += f"{xref_start}\n".encode("utf-8")
+    pdf += b"%%EOF\n"
+    return pdf
+
 @app.route("/")
 def home():
     return render_template("index.html")
 
+@app.route("/profile")
+def profile():
+    return render_template("profile.html")
+
+@app.route("/community")
+def community():
+    return render_template("community.html")
+
+@app.route("/quick-tools")
+def quick_tools():
+    return render_template("quick_tools.html")
+
 @app.route("/ask", methods=["POST"])
 def ask_ai():
     data = request.json
     question = data.get("question", "")
 
     if not question:
         return jsonify({"error": "Question required"})
 
     # TEMP AI LOGIC (later OpenAI connect hoga)
     answer = f"This is a clear explanation for: {question}"
 
     history.insert(0, {
         "question": question,
         "answer": answer
     })
 
     return jsonify({"answer": answer, "history": history[:5]})
 
 @app.route("/quiz", methods=["POST"])
 def quiz():
     topic = request.json.get("topic", "")
 
     quiz_text = f"""
 1. What is {topic}?
 Answer: {topic} is an important concept.
 
 2. Explain basics of {topic}.
 Answer: Basics include definition and examples.
 """
 
     history.insert(0, {
         "question": f"Quiz on {topic}",
         "answer": quiz_text
     })
 
     return jsonify({"quiz": quiz_text, "history": history[:5]})
 
 @app.route("/summarize", methods=["POST"])
 def summarize():
     text = request.json.get("text", "")
     summary = text[:150] + "..."
 
     history.insert(0, {
         "question": "Summarize Notes",
         "answer": summary
     })
 
     return jsonify({"summary": summary, "history": history[:5]})
 
+@app.route("/pyq", methods=["POST"])
+def analyze_pyq():
+    uploaded_file = request.files.get("file")
+    text = ""
+    if uploaded_file:
+        text = uploaded_file.read().decode("utf-8", errors="ignore")
+    counts = extract_topics(text)
+    unique_topics = [topic for topic, _ in counts.most_common(5)]
+    analysis = "Key focus areas: " + ", ".join(unique_topics) if unique_topics else "Upload a PYQ text file to analyze key topics."
+    questions = generate_questions(unique_topics, limit=10)
+
+    history.insert(0, {
+        "question": "PYQ Analyzer",
+        "answer": analysis
+    })
+
+    return jsonify({
+        "analysis": analysis,
+        "questions": questions,
+        "topic_counts": [{"topic": topic, "count": count} for topic, count in counts.most_common(8)],
+        "history": history[:5]
+    })
+
+@app.route("/pyq/mock-pdf", methods=["POST"])
+def mock_questions_pdf():
+    uploaded_file = request.files.get("file")
+    text = ""
+    if uploaded_file:
+        text = uploaded_file.read().decode("utf-8", errors="ignore")
+    counts = extract_topics(text)
+    topics = [topic for topic, _ in counts.most_common(5)]
+    questions = generate_questions(topics, limit=12)
+    if not questions:
+        questions = ["Upload a PYQ file to generate mock questions."]
+    pdf_lines = ["StudySmart Mock Questions", ""] + [f"{idx + 1}. {q}" for idx, q in enumerate(questions)]
+    pdf_bytes = build_pdf(pdf_lines)
+    return send_file(io.BytesIO(pdf_bytes), mimetype="application/pdf", as_attachment=True, download_name="mock-questions.pdf")
+
+@app.route("/strategy", methods=["POST"])
+def strategy():
+    data = request.json or {}
+    exam_date = data.get("examDate", "")
+    hours = data.get("hours", "")
+    plan = [
+        "Day 1-2: Review high-weightage topics and formulas.",
+        "Day 3-4: Solve PYQ sets and note weak areas.",
+        "Day 5: Revise notes + short mock test.",
+        "Day 6: Focus on weak areas and practice numericals.",
+        "Day 7: Quick revision and confidence boost."
+    ]
+    checklist = [
+        "Finish one PYQ set",
+        "Revise summary notes",
+        "Attempt 15 practice questions",
+        "Track mistakes"
+    ]
+    return jsonify({
+        "summary": f"Strategy for exam on {exam_date} with {hours} hours/day.",
+        "plan": plan,
+        "checklist": checklist
+    })
+
+@app.route("/focus-test", methods=["POST"])
+def focus_test():
+    data = request.json or {}
+    topic = data.get("topic", "").strip()
+    if not topic:
+        return jsonify({"questions": []})
+    questions = generate_questions([topic], limit=10)
+    return jsonify({"questions": questions})
+
 if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)
 
EOF
)
