async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(path);
    return await response.json();
  } catch (error) {
    console.warn('Use fallback:', path, error);
    return fallback;
  }
}

function renderList(selector, items) {
  const node = document.querySelector(selector);
  if (!node) return;
  node.innerHTML = items.map(item => `<li>${escapeHtml(item)}</li>`).join('');
}

function normalizePublicAction(text) {
  const value = String(text ?? '');
  if (!value) return '持續補充資料與熱點觀察。';
  return value
    .replace('建立嘉義市議會 metadata crawler', '整理嘉義市議會 metadata 來源與欄位')
    .replace('補齊 1999 與陳情資料來源', '補足可公開展示的城市問題資料來源')
    .replace('將熱點資料轉為 GeoJSON 並接入 Leaflet 地圖', '持續補強熱點資料與地圖呈現');
}

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

const FALLBACK_AI_SUMMARY = {
  updated_at: "2026-05-21 09:00:00",
  summary_title: "本週嘉義城市故障觀察",
  summary: "目前為原型資料。平台將整合議會質詢、1999 陳情與地方生活議題，形成可追蹤、可視覺化的城市治理資料。",
  top_findings: [
    "交通、停車與道路是第一波優先觀察議題",
    "市場周邊與學校周邊適合作為熱點分析示範區",
    "議員質詢 metadata 將作為議題關注度分析基礎",
  ],
  recommended_actions: [
    "建立嘉義市議會 metadata crawler",
    "補齊 1999 與陳情資料來源",
    "將熱點資料轉為 GeoJSON 並接入 Leaflet 地圖",
  ],
};

const TREND_LABELS = {
  up: '上升',
  down: '下降',
  stable: '穩定',
  spike: '快速升高',
};

const REVIEW_STATUS_LABELS = {
  prototype: '原型資料',
  uncertain: '待複核',
  unreviewed: '待確認',
  reviewed: '已確認',
  corrected: '已人工修正',
};

const TREND_WINDOWS = [
  {
    days: 7,
    id: 'trend-7',
    title: '最近 7 天｜短期熱點',
    note: '適合觀察最近快速升高、需要立即注意的議題。',
  },
  {
    days: 30,
    id: 'trend-30',
    title: '最近 30 天｜中期變化',
    note: '適合觀察一個月內逐漸累積的地方議題。',
  },
  {
    days: 90,
    id: 'trend-90',
    title: '最近 90 天｜長期趨勢',
    note: '適合觀察較長時間持續存在的結構性問題。',
  },
];

