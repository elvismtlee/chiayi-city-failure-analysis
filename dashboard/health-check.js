async function loadHealthCheck() {
  const response = await fetch("./data/dashboard_health_check.json");
  const data = await response.json();

  document.querySelector("#status").textContent = data.status || "unknown";
  document.querySelector("#checked-count").textContent = `checked_files: ${(data.checked_files || []).length}`;

  const renderList = (selector, items) => {
    document.querySelector(selector).innerHTML = (items || []).map((item) => `<li>${item}</li>`).join("") || "<li>無</li>";
  };
  renderList("#missing-files", data.missing_files);
  renderList("#empty-files", data.empty_files);
  renderList("#invalid-json-files", data.invalid_json_files);
  renderList("#warnings", data.warnings);

  document.querySelector("#page-checks").innerHTML = (data.page_checks || [])
    .map((item) => `<tr><td>${item.page}</td><td>${item.exists}</td><td>${item.empty}</td></tr>`)
    .join("");

  document.querySelector("#nav-checks").innerHTML = (data.nav_checks || [])
    .map((item) => `<tr><td>${item.name}</td><td>${item.in_site_map}</td><td>${item.in_shared_nav}</td></tr>`)
    .join("");
}

loadHealthCheck().catch((error) => {
  document.querySelector("#warnings").innerHTML = `<li>讀取 dashboard_health_check.json 失敗：${error.message}</li>`;
});
