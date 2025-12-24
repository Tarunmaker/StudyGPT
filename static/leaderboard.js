fetch("/leaderboard-data")
.then(r=>r.json())
.then(d=>{
  d.forEach(s=>{
    board.innerHTML += `
      <tr>
        <td>${s.rank}</td>
        <td>${s.name}</td>
        <td>${s.level}</td>
        <td>${s.xp}</td>
      </tr>`;
  });
});
