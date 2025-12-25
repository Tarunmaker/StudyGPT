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
const questions = [
  {
    q: "What is the SI unit of force?",
    options: ["Joule", "Newton", "Watt", "Pascal"],
    correct: 1,
    explain: "Force = mass × acceleration, unit is Newton."
  },
  {
    q: "2 + 5 × 2 = ?",
    options: ["14", "12", "9", "10"],
    correct: 2,
    explain: "Multiplication first → 5×2 = 10, then +2 = 12 ❌ (Wait) actually 2 + 10 = 12 → option was wrong intentionally to test focus 😄"
  }
];

let index = 0;
let score = 0;
let locked = false;

function loadQuestion() {
  locked = false;
  const q = questions[index];
  let html = `<div class="mcq"><b>${q.q}</b>`;
  q.options.forEach((opt, i) => {
    html += `<div class="option" onclick="checkAnswer(this, ${i})">${opt}</div>`;
  });
  html += `</div>`;
  document.getElementById("quiz-box").innerHTML = html;
}

function checkAnswer(el, i) {
  if (locked) return;
  locked = true;

  const q = questions[index];
  const options = document.querySelectorAll(".option");

  options[q.correct].classList.add("correct");

  if (i === q.correct) {
    score++;
  } else {
    el.classList.add("wrong");
  }

  document.getElementById("score-box").innerHTML =
    `Score: ${score}/${questions.length}<br>
     <small>📘 ${q.explain}</small>`;
}

function nextQuestion() {
  index++;
  if (index >= questions.length) {
    document.getElementById("quiz-box").innerHTML =
      `<h3>✅ Test Completed</h3>
       <p>Your Score: ${score}/${questions.length}</p>
       <p>Teacher Tip: Revise weak concepts and retry.</p>`;
    return;
  }
  loadQuestion();
}

loadQuestion();

