async function loadCommandCenter() {
  const response = await fetch("./data/command_center_overview.json");
  const data = await response.json();

  const keyCounts = document.querySelector("#key-counts");
  keyCounts.innerHTML = Object.entries(data.key_counts || {})
    .map(([name, value]) => `<div class="metric"><span>${name}</span><strong>${value}</strong></div>`)
    .join("");

  const pipeline = document.querySelector("#pipeline-status");
  pipeline.innerHTML = (data.pipeline_status || [])
    .map((item) => `<tr><td>${item.name}</td><td>${item.status}</td><td>${item.record_count}</td><td>${item.next_step}</td></tr>`)
    .join("");

  const backlog = document.querySelector("#review-backlog");
  backlog.innerHTML = Object.entries(data.review_backlog || {})
    .map(([name, value]) => `<div class="metric"><span>${name}</span><strong>${value}</strong></div>`)
    .join("");

  document.querySelector("#next-actions").innerHTML = (data.next_actions || [])
    .map((item) => `<li>${item}</li>`)
    .join("");

  document.querySelector("#warnings").innerHTML = (data.warnings || [])
    .map((item) => `<li>${item}</li>`)
    .join("") || "<li>目前沒有 warning。</li>";
}

loadCommandCenter().catch((error) => {
  document.querySelector("#warnings").innerHTML = `<li>讀取 command_center_overview.json 失敗：${error.message}</li>`;
});
