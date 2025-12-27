function switchMode(mode) {
  document.querySelectorAll(".mode").forEach(m => m.classList.add("hidden"));
  document.getElementById(mode).classList.remove("hidden");

  document.querySelectorAll(".modes button").forEach(b => b.classList.remove("active"));
  event.target.classList.add("active");
}

function check(btn, correct) {
  document.querySelectorAll(".options button").forEach(b => b.disabled = true);

  if (correct) {
    btn.classList.add("correct");
    feedback.innerText = "✔ Correct! Electrostatic force acts between charges.";
  } else {
    btn.classList.add("wrong");
    feedback.innerText = "❌ Incorrect. Correct answer is Electrostatic force.";
  }
}
