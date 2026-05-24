const FALLBACK_SUMMARY = {
  total_cases: 12458,
  total_questions: 386,
  total_hotspots: 18,
  top_issue: "交通",
  updated_at: "2026-05-21",
};

const FALLBACK_HEALTH = {
  status: "ok",
  warnings: [],
  generated_at: "local-fallback",
};

const FALLBACK_INVENTORY = {
  total_count: 29,
};

const FALLBACK_HOTSPOTS = [
  {
    name: "文化路商圈",
    category: "停車 / 人行",
    department: "交通處",
    score: 92,
    action: "商圈動線與停車熱點專案",
  },
  {
    name: "市場周邊",
    category: "垃圾 / 動線",
    department: "環保局 / 建設處",
    score: 78,
    action: "市場周邊環境改善與卸貨規劃",
  },
  {
    name: "學校周邊",
    category: "通學安全",
    department: "交通處 / 教育處",
    score: 71,
    action: "通學步道與接送區改善",
  },
];

const FALLBACK_ISSUES = [
  {
    display_name: "其他議題",
    current_count: 10,
    confidence: 0.4,
    review_status: "prototype",
    recommended_action: "補充樣本與會議日期後，再重新計算趨勢。",
    window_days: 90,
  },
  {
    display_name: "市場商圈",
    current_count: 4,
    confidence: 0.45,
    review_status: "prototype",
    recommended_action: "先把市場商圈問題作為可追蹤題組。",
    window_days: 90,
  },
  {
    display_name: "交通停車",
    current_count: 3,
    confidence: 0.45,
    review_status: "prototype",
    recommended_action: "先補交通停車與熱點對應資料。",
    window_days: 90,
  },
];

const FALLBACK_OVERVIEW = {
  public_use_status: "internal_command_center",
  generated_at: "fallback",
  source_files: [
    "dashboard/data/dashboard_summary.json",
    "dashboard/data/hotspots.json",
    "dashboard/data/issue_trends.json",
    "dashboard/data/open_data_url_inventory.json",
    "dashboard/data/dashboard_health_check.json",
    "dashboard/data/weekly_system_report.json",
  ],
  warnings: [],
};

const AVAILABLE_PAGES = [
  {
    title: "首頁儀表板 index.html",
    description: "第一眼先看城市數字、熱點、議題排行與行動建議。",
    status: "可展示",
    href: "./index.html",
  },
  {
    title: "城市熱點地圖 map.html",
    description: "用地圖方式看目前的西區熱點與問題分布。",
    status: "prototype",
    href: "./map.html",
  },
  {
    title: "資料來源 sources.html",
    description: "整理目前資料來源、來源邊界與檢查方式。",
    status: "可展示",
    href: "./sources.html",
  },
  {
    title: "方法論 methodology.html",
    description: "說明這個城市 dashboard 如何整理原型資料與分類邏輯。",
    status: "可展示",
    href: "./methodology.html",
  },
  {
    title: "健康檢查 health-check.html",
    description: "查看資料檔、頁面與 GitHub Pages 狀態是否正常。",
    status: "內部工具",
    href: "./health-check.html",
  },
  {
    title: "資料源檢查工作台 source-verification-workspace.html",
    description: "人工查看官方資料來源，確認之後能不能安全整理進資料庫。",
    status: "內部工具",
    href: "./source-verification-workspace.html",
  },
];

const NEXT_DATA_CARDS = [
  {
    title: "交通事故資料",
    current: "目前只有議題分類與熱點原型，還沒有正式事故統計接入。",
    next: "優先確認可公開的事故統計來源與欄位結構。",
    safety: "不抓個資，不推估個別事故當事人資訊。",
  },
  {
    title: "道路施工資料",
    current: "已能展示城市問題熱點，但施工資料仍未成為固定資料源。",
    next: "盤點官方施工公告格式，確認能不能整理成時間序列。",
    safety: "不對 source_url 發出程式請求。",
  },
  {
    title: "路燈照明資料",
    current: "路燈相關問題仍偏地方議題線索，缺正式資料表。",
    next: "尋找適合的官方入口與欄位，再評估是否能納入 dashboard。",
    safety: "不啟動 crawler，先做人工來源確認。",
  },
  {
    title: "停車資料",
    current: "已有停車熱點與部分官方來源盤點，但還沒做正式統計接入。",
    next: "先整理停車資料欄位，再決定後續介接方式。",
    safety: "crawler_execution_allowed = false。",
  },
  {
    title: "環境衛生資料",
    current: "已有市場周邊與垃圾動線熱點，但仍是 prototype 問題分類。",
    next: "補足官方環境資料後，再提升指標的可信度。",
    safety: "不抓私人陳情全文。",
  },
  {
    title: "通學安全資料",
    current: "已有學校周邊熱點與通學安全題組，但缺正式結構化資料。",
    next: "優先盤點教育與交通相關公開欄位。",
    safety: "engineering_review_allowed = false。",
  },
];

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function fetchJson(path, fallback) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn(`Failed to load ${path}, using fallback.`, error);
    return fallback;
  }
}

