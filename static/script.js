function show(id){
 document.querySelectorAll("section").forEach(s=>s.classList.remove("show"));
 document.getElementById(id).classList.add("show");
}

// ASK
async function askAI(){
 const q=question.value;
 chat.innerHTML+=`<div class='user'>${q}</div>`;
 const r=await fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q})});
 const d=await r.json();
 chat.innerHTML+=`<div class='ai'>${d.answer}</div>`;
}

// QUIZ
async function startQuiz(){
 const r=await fetch("/quiz",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
   topic:quizTopic.value,mode:quizMode.value,count:quizCount.value
 })});
 quizBox.textContent=(await r.json()).quiz;
}

// REAL TEST
let qs=[],i=0,score=0;
async function startRealTest(){
 const r=await fetch("/test",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
   topic:testTopic.value,count:testCount.value
 })});
 qs=JSON.parse((await r.json()).mcqs);
 i=0;score=0;showQ();
}

function showQ(){
 const q=qs[i];
 testBox.innerHTML=`<h3>${q.question}</h3>`+
 q.options.map(o=>`<button onclick="check('${o}','${q.answer}',this)">${o}</button>`).join("");
}

function check(sel,ans,btn){
 btn.style.background=sel==ans?"green":"red";
 if(sel==ans)score++;
 setTimeout(()=>{
   i++;
   if(i<qs.length)showQ();
   else testBox.innerHTML=`<h2>Score: ${score}/${qs.length}</h2>`;
 },700);
}

// PDF
async function pdfTest(){
 const f=new FormData();
 f.append("pdf",pdfFile.files[0]);
 f.append("count",pdfCount.value);
 const r=await fetch("/pdf-test",{method:"POST",body:f});
 pdfOut.textContent=(await r.json()).quiz;
}
