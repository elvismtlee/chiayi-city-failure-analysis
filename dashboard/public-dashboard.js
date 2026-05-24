const HOMEPAGE_FALLBACK_SUMMARY = {
  total_cases: 12458,
  total_questions: 386,
  total_hotspots: 18,
  top_issue: "交通",
  updated_at: "2026-05-21"
};

const HOMEPAGE_FALLBACK_INVENTORY = {
  total_count: 29
};

const HOMEPAGE_FALLBACK_HEALTH = {
  status: "ok",
  warnings: [],
  missing_files: []
};

const HOMEPAGE_FALLBACK_ISSUES = [
  { display_name: "交通停車", current_count: 3, confidence: 0.45, review_status: "prototype", recommended_action: "先以交通停車作為觀察題組，補足更多樣本後再評估趨勢。", window_days: 90 },
  { display_name: "市場商圈", current_count: 4, confidence: 0.45, review_status: "prototype", recommended_action: "先以市場商圈作為觀察題組，補足更多樣本後再評估趨勢。", window_days: 90 },
  { display_name: "環境衛生", current_count: 2, confidence: 0.45, review_status: "prototype", recommended_action: "先以環境衛生作為觀察題組，補足更多樣本後再評估趨勢。", window_days: 90 },
  { display_name: "通學安全", current_count: 2, confidence: 0.45, review_status: "prototype", recommended_action: "先以通學安全作為觀察題組，補足更多樣本後再評估趨勢。", window_days: 90 },
  { display_name: "人行安全", current_count: 1, confidence: 0.45, review_status: "prototype", recommended_action: "先以人行安全作為觀察題組，補足更多樣本後再評估趨勢。", window_days: 90 }
];

const HOMEPAGE_FALLBACK_HOTSPOTS = [
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
  if (value === undefined || value === null || value === "") {
    return fallback;
  }
  return String(value);
}

function formatNumber(value) {
  const numeric = Number(value);
  if (Number.isFinite(numeric)) {
    return new Intl.NumberFormat("zh-TW").format(numeric);
  }
  return safeText(value, "0");
}

