const PUBLIC_DASHBOARD_FALLBACK_SUMMARY = {
  total_cases: 12458,
  total_questions: 386,
  total_hotspots: 18,
  top_issue: "交通",
  updated_at: "2026-05-21"
};

const PUBLIC_DASHBOARD_FALLBACK_INVENTORY = {
  total_count: 29
};

const PUBLIC_DASHBOARD_FALLBACK_HEALTH = {
  status: "ok",
  warnings: [],
  missing_files: []
};

const PUBLIC_DASHBOARD_FALLBACK_ISSUES = [
  { display_name: "交通停車", current_count: 92, confidence: 0.66, review_status: "prototype", recommended_action: "補足道路與停車議題欄位，讓交通壓力能持續追蹤。", window_days: 90 },
  { display_name: "市場商圈", current_count: 78, confidence: 0.61, review_status: "prototype", recommended_action: "補足商圈周邊樣本，持續整理市場周邊動線與環境議題。", window_days: 90 },
  { display_name: "環境衛生", current_count: 71, confidence: 0.58, review_status: "prototype", recommended_action: "補齊環境清潔與垃圾動線資料，建立更穩定的環境類趨勢。", window_days: 90 },
  { display_name: "通學安全", current_count: 64, confidence: 0.57, review_status: "prototype", recommended_action: "補齊學校周邊風險樣本，建立通學安全熱點追蹤。", window_days: 90 },
  { display_name: "人行安全", current_count: 52, confidence: 0.55, review_status: "prototype", recommended_action: "補足步道、人行空間與通行衝突樣本，讓人行安全分類更穩定。", window_days: 90 }
];

const PUBLIC_DASHBOARD_FALLBACK_HOTSPOTS = [
  {
    name: "文化路商圈",
    category: "停車 / 人行",
    department: "交通處",
    score: 92,
    action: "商圈動線與停車熱點專案"
  },
  {
    name: "市場周邊",
    category: "垃圾 / 動線",
    department: "環保局 / 建設處",
    score: 78,
    action: "市場周邊環境改善與卸貨規劃"
  },
  {
    name: "學校周邊",
    category: "通學安全",
    department: "交通處 / 教育處",
    score: 71,
    action: "通學步道與接送區改善"
  }
];

function safeText(value, fallback = "") {
  if (value === undefined || value === null || value === "") return fallback;
  return String(value);
}

function formatNumber(value) {
  if (typeof value !== "number" || Number.isNaN(value)) {
    return safeText(value, "0");
  }
  return new Intl.NumberFormat("zh-TW").format(value);
}

