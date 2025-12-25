let QUESTIONS = []
let ANSWERS = []

function askAI(){
 fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({question:question.value})})
 .then(r=>r.json()).then(d=>answer.innerHTML=d.answer)
}

function startTest(){
 fetch("/generate-test",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({topic:topic.value,count:count.value})})
 .then(r=>r.json()).then(q=>{
   QUESTIONS=q; ANSWERS=[]
   test.innerHTML=""
   q.forEach((x,i)=>{function toggleDark(){
  document.body.classList.toggle("dark");
}

async function askAI(){
  answer.innerHTML = "Thinking...";
  const res = await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:question.value})
  });
  const data = await res.json();
  answer.innerHTML = data.answer;
}

async function summarizeNotes(){
  summary.innerHTML = "Summarizing...";
  const res = await fetch("/summarize",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({text:notes.value})
  });
  const data = await res.json();
  summary.innerHTML = data.summary;
}

async function startQuiz(){
  quizResult.innerHTML = "Preparing quiz...";
  const res = await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:quizTopic.value})
  });
  const data = await res.json();
  quizResult.innerHTML = data.result;
}

async function startExam(){
  examResult.innerHTML = "Entering focus mode...";
  const res = await fetch("/exam",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({topic:examTopic.value})
  });
  const data = await res.json();
  examResult.innerHTML = data.result;
}

     let div=document.createElement("div")
     div.innerHTML=`<p>${x.q}</p>`
     x.options.forEach((o,j)=>{
       let b=document.createElement("button")
       b.innerText=o
       b.onclick=()=>{ANSWERS[i]=j; b.style.background="orange"}
       div.appendChild(b)
     })
     test.appendChild(div)
   })
   let s=document.createElement("button")
   s.innerText="Submit Test"
   s.onclick=submitTest
   test.appendChild(s)
 })async function askAI(){
  answer.innerHTML = "Thinking...";
  const res = await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:question.value})
  });
  const data = await res.json();
  answer.innerHTML = data.answer;
}

async function generateQuiz(){
  quiz.innerHTML = "Generating quiz...";
  const res = await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:quizTopic.value})
  });
  const data = await res.json();
  quiz.innerHTML = data.answer;
}

async function summarizeNotes(){
  summary.innerHTML = "Summarizing...";
  const res = await fetch("/summarize",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({text:notes.value})
  });
  const data = await res.json();
  summary.innerHTML = data.summary;
}

}

function submitTest(){
 fetch("/submit-test",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({questions:QUESTIONS,answers:ANSWERS})})
 .then(r=>r.json()).then(d=>{
   alert(`Score: ${d.score} | ${d.percent}%`)
 })
}
