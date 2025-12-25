async function askAI() {
  const q = question.value.trim();
  if (!q) return;
  answer.innerHTML = "Thinking...";

  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question: q })
  });
  const data = await res.json();
  answer.innerHTML = data.answer || data.error;
}

async function generateQuiz() {
  quiz.innerHTML = "Generating quiz...";
  const res = await fetch("/quiz", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ topic: topic.value })
  });
  const data = await res.json();
  quiz.innerHTML = data.quiz || data.error;
}

async function summarizeNotes() {
  summary.innerHTML = "Summarizing...";
  const res = await fetch("/summarize", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text: notes.value })
  });
  const data = await res.json();
  summary.innerHTML = data.summary || data.error;
}
