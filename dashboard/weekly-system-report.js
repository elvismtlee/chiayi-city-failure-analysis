async function loadWeeklySystemReport() {
  const response = await fetch("./data/weekly_system_report.json");
  const data = await response.json();

  document.querySelector("#week-range").textContent = `${data.week_start || ""} 到 ${data.week_end || ""}`;
  document.querySelector("#system-status").textContent = `system_status: ${data.system_status || "unknown"}`;

  const renderMetrics = (selector, values) => {
    document.querySelector(selector).innerHTML = Object.entries(values || {})
      .map(([name, value]) => `<div class="metric"><span>${name}</span><strong>${value}</strong></div>`)
      .join("");
  };
  renderMetrics("#pipeline-summary", data.pipeline_summary);
  renderMetrics("#review-backlog-summary", data.review_backlog_summary);
  renderMetrics("#completed-outputs", data.completed_outputs);

  document.querySelector("#warnings").innerHTML = (data.warnings || [])
    .map((item) => `<li>${item}</li>`)
    .join("") || "<li>目前沒有 warning。</li>";
  document.querySelector("#recommended-next-actions").innerHTML = (data.recommended_next_actions || [])
    .map((item) => `<li>${item}</li>`)
    .join("");
}

loadWeeklySystemReport().catch((error) => {
  document.querySelector("#warnings").innerHTML = `<li>讀取 weekly_system_report.json 失敗：${error.message}</li>`;
});
