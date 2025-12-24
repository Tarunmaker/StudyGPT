async function askAI() {
  const q = question.value;
  answer.innerHTML = "Thinking...";
  const r = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({question:q})
  });
  const d = await r.json();
  answer.innerHTML = d.answer || d.error;
}

async function generateQuiz() {
  quiz.innerHTML = "Generating...";
  const r = await fetch("/quiz", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({question:topic.value})
  });
  const d = await r.json();
  quiz.innerHTML = d.answer;
}

async function startTest() {
  testBox.innerHTML = "Loading test...";
  const r = await fetch("/test", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({topic:testTopic.value})
  });
  const d = await r.json();
  const data = JSON.parse(d.test);

  let score = 0;
  testBox.innerHTML = "";

  data.forEach((q,i)=>{
    const div = document.createElement("div");
    div.innerHTML = `<b>Q${i+1}. ${q.q}</b>`;
    q.options.forEach(opt=>{
      const o = document.createElement("div");
      o.className="option";
      o.innerText=opt;
      o.onclick=()=>{
        if(opt===q.answer){
          o.classList.add("correct"); score++;
        } else o.classList.add("wrong");
      };
      div.appendChild(o);
    });
    testBox.appendChild(div);
  });

  setTimeout(()=>{
    alert("Test finished! Score: "+score+"/"+data.length);
  },500);
}
