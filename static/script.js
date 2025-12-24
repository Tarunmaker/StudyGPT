const chat = document.getElementById("chat");

function show(id){
  document.querySelectorAll(".panel").forEach(p=>p.classList.remove("show"));
  document.getElementById(id).classList.add("show");
  document.querySelectorAll(".nav").forEach(b=>b.classList.remove("active"));
  event.target.classList.add("active");
}

function addMsg(text,type){
  const d=document.createElement("div");
  d.className=`msg ${type}`;
  d.innerHTML=text.replace(/\n/g,"<br>");
  chat.appendChild(d);
  chat.scrollTop=chat.scrollHeight;
}

async function askAI(){
  const q=document.getElementById("question").value.trim();
  if(!q) return;
  document.getElementById("question").value="";
  addMsg(q,"user");
  addMsg("Thinking…","ai");

  const res=await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:q})
  });
  const data=await res.json();
  chat.lastChild.remove();
  addMsg(data.answer || "Error","ai");
}

async function startQuiz(){
  const topic=document.getElementById("topic").value;
  const mode=document.getElementById("mode").value;
  const count=document.getElementById("count").value;
  const box=document.getElementById("quizBox");
  box.textContent="Preparing your practice…";

  const res=await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic,mode,count})
  });
  const data=await res.json();
  box.textContent=data.quiz || data.error;
}