async function loadJson(path, fallback) {
  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to load ${path}`);
    }
    return await response.json();
  } catch (error) {
    return fallback;
  }
}

function getTarget(idOptions) {
  for (const id of idOptions) {
    const element = document.getElementById(id);
    if (element) {
      return element;
    }
  }
  return null;
}

function renderHomepageKpis(summary, inventory, health) {
  const target = getTarget(["homepage-kpis", "kpiGrid"]);
  if (!target) {
    return;
  }

  const totalSources = Array.isArray(inventory)
    ? inventory.length
    : Number(inventory?.total_count || HOMEPAGE_FALLBACK_INVENTORY.total_count);
  const deployStatus = safeText(health?.status, HOMEPAGE_FALLBACK_HEALTH.status).toLowerCase() === "ok"
    ? "Ready"
    : "Prototype";

  const kpis = [
    {
      label: "原型案件數",
      value: formatNumber(summary?.total_cases ?? HOMEPAGE_FALLBACK_SUMMARY.total_cases),
      desc: "作為原型儀表板的總案件量級指標。",
      source: "source: dashboard_summary.json"
    },
    {
      label: "質詢紀錄數",
      value: formatNumber(summary?.total_questions ?? HOMEPAGE_FALLBACK_SUMMARY.total_questions),
      desc: "對照地方議題分類與城市問題脈絡。",
      source: "source: dashboard_summary.json"
    },
    {
      label: "城市熱點",
      value: formatNumber(summary?.total_hotspots ?? HOMEPAGE_FALLBACK_SUMMARY.total_hotspots),
      desc: "目前熱點總數，用來標示需要優先看的區位。",
      source: "source: hotspots.json"
    },
    {
      label: "最大議題",
      value: safeText(summary?.top_issue, HOMEPAGE_FALLBACK_SUMMARY.top_issue),
      desc: "目前原型資料中最常出現的城市議題。",
      source: "source: issue_trends.json"
    },
    {
      label: "官方資料源",
      value: formatNumber(totalSources),
      desc: "已盤點的官方資料來源數量。",
      source: "source: open_data_url_inventory.json"
    },
    {
      label: "上線狀態",
      value: deployStatus,
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
  const target = getTarget(["issue-ranking-list", "issueBars"]);
  if (!target) {
    return;
  }

  const items = Array.isArray(trends) ? trends : [];
  const preferred = items.filter((item) => Number(item?.window_days) === 90);
  const chosen = (preferred.length ? preferred : HOMEPAGE_FALLBACK_ISSUES)
    .slice()
    .sort((left, right) => Number(right?.current_count || 0) - Number(left?.current_count || 0))
    .slice(0, 5);

  const maxCount = Math.max(...chosen.map((item) => Number(item?.current_count || 0)), 1);

  target.innerHTML = chosen.map((item) => {
    const width = Math.max(12, Math.round((Number(item?.current_count || 0) / maxCount) * 100));
    return `
      <article class="issue-card">
        <div class="issue-top">
          <span class="issue-name">${safeText(item?.display_name, "未命名議題")}</span>
          <div class="issue-meta">
            <span class="issue-pill">confidence ${Number(item?.confidence || 0).toFixed(2)}</span>
            <span class="issue-pill">${safeText(item?.review_status, "prototype")}</span>
          </div>
        </div>
        <div class="issue-bar"><span style="width:${width}%"></span></div>
        <div class="issue-foot">
          <span>${safeText(item?.recommended_action, "持續補資料後再評估。")}</span>
          <span class="issue-count">${formatNumber(item?.current_count || 0)}</span>
        </div>
      </article>
    `;
  }).join("");
}

function hotspotCardTemplate(item) {
  return `
    <article class="hotspot-card">
      <h3>${safeText(item?.name, "未命名熱點")}</h3>
      <div class="score-badge">${safeText(item?.score, "—")}</div>
      <div class="tag-row">
        <span class="tag">${safeText(item?.category, "待分類")}</span>
        <span class="tag">${safeText(item?.department, "待確認單位")}</span>
      </div>
      <p><b>行動建議：</b>${safeText(item?.action, "先補齊公開資料與欄位。")}</p>
      <a class="hotspot-link" href="./map.html">查看地圖 →</a>
    </article>
  `;
}

function renderHotspotCards(hotspots) {
  const cardsTarget = getTarget(["hotspot-cards", "hotspotCards"]);
  const sidebarTarget = getTarget(["hotspot-sidebar", "hotspotSidebar"]);
  const items = (Array.isArray(hotspots) ? hotspots : HOMEPAGE_FALLBACK_HOTSPOTS).slice(0, 3);
  const html = items.map(hotspotCardTemplate).join("");

  if (cardsTarget) {
    cardsTarget.innerHTML = html;
  }
  if (sidebarTarget) {
    sidebarTarget.innerHTML = html;
  }
}

function renderDataStatus(summary, health) {
  const target = getTarget(["data-status-grid", "dataStatusGrid"]);
  if (!target) {
    return;
  }

  const healthStatus = safeText(health?.status, HOMEPAGE_FALLBACK_HEALTH.status);
  const warningCount = Array.isArray(health?.warnings) ? health.warnings.length : 0;
  const totalHotspots = formatNumber(summary?.total_hotspots ?? HOMEPAGE_FALLBACK_SUMMARY.total_hotspots);
  const totalCases = formatNumber(summary?.total_cases ?? HOMEPAGE_FALLBACK_SUMMARY.total_cases);

  const items = [
    {
      title: "prototype dashboard",
      text: `目前首頁使用 ${totalCases} 筆原型案件與 ${totalHotspots} 個城市熱點，作為公開展示與分類觀察。`,
      badge: "prototype data"
    },
    {
      title: "非正式全量資料",
      text: `目前熱點 ${totalHotspots} 個屬於原型展示，正式資料仍在接入中。`,
      badge: "資料持續接入"
    },
    {
      title: "no live crawler",
      text: "正式資料接入前，不啟動 live crawler，也不對資料來源網址發出程式請求。",
      badge: "crawler off"
    },
    {
      title: "GitHub Pages",
      text: `網站狀態 ${healthStatus}，目前 warnings ${warningCount}，可作為公開儀表板原型展示。`,
      badge: `status: ${healthStatus}`
    }
  ];

  target.innerHTML = items.map((item) => `
    <article class="status-card">
      <h3>${item.title}</h3>
      <p>${item.text}</p>
      <span class="status-badge">${item.badge}</span>
    </article>
  `).join("");
}

async function initPublicDashboard() {
  const [summary, trends, hotspots, health, inventory] = await Promise.all([
    loadJson("./data/dashboard_summary.json", HOMEPAGE_FALLBACK_SUMMARY),
    loadJson("./data/issue_trends.json", HOMEPAGE_FALLBACK_ISSUES),
    loadJson("./data/hotspots.json", HOMEPAGE_FALLBACK_HOTSPOTS),
    loadJson("./data/dashboard_health_check.json", HOMEPAGE_FALLBACK_HEALTH),
    loadJson("./data/open_data_url_inventory.json", HOMEPAGE_FALLBACK_INVENTORY)
  ]);

  renderHomepageKpis(summary, inventory, health);
  renderIssueRanking(trends);
  renderHotspotCards(hotspots);
  renderDataStatus(summary, health);
}

document.addEventListener("DOMContentLoaded", () => {
  initPublicDashboard().catch(() => {
    renderHomepageKpis(HOMEPAGE_FALLBACK_SUMMARY, HOMEPAGE_FALLBACK_INVENTORY, HOMEPAGE_FALLBACK_HEALTH);
    renderIssueRanking(HOMEPAGE_FALLBACK_ISSUES);
    renderHotspotCards(HOMEPAGE_FALLBACK_HOTSPOTS);
    renderDataStatus(HOMEPAGE_FALLBACK_SUMMARY, HOMEPAGE_FALLBACK_HEALTH);
  });
});
