function toggleTheme(){
  document.body.classList.toggle("dark");
}

async function askAI(){
  answer.innerHTML="Thinking...";
  const res = await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:question.value})
  });
  const data = await res.json();
  answer.innerHTML = data.answer || data.error;
}

async function generateQuiz(){
  quiz.innerHTML="Generating...";
  const res = await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:topic.value})
  });
  const data = await res.json();
  quiz.innerHTML = data.quiz || data.error;
}

async function pdfTest(){
  const f = pdfFile.files[0];
  if(!f) return;

  const fd = new FormData();
  fd.append("pdf", f);

  pdfOut.innerHTML="Processing...";
  const res = await fetch("/pdf-test",{method:"POST",body:fd});
  const data = await res.json();
  pdfOut.innerHTML = data.quiz || data.error;
}

async function loadDashboard(){
  const res = await fetch("/dashboard");
  const d = await res.json();
  dash.innerHTML = `
    Questions Asked: ${d.questions}<br>
    Quizzes Taken: ${d.quizzes}<br>
    PDF Tests: ${d.pdf_tests}
  `;
}
