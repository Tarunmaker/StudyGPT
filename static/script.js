function toggleTheme(){
 document.body.classList.toggle("dark");
}

async function askAI(){
 answer.innerHTML="Thinking...";
 const r=await fetch("/ask",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({question:question.value})
 });
 const d=await r.json();
 answer.innerHTML=d.answer||d.error;
}

async function generateQuiz(){
 quiz.innerHTML="Generating...";
 const r=await fetch("/quiz",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({topic:topic.value})
 });
 const d=await r.json();
 quiz.innerHTML=d.quiz||d.error;
}

/* REAL TEST */
let qs=[],i=0,score=0,history=JSON.parse(localStorage.getItem("hist")||"[]");

async function startRealTest(){
 testArea.innerHTML="Loading...";
 const r=await fetch("/real-test",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({topic:testTopic.value})
 });
 qs=JSON.parse((await r.json()).questions);
 i=0;score=0;
 showQ();
}

function showQ(){
 const q=qs[i];
 testArea.innerHTML=`<b>Q${i+1}. ${q.q}</b><br>`;
 q.options.forEach(o=>{
  const b=document.createElement("button");
  b.innerText=o;
  b.onclick=()=>check(o,q.answer,b);
  testArea.appendChild(b);
 });
}

function check(s,a,b){
 if(s===a){b.classList.add("correct");score++}
 else b.classList.add("wrong");
 setTimeout(()=>{
  i++;
  if(i<qs.length)showQ();
  else finish();
 },700);
}

function finish(){
 const acc=Math.round(score/qs.length*100);
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
