async function askAI() {
  const q = question.value.trim();
  if (!q) return;
  answer.innerHTML = "Thinking...";

  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ question: q })
  });
  const data = await res.json();
  answer.innerHTML = data.answer || data.error;
}

async function generateQuiz() {
  quiz.innerHTML = "Generating quiz...";
  const res = await fetch("/quiz", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ topic: topic.value })
  });
  const data = await res.json();
  quiz.innerHTML = data.quiz || data.error;
}

async function summarizeNotes() {
  summary.innerHTML = "Summarizing...";
  const res = await fetch("/summarize", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ text: notes.value })
  });
  const data = await res.json();
  summary.innerHTML = data.summary || data.error;
}
let questions=[], idx=0, score=0;

async function startTest(){
  testBox.innerHTML="Loading test...";
  const res = await fetch("/test",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:testTopic.value})
  });
  const data = await res.json();
  questions = JSON.parse(data.test);
  idx=0; score=0;
  showQ();
}

function showQ(){
  const q = questions[idx];
  testBox.innerHTML = `<b>Q${idx+1}. ${q.q}</b><br>`;
  q.options.forEach(opt=>{
    const btn=document.createElement("button");
    btn.innerText=opt;
    btn.onclick=()=>check(opt,q.answer,btn);
    testBox.appendChild(btn);
  });
}

function check(sel,ans,btn){
  if(sel===ans){
    btn.style.background="green"; score++;
  } else {
    btn.style.background="red";
  }
  setTimeout(()=>{
    idx++;
    if(idx<questions.length) showQ();
    else testBox.innerHTML=`✅ Score: ${score}/${questions.length}`;
  },700);
}
