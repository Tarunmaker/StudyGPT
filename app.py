from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# ---------------- HOME PAGE ----------------
@app.route("/")
def index():
    return """
    <h1>StudyGPT Running ✅</h1>
    <p>Your Flask app is live.</p>
    """

# ---------------- API TEST ROUTE ----------------
@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "StudyGPT backend working"})

# ---------------- MAIN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
