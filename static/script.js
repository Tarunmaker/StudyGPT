async function startQuiz() {
  const topic = document.getElementById("quizTopic").value;
  const mode = document.getElementById("quizType").value;
  const count = document.getElementById("questionCount").value;

  const quizArea = document.getElementById("quizArea");
  quizArea.innerHTML = "👩‍🏫 Teacher is preparing your test...";

  try {
    const res = await fetch("/quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, mode, count })
    });

    const data = await res.json();
    quizArea.innerHTML = `<pre>${data.quiz}</pre>`;

  } catch {
    quizArea.innerHTML = "❌ Error generating quiz.";
  }
}
