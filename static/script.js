const chat = document.getElementById("chat");
let examTopic = "";
let lastExamAnswer = "";

function addMsg(text, cls){
  const div = document.createElement("div");
  div.className = "msg " + cls;
  div.innerText = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// 1️⃣ Ask AI
async function sendAsk(){
  const input = document.getElementById("input");
  const text = input.value.trim();
  if(!text) return;

  addMsg(text, "user");
  input.value = "";

  const res = await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({message:text})
  });
  const data = await res.json();
  addMsg(data.reply, "ai");
}

// 2️⃣ Quiz Mode
async function startQuiz(){
  const t = document.getElementById("topic").value;
  if(!t) return;

  addMsg("📝 Quiz on: " + t, "ai");

  const res = await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:t})
  });
  const data = await res.json();
  addMsg(data.result, "ai");
}

// 3️⃣ Exam / Focus Mode
async function startExam(){
  examTopic = document.getElementById("topic").value;
  lastExamAnswer = "";

  addMsg("🎯 Exam mode started. Focus.", "ai");

  const res = await fetch("/exam",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:examTopic})
  });
  const data = await res.json();
  addMsg(data.reply, "ai");
}
 history.push({score,acc,date:new Date().toLocaleString()});
 localStorage.setItem("hist",JSON.stringify(history));
 testArea.innerHTML=`Score: ${score}/${qs.length}<br>Accuracy: ${acc}%`;
}

function showHistory(){
 historyBox.innerHTML=history.length
 ? history.map(h=>`${h.date}<br>Score:${h.score} Accuracy:${h.acc}%<hr>`).join("")
 : "No history";
}

async function pdfTest(){
 const f=pdfFile.files[0];
 if(!f)return;
 const fd=new FormData();
 fd.append("pdf",f);
 pdfOut.innerHTML="Processing...";
 const r=await fetch("/pdf-test",{method:"POST",body:fd});
 const d=await r.json();
 pdfOut.innerHTML=d.quiz||d.error;
}
