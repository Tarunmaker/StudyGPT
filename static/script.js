let mode = "normal";

function setMode(m) {
  mode = m;
  document.querySelectorAll(".mode-bar button")
    .forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");
}

async function send() {
  const input = document.getElementById("question");
  const chat = document.getElementById("chat");
  const text = input.value.trim();
  if (!text) return;

  chat.innerHTML += `<div class="msg user">${text}</div>`;
  input.value = "";

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: text, mode })
  });

  const data = await res.json();

  if (data.answer) {
    chat.innerHTML += `<div class="msg ai">${data.answer.replace(/\n/g,"<br>")}</div>`;
    chat.scrollTop = chat.scrollHeight;
  }
}