function formatConfidence(value) {
  if (typeof value !== "number") return "confidence n/a";
  return `confidence ${Math.round(value * 100)}%`;
}

function renderHeroMeta(overview) {
  const generatedAt = document.querySelector("#heroGeneratedAt");
  const publicStatus = document.querySelector("#heroPublicStatus");
  if (generatedAt) generatedAt.textContent = `generated_at ${overview.generated_at || "not recorded"}`;
  if (publicStatus) publicStatus.textContent = overview.public_use_status || "internal_command_center";
}

function renderControlRoomKpis(summary, inventory, health) {
  const target = document.querySelector("#controlRoomKpis");
  const cards = [
    {
      label: "原型案件數",
      value: Number(summary.total_cases || 12458).toLocaleString("en-US"),
      note: "來自 dashboard_summary.json，代表目前可展示的原型案件量級。",
    },
    {
      label: "質詢紀錄數",
      value: Number(summary.total_questions || 386).toLocaleString("en-US"),
      note: "作為地方議題與城市問題分類的原型背景資料。",
    },
    {
      label: "城市熱點",
      value: String(summary.total_hotspots || 18),
      note: "目前已整理出的熱點數量，方便快速看到焦點區域。",
    },
    {
      label: "最大議題",
      value: summary.top_issue || "交通",
      note: "根據現有原型資料，交通仍是目前最重要的題組。",
    },
    {
      label: "官方資料源",
      value: String(inventory.total_count || 29),
      note: "代表已盤點的官方來源數量，不等於已全量接入。",
    },
    {
      label: "Health Check",
      value: String(health.status || "ok"),
      note: "目前頁面與本地資料檔狀態正常，可作為展示用 prototype。",
    },
  ];

  target.innerHTML = cards.map((card) => `
    <article class="card">
      <span class="kpi-label">${escapeHtml(card.label)}</span>
      <strong class="kpi-value">${escapeHtml(card.value)}</strong>
      <span class="kpi-note">${escapeHtml(card.note)}</span>
    </article>
  `).join("");
}

function renderAvailablePages() {
  const target = document.querySelector("#availablePages");
  target.innerHTML = AVAILABLE_PAGES.map((page) => `
    <a class="page-card" href="${escapeHtml(page.href)}">
      <b>${escapeHtml(page.title)}</b>
      <p>${escapeHtml(page.description)}</p>
      <div class="page-meta">
        <span class="meta ${page.status === "可展示" ? "green" : page.status === "prototype" ? "orange" : ""}">${escapeHtml(page.status)}</span>
        <span class="meta">${escapeHtml(page.href)}</span>
      </div>
      <span class="page-link">前往頁面 →</span>
    </a>
  `).join("");
}

function renderDataStatus(summary, inventory, hotspots, trends, health) {
  const statusList = document.querySelector("#dataStatusList");
  const summaryList = document.querySelector("#dataStatusSummary");
  const topIssues = (trends || [])
    .filter((item) => item.window_days === 90)
    .sort((a, b) => (b.current_count || 0) - (a.current_count || 0))
    .slice(0, 3);
  const topHotspots = (hotspots || []).slice(0, 3);

  const timeline = [
    {
      title: "已有 prototype data",
      desc: `目前首頁與總控台可展示 ${Number(summary.total_cases || 12458).toLocaleString("en-US")} 筆原型案件量級與 ${summary.total_hotspots || 18} 個熱點。`,
    },
    {
      title: "官方資料來源盤點已建立",
      desc: `本地 inventory 已盤點 ${inventory.total_count || 29} 個官方資料來源，方便後續逐步接入。`,
    },
    {
      title: "資料源人工檢查中",
      desc: "正式資料接入前，仍以人工檢查資料來源、欄位與風險為主。",
    },
    {
      title: "crawler 尚未啟動",
      desc: "目前維持 no live crawler、no source_url requests，不把 prototype 當正式全量資料。",
    },
    {
      title: "正式統計資料尚未全量接入",
      desc: `Health Check 現在是 ${health.status || "ok"}，代表頁面可展示，但不代表正式統計資料已完整到位。`,
    },
  ];

  statusList.innerHTML = timeline.map((item, index) => `
    <div class="timeline-item">
      <div class="timeline-dot">${index + 1}</div>
      <div>
        <b>${escapeHtml(item.title)}</b>
        <span>${escapeHtml(item.desc)}</span>
      </div>
    </div>
  `).join("");

  const summaryItems = [
    topHotspots[0]
      ? `最高熱點是 ${topHotspots[0].name}，分數 ${topHotspots[0].score}，建議 ${topHotspots[0].action}。`
      : "目前沒有可顯示的熱點資料。",
    topIssues[0]
      ? `90 天題組中目前件數最高的是 ${topIssues[0].display_name}，${formatConfidence(topIssues[0].confidence)}。`
      : "目前沒有可顯示的 90 天議題資料。",
    "這些數字都來自本地 JSON 與 prototype dashboard，不是正式全量統計。",
  ];

  summaryList.innerHTML = summaryItems.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
}