async function loadJson(path, fallback) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Failed to load ${path}`);
    return await response.json();
  } catch (error) {
    return fallback;
  }
}

function renderHomepageKpis(summary, inventory, health) {
  const target = document.getElementById("kpiGrid");
  if (!target) return;

  const totalCases = Number(summary?.total_cases ?? PUBLIC_DASHBOARD_FALLBACK_SUMMARY.total_cases);
  const totalQuestions = Number(summary?.total_questions ?? PUBLIC_DASHBOARD_FALLBACK_SUMMARY.total_questions);
  const totalHotspots = Number(summary?.total_hotspots ?? PUBLIC_DASHBOARD_FALLBACK_SUMMARY.total_hotspots);
  const topIssue = safeText(summary?.top_issue, PUBLIC_DASHBOARD_FALLBACK_SUMMARY.top_issue);
  const totalSources = Number(inventory?.total_count ?? PUBLIC_DASHBOARD_FALLBACK_INVENTORY.total_count);
  const statusOk = safeText(health?.status, "ok") === "ok";

  const kpis = [
    {
      label: "原型案件數",
      value: formatNumber(totalCases),
      desc: "作為原型儀表板的總案件量級指標。",
      source: "source: dashboard_summary.json"
    },
    {
      label: "質詢紀錄數",
      value: formatNumber(totalQuestions),
      desc: "對照地方議題分類與城市問題脈絡。",
      source: "source: dashboard_summary.json"
    },
    {
      label: "城市熱點",
      value: formatNumber(totalHotspots),
      desc: "目前熱點總數，用來標示需要優先看的區位。",
      source: "source: dashboard_summary.json"
    },
    {
      label: "最大議題",
      value: topIssue,
      desc: "目前原型資料中最常出現的城市議題。",
      source: "source: dashboard_summary.json"
    },
    {
      label: "官方資料源",
      value: formatNumber(totalSources),
      desc: "已盤點的官方資料來源數量。",
      source: "source: open_data_url_inventory.json"
    },
    {
      label: "上線狀態",
      value: statusOk ? "Ready" : "Prototype",
      desc: "首頁與 GitHub Pages 已可展示，但資料仍屬 prototype。",
      source: "source: dashboard_health_check.json"
    }
  ];

  target.innerHTML = kpis.map((item) => `
    <article class="kpi-card">
      <span class="kpi-label">${item.label}</span>
      <div class="kpi-value">${item.value}</div>
      <div class="kpi-desc">${item.desc}</div>
      <span class="kpi-source">${item.source}</span>
    </article>
  `).join("");
}

function renderIssueRanking(trends) {
  const target = document.getElementById("issueBars");
  if (!target) return;

  const items = Array.isArray(trends) ? trends : [];
  const from90Days = items.filter((item) => Number(item.window_days) === 90);
  const chosen = (from90Days.length ? from90Days : PUBLIC_DASHBOARD_FALLBACK_ISSUES)
    .slice()
    .sort((a, b) => Number(b.current_count || 0) - Number(a.current_count || 0))
    .slice(0, 5);

  const maxCount = Math.max(...chosen.map((item) => Number(item.current_count || 0)), 1);
  target.innerHTML = chosen.map((item) => {
    const count = Number(item.current_count || 0);
    const width = Math.max(16, Math.round((count / maxCount) * 100));
    return `
      <div class="bar-row">
        <div>
          <div class="bar-meta">
            <span class="bar-name">${safeText(item.display_name, "未分類")}</span>
            <span>confidence ${Number(item.confidence || 0).toFixed(2)}</span>
          </div>
          <div class="bar-note">review_status: ${safeText(item.review_status, "prototype")} ｜ ${safeText(item.recommended_action, "持續補充樣本後再更新趨勢。")}</div>
        </div>
        <div class="bar-track"><span class="bar-fill" style="width:${width}%"></span></div>
        <span class="bar-value">${formatNumber(count)}</span>
      </div>
    `;
  }).join("");
}

function hotspotCardTemplate(item) {
  return `
    <article class="hotspot-card">
      <h3>${safeText(item.name, "未命名熱點")}</h3>
      <div class="score-badge">${formatNumber(Number(item.score || 0))}</div>
      <div class="tag-row">
        <span class="tag">${safeText(item.category, "未分類")}</span>
        <span class="tag">${safeText(item.department, "待確認主管機關")}</span>
      </div>
      <p><b>行動建議：</b>${safeText(item.action, "持續觀察後補充行動建議。")}</p>
      <a class="hotspot-link" href="./map.html">查看地圖 →</a>
    </article>
  `;
}

function renderHotspotCards(hotspots) {
  const mainTarget = document.getElementById("hotspotCards");
  const sideTarget = document.getElementById("hotspotSidebar");
  if (!mainTarget && !sideTarget) return;

  const items = (Array.isArray(hotspots) ? hotspots : PUBLIC_DASHBOARD_FALLBACK_HOTSPOTS)
    .slice()
    .sort((a, b) => Number(b.score || 0) - Number(a.score || 0))
    .slice(0, 3);

  const html = items.map(hotspotCardTemplate).join("");
  if (mainTarget) mainTarget.innerHTML = html;
  if (sideTarget) sideTarget.innerHTML = html;
}

function renderDataStatus(summary, health) {
  const target = document.getElementById("dataStatusGrid");
  if (!target) return;

  const totalSources = Number(summary?.total_sources ?? PUBLIC_DASHBOARD_FALLBACK_INVENTORY.total_count);
  const healthStatus = safeText(health?.status, "ok");
  const warnings = Array.isArray(health?.warnings) ? health.warnings.length : 0;

  const items = [
    {
      title: "官方資料源數量",
      text: `${formatNumber(totalSources)} 筆官方資料來源已完成盤點。`
    },
    {
      title: "prototype dashboard",
      text: "首頁目前使用 prototype data，作為公開展示與議題說明用儀表板。"
    },
    {
      title: "no live crawler",
      text: "尚未啟動 live crawler，也不會直接對資料來源網址發出程式請求。"
    },
    {
      title: "資料仍在接入中",
      text: "正式資料尚未全量接入，首頁數字仍屬非正式全量資料。"
    },
    {
      title: "GitHub Pages",
      text: `狀態：${healthStatus} ｜ warnings ${warnings} ｜ 網站可展示。`
    }
  ];

  target.innerHTML = items.map((item) => `
    <article class="status-item">
      <b>${item.title}</b>
      <span>${item.text}</span>
    </article>
  `).join("");
}

async function initPublicDashboard() {
  const [summary, trends, hotspots, health, inventory] = await Promise.all([
    loadJson("./data/dashboard_summary.json", PUBLIC_DASHBOARD_FALLBACK_SUMMARY),
    loadJson("./data/issue_trends.json", PUBLIC_DASHBOARD_FALLBACK_ISSUES),
    loadJson("./data/hotspots.json", PUBLIC_DASHBOARD_FALLBACK_HOTSPOTS),
    loadJson("./data/dashboard_health_check.json", PUBLIC_DASHBOARD_FALLBACK_HEALTH),
    loadJson("./data/open_data_url_inventory.json", PUBLIC_DASHBOARD_FALLBACK_INVENTORY)
  ]);

  renderHomepageKpis(summary, inventory, health);
  renderIssueRanking(trends);
  renderHotspotCards(hotspots);
  renderDataStatus({ total_sources: inventory?.total_count }, health);
}

document.addEventListener("DOMContentLoaded", () => {
  initPublicDashboard();
});
