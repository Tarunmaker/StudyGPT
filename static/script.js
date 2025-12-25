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
   q.forEach((x,i)=>{
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
 })
}

function submitTest(){
 fetch("/submit-test",{method:"POST",headers:{"Content-Type":"application/json"},
 body:JSON.stringify({questions:QUESTIONS,answers:ANSWERS})})
 .then(r=>r.json()).then(d=>{
   alert(`Score: ${d.score} | ${d.percent}%`)
 })
}
