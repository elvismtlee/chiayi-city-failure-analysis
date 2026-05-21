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

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

const TREND_LABELS = {
  up: '上升',
  down: '下降',
  stable: '穩定',
  spike: '快速升高',
};

const REVIEW_STATUS_LABELS = {
  prototype: '原型資料',
  uncertain: '待複核',
  unreviewed: '尚未人工檢查',
  reviewed: '已人工檢查',
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
      <b>建議：${escapeHtml(item.recommended_action || '持續補充資料並人工 review。')}</b>
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
  const summary = await readJson('./data/ai_issue_summary.json', {});
  const trends = await readJson('./data/issue_trends.json', []);
  const scores = await readJson('./data/urban_failure_scores.json', []);
  const departments = await readJson('./data/department_performance.json', []);
  const councilors = await readJson('./data/councilor_issue_analysis.json', []);

  const title = document.querySelector('[data-ai="title"]');
  const body = document.querySelector('[data-ai="summary"]');
  const updated = document.querySelector('[data-ai="updated"]');
  if (title) title.textContent = summary.summary_title || 'AI 城市觀察摘要';
  if (body) body.textContent = summary.summary || '資料讀取中。';
  if (updated) updated.textContent = `資料更新：${summary.updated_at || 'prototype'}`;

  renderList('[data-ai="findings"]', summary.top_findings || []);
  renderList('[data-ai="actions"]', summary.recommended_actions || []);
  renderTrendCards(trends);
  renderScoreTable(scores);
  renderDepartmentCards(departments);
  renderCouncilorCards(councilors);
}

bootInsights();
