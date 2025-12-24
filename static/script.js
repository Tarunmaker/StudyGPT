async function askAI() {
  const q = question.value;
  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({question: q})
  });
  const d = await res.json();
  answer.innerHTML = d.answer.replace(/\n/g,"<br>");
}

async function summarizeNotes() {
  const res = await fetch("/summarize", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({text:notes.value})
  });
  const d = await res.json();
  summary.innerHTML = d.summary.replace(/\n/g,"<br>");
}

async function startQuiz() {
  const res = await fetch("/quiz", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      topic:quizTopic.value,
      mode:quizType.value,
      count:questionCount.value
    })
  });
  const d = await res.json();
  quizArea.textContent = d.quiz;
}

async function generatePdfTest() {
  const f = pdfFile.files[0];
  const form = new FormData();
  form.append("pdf", f);
  form.append("mode", pdfMode.value);
  form.append("count", pdfCount.value);

  const res = await fetch("/pdf-test", {method:"POST", body:form});
  const d = await res.json();
  pdfQuiz.textContent = d.quiz || d.error;
}

async function analyze() {
  const res = await fetch("/analyze-result", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      total:totalQ.value,
      correct:correctQ.value
    })
  });
  const d = await res.json();
  resultBox.textContent =
    `Score: ${d.correct}/${d.total}\n` +
    `Percentage: ${d.percentage}%\n` +
    `Feedback: ${d.feedback}`;
}
