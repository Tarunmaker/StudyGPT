async function askAI() {
  const q = question.value.trim();
  answer.innerHTML = "Thinking...";
  if (!q) return;

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ question: q })
    });
    const data = await res.json();
    answer.innerHTML = data.answer || data.error;
  } catch {
    answer.innerHTML = "Server error";
  }
}

async function generateQuiz() {
  quiz.innerHTML = "Generating quiz...";
  try {
    const res = await fetch("/quiz", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ question: topic.value })
    });
    const data = await res.json();
    quiz.innerHTML = data.answer || data.error;
  } catch {
    quiz.innerHTML = "Server error";
  }
}

async function summarizeNotes() {
  summary.innerHTML = "Summarizing...";
  try {
    const res = await fetch("/summarize", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ text: notes.value })
    });
    const data = await res.json();
    summary.innerHTML = data.summary || data.error;
  } catch {
    summary.innerHTML = "Server error";
  }
}
