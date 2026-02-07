 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/static/profile.js b/static/profile.js
new file mode 100644
index 0000000000000000000000000000000000000000..8bc59125e176060e7cad6a0b6b045ce9b09de7ef
--- /dev/null
+++ b/static/profile.js
@@ -0,0 +1,88 @@
+const progressState = {
+    streak: 0,
+    topics: [],
+    accuracy: 0
+};
+
+function loadProgress() {
+    const stored = localStorage.getItem("progressState");
+    if (stored) {
+        const parsed = JSON.parse(stored);
+        progressState.streak = parsed.streak || 0;
+        progressState.topics = parsed.topics || [];
+        progressState.accuracy = parsed.accuracy || 0;
+    }
+    updateProgressView();
+}
+
+function saveProgress() {
+    localStorage.setItem("progressState", JSON.stringify(progressState));
+}
+
+function updateProgressView() {
+    const streakEl = document.getElementById("streak-count");
+    if (streakEl) {
+        streakEl.innerText = `${progressState.streak} days`;
+    }
+    const topicList = document.getElementById("topic-list");
+    if (topicList) {
+        topicList.innerHTML = progressState.topics.map(topic => `<li>${topic}</li>`).join("");
+    }
+    const accuracyDisplay = document.getElementById("accuracy-display");
+    if (accuracyDisplay) {
+        accuracyDisplay.innerText = `${progressState.accuracy}%`;
+    }
+    const topicCount = document.getElementById("topic-count");
+    if (topicCount) {
+        topicCount.innerText = progressState.topics.length;
+    }
+    updateReadiness();
+}
+
+function updateReadiness() {
+    const readinessScore = Math.min(
+        100,
+        Math.round(progressState.streak * 2 + progressState.topics.length * 3 + progressState.accuracy * 0.4)
+    );
+    const scoreEl = document.getElementById("readiness-score");
+    const fillEl = document.getElementById("readiness-fill");
+    if (scoreEl) {
+        scoreEl.innerText = `${readinessScore}%`;
+    }
+    if (fillEl) {
+        fillEl.style.width = `${readinessScore}%`;
+    }
+}
+
+function markStudyDone() {
+    progressState.streak += 1;
+    saveProgress();
+    updateProgressView();
+}
+
+function addTopic() {
+    const input = document.getElementById("topic-input");
+    if (!input || !input.value.trim()) {
+        return;
+    }
+    progressState.topics.push(input.value.trim());
+    input.value = "";
+    saveProgress();
+    updateProgressView();
+}
+
+function saveAccuracy() {
+    const input = document.getElementById("accuracy-input");
+    if (!input) {
+        return;
+    }
+    const value = Number(input.value);
+    if (Number.isNaN(value) || value < 0 || value > 100) {
+        return;
+    }
+    progressState.accuracy = value;
+    saveProgress();
+    updateProgressView();
+}
+
+document.addEventListener("DOMContentLoaded", loadProgress);
 
EOF
)
