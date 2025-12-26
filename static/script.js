async function askAI() {
  const chat = document.getElementById("chat");
  const q = question.value;
  if (!q) return;

  chat.innerHTML += `<div class="msg user">${q}</div>`;
  question.value = "";

  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({question:q})
  });
  const data = await res.json();
  chat.innerHTML += `<div class="msg ai">${data.answer}</div>`;
  chat.scrollTop = chat.scrollHeight;
}

async function startQuiz() {
  const t = topic.value;
  const chat = document.getElementById("chat");

  const res = await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:t})
  });
  const data = await res.json();
  chat.innerHTML += `<div class="msg ai">${data.result}</div>`;
}

async function startExam() {
  const t = topic.value;
  const chat = document.getElementById("chat");

  const res = await fetch("/exam",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:t})
  });
  const data = await res.json();
  chat.innerHTML += `<div class="msg ai">${data.result}</div>`;
}
