function toggleMode(){
 document.body.classList.toggle("dark");
}

async function askAI(){
 answer.innerText="Thinking...";
 const r=await fetch("/ask",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({question:question.value})
 });
 const d=await r.json();
 answer.innerText=d.answer;
}

let qs=[],i=0,score=0;

async function startTest(){
 const r=await fetch("/test",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({topic:topic.value})
 });
 qs=JSON.parse((await r.json()).test);
 i=0;score=0;
 showQ();
}

function showQ(){
 const q=qs[i];
 testBox.innerHTML=`<b>${q.q}</b><br>`+
 q.options.map(o=>`<button onclick="check('${o}','${q.answer}',this)">${o}</button>`).join("");
}

function check(sel,ans,btn){
 btn.style.background=sel===ans?"green":"red";
 if(sel===ans)score++;
 setTimeout(()=>{
  i++;
  if(i<qs.length)showQ();
  else testBox.innerHTML=`Score: ${score}/${qs.length}`;
 },700);
}
