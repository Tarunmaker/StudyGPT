async function ask(){
  const r = await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({question:q.value})
  });
  const d = await r.json();
  ans.innerHTML = d.answer;
}

async function quiz(){
  const r = await fetch("/quiz",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      topic:topic.value,
      count:count.value
    })
  });
  const d = await r.json();
  quiz.textContent = d.quiz;
}