const FALLBACK_TRENDS = [
  {
    issue: "market",
    display_name: "市場商圈",
    current_count: 4,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 7,
    confidence: 0.45,
    summary: "7 天趨勢目前仍是 metadata / sample 階段；市場商圈是最明顯的高密度觀察題組。",
    review_status: "prototype",
    recommended_action: "先以市場商圈作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "traffic",
    display_name: "交通停車",
    current_count: 3,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 7,
    confidence: 0.45,
    summary: "7 天趨勢目前仍是 metadata / sample 階段；交通停車是最需要優先接入正式資料的分類。",
    review_status: "prototype",
    recommended_action: "先以交通停車作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "school",
    display_name: "通學安全",
    current_count: 2,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 7,
    confidence: 0.45,
    summary: "7 天趨勢目前仍是 metadata / sample 階段；學校周邊安全問題值得繼續補資料。",
    review_status: "prototype",
    recommended_action: "先以通學安全作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "market",
    display_name: "市場商圈",
    current_count: 4,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 30,
    confidence: 0.45,
    summary: "30 天趨勢目前仍是 metadata / sample 階段；市場商圈持續是高優先觀察題組。",
    review_status: "prototype",
    recommended_action: "先以市場商圈作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "environment",
    display_name: "環境衛生",
    current_count: 2,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 30,
    confidence: 0.45,
    summary: "30 天趨勢目前仍是 metadata / sample 階段；市場周邊環境問題值得補更多正式資料。",
    review_status: "prototype",
    recommended_action: "先以環境衛生作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "traffic",
    display_name: "交通停車",
    current_count: 3,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 30,
    confidence: 0.45,
    summary: "30 天趨勢目前仍是 metadata / sample 階段；交通停車與商圈動線值得持續追蹤。",
    review_status: "prototype",
    recommended_action: "先以交通停車作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "market",
    display_name: "市場商圈",
    current_count: 4,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 90,
    confidence: 0.45,
    summary: "90 天趨勢目前仍是 metadata / sample 階段；市場商圈是最穩定的長期觀察題組。",
    review_status: "prototype",
    recommended_action: "先以市場商圈作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "traffic",
    display_name: "交通停車",
    current_count: 3,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 90,
    confidence: 0.45,
    summary: "90 天趨勢目前仍是 metadata / sample 階段；交通停車是最需要率先轉成正式城市指標的題組。",
    review_status: "prototype",
    recommended_action: "先以交通停車作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
  {
    issue: "school",
    display_name: "通學安全",
    current_count: 2,
    previous_count: 0,
    change_percent: 0,
    trend: "stable",
    window_days: 90,
    confidence: 0.45,
    summary: "90 天趨勢目前仍是 metadata / sample 階段；學校周邊安全與接送區是值得長期追蹤的分類。",
    review_status: "prototype",
    recommended_action: "先以通學安全作為觀察題組，補足會議日期與更多樣本後再評估趨勢。",
  },
];

const FALLBACK_SCORES = [
  {
    target_name: "文化路商圈",
    issue: "停車 / 人行",
    score: 92,
    level: "極高",
    recommended_action: "商圈停車與人行動線改善專案。",
  },
  {
    target_name: "市場周邊",
    issue: "垃圾 / 動線",
    score: 78,
    level: "高",
    recommended_action: "市場周邊環境改善與卸貨動線規劃。",
  },
  {
    target_name: "學校周邊",
    issue: "通學安全",
    score: 71,
    level: "高",
    recommended_action: "通學安全盤點與行人友善改善。",
  },
];

const FALLBACK_DEPARTMENTS = [
  {
    department: "交通處",
    total_cases: 320,
    avg_processing_days: 12.5,
    top_issues: ["停車", "號誌", "通學安全"],
    response_score: 78,
  },
  {
    department: "工務處",
    total_cases: 260,
    avg_processing_days: 15.8,
    top_issues: ["路平", "施工", "人行道"],
    response_score: 72,
  },
  {
    department: "環保局",
    total_cases: 210,
    avg_processing_days: 8.4,
    top_issues: ["垃圾", "異味", "噪音"],
    response_score: 81,
  },
];

const FALLBACK_COUNCILORS = [
  {
    councilor_name: "範例議員 A",
    council_term: "第十一屆",
    district: "西區",
    total_questions: 25,
    top_issues: ["交通", "道路", "教育"],
  },
  {
    councilor_name: "範例議員 B",
    council_term: "第十一屆",
    district: "西區",
    total_questions: 18,
    top_issues: ["環境", "文化", "社福"],
  },
];

function groupTrendsByWindow(items) {
  return TREND_WINDOWS.map(window => ({
    ...window,
    items: items.filter(item => Number(item.window_days) === window.days),
  }));
}

function issueTrendTitle(item) {
  return item.display_name || item.issue || '未分類議題';
}

function renderTrendCards(items) {
  const node = document.querySelector('[data-render="trends"]');
  if (!node) return;
  const groups = groupTrendsByWindow(items);
  node.innerHTML = groups.map(group => `
    <section id="${group.id}" class="trend-group trend-group-${group.days}" data-window-days="${group.days}">
      <div class="trend-group-header">
        <div>
          <h3>${group.title}</h3>
          <p class="trend-group-note">${group.note}</p>
        </div>
        <span>${group.items.length} 筆觀察</span>
      </div>
      <div class="trend-card-grid">
        ${group.items.map(renderTrendCard).join('') || '<p class="trend-empty">目前沒有可顯示的趨勢資料。</p>'}
      </div>
    </section>
  `).join('');
}

function renderTrendCard(item) {
  const displayName = issueTrendTitle(item);
  const trend = TREND_LABELS[item.trend] || item.trend || '待判讀';
  const reviewStatus = REVIEW_STATUS_LABELS[item.review_status] || item.review_status || '待確認';
  const confidence = Number(item.confidence ?? 0);
  return `
    <article class="card trend-card">
      <div class="trend-card-topline">
        <span class="pill">${escapeHtml(trend)}</span>
        <span class="pill ghost">${escapeHtml(reviewStatus)}</span>
      </div>
      <h4>${escapeHtml(displayName)}</h4>
      <dl class="trend-metrics">
        <div><dt>目前</dt><dd>${Number(item.current_count || 0)}</dd></div>
        <div><dt>前期</dt><dd>${Number(item.previous_count || 0)}</dd></div>
        <div><dt>變化</dt><dd>${Number(item.change_percent || 0)}%</dd></div>
        <div><dt>信心</dt><dd>${Math.round(confidence * 100)}%</dd></div>
      </dl>
      <p>${escapeHtml(item.summary || '目前仍在資料整理階段。')}</p>
      <b>建議：${escapeHtml(item.recommended_action || '持續補充資料並做公開資料確認。')}</b>
    </article>
  `;
}

function renderScoreTable(items) {
  const node = document.querySelector('[data-render="scores"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <tr>
      <td>${item.target_name}</td>
      <td>${item.issue}</td>
      <td>${item.score}</td>
      <td><span class="pill">${item.level}</span></td>
      <td>${item.recommended_action}</td>
    </tr>
  `).join('');
}

function renderDepartmentCards(items) {
  const node = document.querySelector('[data-render="departments"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <article class="card compact">
      <h3>${item.department}</h3>
      <p>案件量：${item.total_cases}｜平均處理天數：${item.avg_processing_days}</p>
      <p>主要議題：${item.top_issues.join('、')}</p>
      <b>回應指標：${item.response_score}</b>
    </article>
  `).join('');
}

function renderCouncilorCards(items) {
  const node = document.querySelector('[data-render="councilors"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <article class="card compact">
      <h3>${item.councilor_name}</h3>
      <p>${item.council_term}｜${item.district}</p>
      <p>質詢樣本數：${item.total_questions}</p>
      <b>主要議題：${item.top_issues.join('、')}</b>
    </article>
  `).join('');
}

async function bootInsights() {
  const summary = await readJson('./data/ai_issue_summary.json', FALLBACK_AI_SUMMARY);
  const trends = await readJson('./data/issue_trends.json', FALLBACK_TRENDS);
  const scores = await readJson('./data/urban_failure_scores.json', FALLBACK_SCORES);
  const departments = await readJson('./data/department_performance.json', FALLBACK_DEPARTMENTS);
  const councilors = await readJson('./data/councilor_issue_analysis.json', FALLBACK_COUNCILORS);

  const title = document.querySelector('[data-ai="title"]');
  const body = document.querySelector('[data-ai="summary"]');
  const updated = document.querySelector('[data-ai="updated"]');
  if (title) title.textContent = summary.summary_title || 'AI 城市觀察摘要';
  if (body) body.textContent = summary.summary || '資料讀取中。';
  if (updated) updated.textContent = `資料更新：${summary.updated_at || 'prototype'}`;

  renderList('[data-ai="findings"]', summary.top_findings || []);
  renderList('[data-ai="actions"]', (summary.recommended_actions || []).map(normalizePublicAction));
  renderTrendCards(trends);
  renderScoreTable(scores);
  renderDepartmentCards(departments);
  renderCouncilorCards(councilors);
}

document.addEventListener('DOMContentLoaded', () => {
  bootInsights().catch((error) => {
    console.warn('Insights fallback content is active:', error);
  });
});
