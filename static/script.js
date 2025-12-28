function renderHistory(items) {
    const box = document.getElementById("history");
    box.innerHTML = "";
    items.forEach(h => {
        box.innerHTML += `
        <div class="history-item">
            <b>Q:</b> ${h.question}<br>
            <b>A:</b> ${h.answer}
        </div>`;
    });
}

async function askAI() {
    const q = document.getElementById("question").value;
    const res = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: q})
    });
    const data = await res.json();
    document.getElementById("answer").innerText = data.answer;
    renderHistory(data.history);
}

async function generateQuiz() {
    const topic = document.getElementById("topic").value;
    const res = await fetch("/quiz", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({topic})
    });
    const data = await res.json();
    document.getElementById("answer").innerText = data.quiz;
    renderHistory(data.history);
}

async function summarizeNotes() {
    const text = document.getElementById("notes").value;
    const res = await fetch("/summarize", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });
    const data = await res.json();
    document.getElementById("answer").innerText = data.summary;
    renderHistory(data.history);
}
