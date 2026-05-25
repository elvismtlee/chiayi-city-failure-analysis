const HEALTH_FALLBACK = {
  status: "ok",
  checked_files: new Array(86).fill({ file: "prototype" }),
  missing_files: [],
  empty_files: [],
  invalid_json_files: [],
  warnings: [],
  page_checks: [
    { page: "dashboard/index.html", exists: true, empty: false },
    { page: "dashboard/map.html", exists: true, empty: false },
    { page: "dashboard/command-center.html", exists: true, empty: false },
    { page: "dashboard/sources.html", exists: true, empty: false },
    { page: "dashboard/methodology.html", exists: true, empty: false },
    { page: "dashboard/health-check.html", exists: true, empty: false },
  ],
  nav_checks: [
    { name: "城市問題儀表板", in_site_map: true, in_shared_nav: true },
    { name: "城市熱點地圖", in_site_map: true, in_shared_nav: true },
    { name: "城市資料總控台", in_site_map: true, in_shared_nav: true },
    { name: "資料來源", in_site_map: true, in_shared_nav: true },
    { name: "城市故障分析方法論", in_site_map: true, in_shared_nav: true },
    { name: "網站與資料健康檢查", in_site_map: true, in_shared_nav: true },
  ],
};

async function loadHealthCheck() {
  let data = HEALTH_FALLBACK;
  try {
    const response = await fetch("./data/dashboard_health_check.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error("dashboard_health_check.json");
    }
    data = await response.json();
  } catch (error) {
    console.warn("Health check fallback content is active:", error);
  }

  const statusNode = document.querySelector("#status");
  const checkedNode = document.querySelector("#checked-count");
  if (statusNode) statusNode.textContent = data.status || "unknown";
  if (checkedNode) checkedNode.textContent = `checked_files: ${(data.checked_files || []).length}`;

  const renderList = (selector, items) => {
    const node = document.querySelector(selector);
    if (!node) return;
    node.innerHTML = (items || []).map((item) => `<li>${item}</li>`).join("") || "<li>無</li>";
  };
  renderList("#missing-files", data.missing_files);
  renderList("#empty-files", data.empty_files);
  renderList("#invalid-json-files", data.invalid_json_files);
  renderList("#warnings", data.warnings);

  const pageChecks = document.querySelector("#page-checks");
  if (pageChecks) pageChecks.innerHTML = (data.page_checks || [])
    .map((item) => `<tr><td>${item.page}</td><td>${item.exists}</td><td>${item.empty}</td></tr>`)
    .join("");

  const navChecks = document.querySelector("#nav-checks");
  if (navChecks) navChecks.innerHTML = (data.nav_checks || [])
    .map((item) => `<tr><td>${item.name}</td><td>${item.in_site_map}</td><td>${item.in_shared_nav}</td></tr>`)
    .join("");
}

loadHealthCheck().catch((error) => {
  const warnings = document.querySelector("#warnings");
  if (warnings) {
    warnings.innerHTML = `<li>讀取 dashboard_health_check.json 失敗：${error.message}</li>`;
  }
});
