async function askAI() {
  const q = document.getElementById("question").value;
  const box = document.getElementById("answer");
  box.innerHTML = "Thinking…";

  try {
    const r = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ question: q })
    });
    const d = await r.json();
    box.innerHTML = d.answer || d.error;
  } catch {
    box.innerHTML = "Server error";
  }
}

async function startTest() {
  const topic = document.getElementById("topic").value;
  const count = document.getElementById("count").value;
  const box = document.getElementById("test");
  box.innerHTML = "Generating test…";

  try {
    const r = await fetch("/test", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ topic, count })
    });
    const d = await r.json();
    box.innerHTML = d.test || d.error;
  } catch {
    box.innerHTML = "Server error";
  }
}
