async function loadJson(path) {
  const response = await fetch(path, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error(`Failed to load ${path}`);
  }
  return response.json();
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) {
    node.textContent = value;
  }
}

function createPill(text) {
  const span = document.createElement('span');
  span.className = 'module-pill';
  span.textContent = text;
  return span;
}

function createLinkButton(label, href, tone = '') {
  const a = document.createElement('a');
  a.href = href;
  a.className = `quick-link${tone ? ` ${tone}` : ''}`;
  a.textContent = label;
  return a;
}

function renderVisibleKpis(summary) {
  const container = document.querySelector('[data-render="home-mvp-kpis"]');
  if (!container) return;

  const kpis = [
    ['已盤點官方 URL', summary.visible_kpis.official_url_inventory_count, '29 筆來源已進 inventory'],
    ['Top 10 審核任務', summary.visible_kpis.top10_review_tasks_count, '高優先人工審核任務'],
    ['Day 1 任務', summary.visible_kpis.day1_task_count, '今天先做 3 筆'],
    ['Day 1 預估時間', `${summary.visible_kpis.day1_estimated_minutes} 分鐘`, '一人團隊可執行'],
    ['Patch 草稿', summary.visible_kpis.patch_draft_count, '等待人工回填'],
    ['Health Check', summary.visible_kpis.health_status, 'status ok / warnings []'],
  ];

  container.innerHTML = '';
  kpis.forEach(([label, value, note]) => {
    const article = document.createElement('article');
    article.className = 'mvp-kpi-card';
    article.innerHTML = `<div class="label">${label}</div><div class="value">${value}</div><p>${note}</p>`;
    container.appendChild(article);
  });
}

function renderResultCards(summary) {
  const container = document.querySelector('[data-render="home-results-cards"]');
  if (!container) return;

  const cards = [
    {
      title: '官方資料盤點',
      stat: `${summary.visible_kpis.official_url_inventory_count} 筆官方 URL inventory`,
      body: '官方資料來源已整理進 dashboard，可直接回看來源頁與人工審核入口。',
      href: './open-data-inventory.html',
      cta: '查看盤點',
    },
    {
      title: 'Top 10 人工審核任務',
      stat: `${summary.visible_kpis.top10_review_tasks_count} 筆高優先審核任務`,
      body: '已從 readiness report 挑出最適合一人團隊先處理的官方資料來源。',
      href: './open-data-top10-tasks.html',
      cta: '查看任務',
    },
    {
      title: 'Day 1 人工審核工作包',
      stat: `${summary.visible_kpis.day1_task_count} 筆 Day 1 任務 / 預估 ${summary.visible_kpis.day1_estimated_minutes} 分鐘`,
      body: '今天要做哪 3 筆、每筆該記什麼、要回填什麼，都已整理成可執行工作包。',
      href: './open-data-manual-review-packets.html',
      cta: '打開工作包',
    },
    {
      title: 'Day 1 審核表單草稿',
      stat: `${summary.visible_kpis.manual_review_form_count} 筆可填寫表單草稿`,
      body: '已把 reviewer fields、source identity、risk review 等欄位拆成可直接填的表單段落。',
      href: './open-data-day1-review-form.html',
      cta: '查看表單',
    },
    {
      title: 'Patch 草稿',
      stat: `${summary.visible_kpis.patch_draft_count} 筆回填 Patch 草稿`,
      body: '人工審核完成後，要怎麼回填結果、工作簿與工程審查清單，現在已經有草稿路徑。',
      href: './open-data-manual-review-patches.html',
      cta: '查看 Patch',
    },
    {
      title: 'Health Check',
      stat: `status ${summary.visible_kpis.health_status} / warnings []`,
      body: '頁面、JSON、導覽與工作文件都已納入健康檢查，現在可以快速確認整體狀態。',
      href: './health-check.html',
      cta: '查看健康檢查',
    },
  ];

  container.innerHTML = '';
  cards.forEach((card) => {
    const article = document.createElement('article');
    article.className = 'result-card';
    article.innerHTML = `
      <div class="result-card-top">
        <span class="result-tag">Visible MVP</span>
        <h3>${card.title}</h3>
      </div>
      <strong>${card.stat}</strong>
      <p>${card.body}</p>
      <a class="result-link" href="${card.href}">${card.cta} →</a>
    `;
    container.appendChild(article);
  });
}

function renderCompletedModules(summary) {
  const container = document.querySelector('[data-render="home-completed-modules"]');
  if (!container) return;
  container.innerHTML = '';
  summary.completed_modules.forEach((item) => container.appendChild(createPill(item)));
}

function renderNextActions(summary) {
  const container = document.querySelector('[data-render="home-next-actions"]');
  if (!container) return;
  container.innerHTML = '';
  summary.next_actions.forEach((item, index) => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${index + 1}.</strong> ${item}`;
    container.appendChild(li);
  });
}

function renderSafetyNotes(summary) {
  const container = document.querySelector('[data-render="home-safety-notes"]');
  if (!container) return;
  container.innerHTML = '';
  summary.safety_notes.forEach((item) => container.appendChild(createPill(item)));
}

function renderQuickLinks() {
  const container = document.querySelector('[data-render="home-quick-links"]');
  if (!container) return;

  const links = [
    ['Day 1 審核表單', './open-data-day1-review-form.html'],
    ['Day 1 填寫範例', './open-data-day1-sample-results.html'],
    ['回填 Patch 草稿', './open-data-manual-review-patches.html'],
    ['人工審核工作包', './open-data-manual-review-packets.html'],
    ['人工審核 SOP', './open-data-manual-review-sop.html'],
    ['Evidence Pack', './open-data-review-evidence.html'],
    ['Engineering Review Checklist', './open-data-engineering-review.html'],
    ['Sources', './sources.html'],
    ['Health Check', './health-check.html'],
  ];

  container.innerHTML = '';
  links.forEach(([label, href], index) => {
    container.appendChild(createLinkButton(label, href, index < 3 ? 'primary' : 'secondary'));
  });
}

async function bootHomeVisibleMvp() {
  const root = document.getElementById('visibleMvpHome');
  if (!root) return;

  try {
    const summary = await loadJson('./data/home_visible_mvp_summary.json');
    setText('[data-home="status"]', '目前狀態：內部人工審核階段，尚未啟動 live crawler。');
    setText('[data-home="generated-at"]', summary.generated_at);
    renderVisibleKpis(summary);
    renderResultCards(summary);
    renderCompletedModules(summary);
    renderNextActions(summary);
    renderSafetyNotes(summary);
    renderQuickLinks();
  } catch (error) {
    console.error(error);
    setText('[data-home="status"]', '首頁摘要讀取中斷，請回健康檢查看目前狀態。');
  }
}

bootHomeVisibleMvp();
