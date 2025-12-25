async function askAI() {
  const input = document.getElementById("question");
  const chat = document.getElementById("chat");
  const text = input.value.trim();
  if (!text) return;

  // User message
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.style.background = "#19c37d";
  userMsg.style.color = "#000";
  userMsg.style.alignSelf = "flex-end";
  userMsg.innerText = text;
  chat.appendChild(userMsg);

  input.value = "";

  // AI placeholder
  const aiMsg = document.createElement("div");
  aiMsg.className = "message ai";
  aiMsg.innerText = "Thinking...";
  chat.appendChild(aiMsg);

  chat.scrollTop = chat.scrollHeight;

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: text })
  });

  const data = await res.json();
  aiMsg.innerText = data.answer;

  chat.scrollTop = chat.scrollHeight;
}
