// 💬 Ask AI
async function askAI() {
  const question = document.getElementById("question").value.trim();
  const answerBox = document.getElementById("answer");
  answerBox.innerHTML = "<p>🤔 Thinking...</p>";

  if (!question) {
    answerBox.innerHTML = "<p style='color:red;'>Please enter a question!</p>";
    return;
  }

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: question })   // ✅ FIXED
    });

    const data = await res.json();

    if (data.error) {
      answerBox.innerHTML = `<p style='color:red;'>Error: ${data.error}</p>`;
    } else {
      answerBox.innerHTML = `<b>🧠 AI:</b><br>${data.answer.replace(/\n/g, "<br>")}`;
    }
  } catch {
    answerBox.innerHTML = "<p style='color:red;'>⚠️ Error connecting to server.</p>";
  }
}


// 🧮 Generate Quiz (MCQs)
async function generateQuiz() {
  const topic = document.getElementById("topic").value.trim();
  const quizBox = document.getElementById("quiz");
  quizBox.innerHTML = "<p>🧮 Generating quiz...</p>";

  if (!topic) {
    quizBox.innerHTML = "<p style='color:red;'>Please enter a topic!</p>";
    return;
  }

  try {
    const res = await fetch("/test", {   // ✅ FIXED (/quiz → /test)
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic })    // ✅ FIXED
    });

    const data = await res.json();

    if (data.error) {
      quizBox.innerHTML = `<p style='color:red;'>Error: ${data.error}</p>`;
    } else {
      quizBox.innerHTML = `<b>📘 Quiz on ${topic}:</b><br>${data.test.replace(/\n/g, "<br>")}`;
    }
  } catch {
    quizBox.innerHTML = "<p style='color:red;'>⚠️ Error connecting to server.</p>";
  }
}


// ✂️ Summarize Notes
async function summarizeNotes() {
  const text = document.getElementById("notes").value.trim();
  const summaryBox = document.getElementById("summary");
  summaryBox.innerHTML = "<p>🪶 Summarizing...</p>";

  if (!text) {
    summaryBox.innerHTML = "<p style='color:red;'>Please paste some notes first!</p>";
    return;
  }

  try {
    const res = await fetch("/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });

    const data = await res.json();

    if (data.error) {
      summaryBox.innerHTML = `<p style='color:red;'>Error: ${data.error}</p>`;
    } else {
      summaryBox.innerHTML = `<b>📝 Summary:</b><br>${data.summary.replace(/\n/g, "<br>")}`;
    }
  } catch {
    summaryBox.innerHTML = "<p style='color:red;'>⚠️ Error connecting to server.</p>";
  }
}
