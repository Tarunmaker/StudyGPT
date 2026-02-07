async function askAI() {
    const q = document.getElementById("question").value;
    const res = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({question: q})
    });
    const data = await res.json();
    document.getElementById("answer").innerText = data.answer;
    }
    async function analyzePYQ() {
    const fileInput = document.getElementById("pyq-file");
    const result = document.getElementById("pyq-result");
    if (!fileInput.files.length) {
        result.innerText = "Please upload a PYQ text file first.";
        return;
    }
    const formData = new FormData();
    if (fileInput.files.length > 0) {
        formData.append("file", fileInput.files[0]);
    }
    const res = await fetch("/pyq", {
        method: "POST",
        body: formData
    });
    const data = await res.json();
    if (data.questions && data.questions.length) {
        const items = data.questions.map(q => `<li>${q}</li>`).join("");
        result.innerHTML = `<strong>${data.analysis}</strong><ul>${items}</ul>`;
    } else {
        result.innerText = data.analysis;
    }
}

async function showHeatmap() {
    const fileInput = document.getElementById("pyq-file");
    const container = document.getElementById("pyq-heatmap");
    if (!fileInput.files.length) {
        container.innerText = "Upload a PYQ file to view the topic heatmap.";
        return;
    }
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    const res = await fetch("/pyq", {
        method: "POST",
        body: formData
    });
    const data = await res.json();
    if (!data.topic_counts || !data.topic_counts.length) {
        container.innerText = "No topics found to display.";
        return;
    }
    const maxCount = Math.max(...data.topic_counts.map(item => item.count));
    const bars = data.topic_counts.map(item => {
        const width = Math.round((item.count / maxCount) * 100);
        return `<div class="heatmap-row"><span>${item.topic}</span><div class="heatmap-bar"><div style="width:${width}%"></div></div><span class="heatmap-count">${item.count}</span></div>`;
    }).join("");
    container.innerHTML = `<h4>Topic Heatmap</h4>${bars}`;
}

async function downloadMockQuestions() {
    const fileInput = document.getElementById("pyq-file");
    const result = document.getElementById("pyq-result");
    if (!fileInput.files.length) {
        result.innerText = "Please upload a PYQ text file first.";
        return;
    }
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    const res = await fetch("/pyq/mock-pdf", {
        method: "POST",
        body: formData
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "mock-questions.pdf";
    link.click();
    window.URL.revokeObjectURL(url);
}

async function generateStrategy() {
    const examDate = document.getElementById("exam-date").value;
    const hours = document.getElementById("study-hours").value;
    const result = document.getElementById("strategy-result");
    const res = await fetch("/strategy", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({examDate, hours})
    });
    const data = await res.json();
    const planItems = data.plan.map(item => `<li>${item}</li>`).join("");
    const checklistItems = data.checklist.map(item => `<li>${item}</li>`).join("");
    result.innerHTML = `<strong>${data.summary}</strong><div class="plan-grid"><div><h4>Plan</h4><ul>${planItems}</ul></div><div><h4>Daily Checklist</h4><ul>${checklistItems}</ul></div></div>`;
}

let focusActive = false;

async function startFocusMode() {
    const topic = document.getElementById("focus-topic").value;
    const status = document.getElementById("focus-status");
    const questionsContainer = document.getElementById("focus-questions");
    if (!topic) {
        status.innerText = "Please enter a topic to start focus mode.";
        return;
    }
    const res = await fetch("/focus-test", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({topic})
    });
    const data = await res.json();
    const items = data.questions.map(item => `<li>${item}</li>`).join("");
    questionsContainer.innerHTML = `<ol>${items}</ol>`;
    status.innerText = "Focus sprint is on. Stay on this tab to continue.";
    focusActive = true;
    document.body.classList.add("focus-active");
    const main = document.querySelector("main");
    if (main && main.requestFullscreen) {
        main.requestFullscreen().catch(() => {});
    }
}

function endFocusMode() {
    focusActive = false;
    document.body.classList.remove("focus-active");
    document.getElementById("focus-status").innerText = "Focus sprint is off.";
    document.getElementById("focus-overlay").classList.add("hidden");
    if (document.fullscreenElement) {
        document.exitFullscreen().catch(() => {});
    }
    window.location.href = "/profile";
}

function resumeFocus() {
    if (focusActive) {
        document.getElementById("focus-overlay").classList.add("hidden");
    }
}

document.addEventListener("visibilitychange", () => {
    if (focusActive && document.hidden) {
        document.getElementById("focus-overlay").classList.remove("hidden");
    }
});

async function generateQuiz() {
    const topic = document.getElementById("topic").value;
    const res = await fetch("/quiz", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({topic})
    });
    const data = await res.json();
    document.getElementById("answer").innerText = data.quiz;
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
}