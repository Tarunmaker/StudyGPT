 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/static/community.js b/static/community.js
new file mode 100644
index 0000000000000000000000000000000000000000..5c9b4ee09a52e1509cdfbcad3c7c350f6ef3193f
--- /dev/null
+++ b/static/community.js
@@ -0,0 +1,67 @@
+let replyState = null;
+
+function formatMessage(text) {
+    return text
+        .replace(/(@[\\w]+)/g, '<span class="mention">$1</span>')
+        .replace(/(#[\\w]+)/g, '<span class="tag">$1</span>');
+}
+
+function setReply(user, text) {
+    replyState = { user, text };
+    const preview = document.getElementById("reply-preview");
+    document.getElementById("reply-user").innerText = user;
+    document.getElementById("reply-text").innerText = text;
+    preview.classList.remove("hidden");
+}
+
+function clearReply() {
+    replyState = null;
+    const preview = document.getElementById("reply-preview");
+    preview.classList.add("hidden");
+}
+
+function upvoteMessage(button) {
+    const countSpan = button.querySelector("span");
+    if (!countSpan) {
+        return;
+    }
+    const current = Number(countSpan.innerText) || 0;
+    countSpan.innerText = current + 1;
+}
+
+function markBestAnswer(button) {
+    const bubble = button.closest(".message.bubble");
+    if (!bubble) {
+        return;
+    }
+    const current = document.querySelector(".best-answer");
+    if (current) {
+        current.classList.remove("best-answer");
+    }
+    bubble.classList.add("best-answer");
+}
+
+function sendCommunityMessage() {
+    const input = document.getElementById("chat-input");
+    const messages = document.getElementById("chat-messages");
+    if (!input || !messages || !input.value.trim()) {
+        return;
+    }
+    const row = document.createElement("div");
+    row.className = "chat-row self";
+    const message = document.createElement("div");
+    message.className = "message bubble self";
+    const replyHtml = replyState
+        ? `<div class="reply-quote"><span>Replying to ${replyState.user}</span><p>${replyState.text}</p></div>`
+        : "";
+    message.innerHTML = `${replyHtml}<div class="meta"><span class="user">You</span><span class="time">Now</span></div><p>${formatMessage(input.value.trim())}</p>`;
+    const actions = document.createElement("div");
+    actions.className = "message-actions";
+    actions.innerHTML = '<button onclick="upvoteMessage(this)">👍 <span>0</span></button><button onclick="markBestAnswer(this)">⭐ Best</button>';
+    message.appendChild(actions);
+    row.appendChild(message);
+    messages.appendChild(row);
+    input.value = "";
+    messages.scrollTop = messages.scrollHeight;
+    clearReply();
+}
 
EOF
)