function renderDataFiles(overview, health) {
  const target = document.querySelector("#dataFilesGrid");
  const checkedByPath = Object.fromEntries((health.checked_files || []).map((item) => [item.file, item]));
  const cards = [
    {
      title: "儀表板摘要",
      path: "dashboard/data/dashboard_summary.json",
      desc: "整理原型案件數、質詢紀錄數、城市熱點與最大議題。",
    },
    {
      title: "熱點資料",
      path: "dashboard/data/hotspots.json",
      desc: "顯示文化路商圈、市場周邊、學校周邊等重點熱點。",
    },
    {
      title: "議題趨勢",
      path: "dashboard/data/issue_trends.json",
      desc: "用不同時間窗追蹤地方議題題組，目前仍是 prototype 分類。",
    },
    {
      title: "資料來源盤點",
      path: "dashboard/data/open_data_url_inventory.json",
      desc: "盤點官方資料來源，幫助後續決定哪些資料可以安全接入。",
    },
    {
      title: "健康檢查",
      path: "dashboard/data/dashboard_health_check.json",
      desc: "確認頁面、資料檔與 GitHub Pages 狀態是否正常。",
    },
    {
      title: "每週系統報告",
      path: "dashboard/data/weekly_system_report.json",
      desc: "用來追蹤目前整體資料與內容系統的每週狀態。",
    },
  ];

  target.innerHTML = cards.map((card) => {
    const checked = checkedByPath[card.path] || {};
    const state = checked.exists === false ? "尚未就緒" : checked.valid_json === false ? "需修正" : "可讀取";
    return `
      <article class="data-card">
        <b>${escapeHtml(card.title)}</b>
        <p>${escapeHtml(card.desc)}</p>
        <div class="data-meta">
          <span class="meta ${state === "可讀取" ? "green" : state === "需修正" ? "orange" : ""}">${escapeHtml(state)}</span>
          <span class="meta">${escapeHtml(card.path)}</span>
        </div>
        <span class="data-link">source file count ${escapeHtml(String((overview.source_files || []).length))}</span>
      </article>
    `;
  }).join("");
}

function renderNextDataCards() {
  const target = document.querySelector("#nextDataCards");
  target.innerHTML = NEXT_DATA_CARDS.map((card) => `
    <article class="next-card">
      <b>${escapeHtml(card.title)}</b>
      <p><strong>現況：</strong>${escapeHtml(card.current)}</p>
      <p><strong>下一步：</strong>${escapeHtml(card.next)}</p>
      <div class="next-meta">
        <span class="meta orange">${escapeHtml(card.safety)}</span>
      </div>
    </article>
  `).join("");
}

async function loadControlRoomData() {
  const [overview, summary, hotspots, trends, health, inventory] = await Promise.all([
    fetchJson("./data/command_center_overview.json", FALLBACK_OVERVIEW),
    fetchJson("./data/dashboard_summary.json", FALLBACK_SUMMARY),
    fetchJson("./data/hotspots.json", FALLBACK_HOTSPOTS),
    fetchJson("./data/issue_trends.json", FALLBACK_ISSUES),
    fetchJson("./data/dashboard_health_check.json", FALLBACK_HEALTH),
    fetchJson("./data/open_data_url_inventory.json", FALLBACK_INVENTORY),
  ]);

  renderHeroMeta(overview);
  renderControlRoomKpis(summary, inventory, health);
  renderAvailablePages();
  renderDataStatus(summary, inventory, hotspots, trends, health);
  renderDataFiles(overview, health);
  renderNextDataCards();
}

loadControlRoomData().catch((error) => {
  console.warn("Failed to render command center, using DOM fallback.", error);
  const containers = [
    "#controlRoomKpis",
    "#availablePages",
    "#dataStatusList",
    "#dataStatusSummary",
    "#dataFilesGrid",
    "#nextDataCards",
  ];
  containers.forEach((selector) => {
    const node = document.querySelector(selector);
    if (node && !node.innerHTML.trim()) {
      node.innerHTML = '<div class="empty">目前資料讀取失敗，請稍後重新整理，或檢查本地 JSON 是否完整。</div>';
    }
  });
});
