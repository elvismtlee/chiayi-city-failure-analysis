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

function escapeHtml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderList(selector, items) {
  const node = document.querySelector(selector);
  if (!node) return;
  node.innerHTML = items.map(item => `<li>${escapeHtml(item)}</li>`).join('');
}

function issueTrendTitle(item) {
  return item.display_name || item.issue || '未分類議題';
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

function groupTrendsByWindow(items) {
  return [7, 30, 90].map(days => ({
    days,
    items: items.filter(item => Number(item.window_days) === days),
  }));
}

function renderTrendCards(items) {
  const node = document.querySelector('[data-render="trends"]');
  if (!node) return;
  const groups = groupTrendsByWindow(items);
  node.innerHTML = groups.map(group => `
    <section class="trend-window" data-window-days="${group.days}">
      <div class="trend-window-heading">
        <h3>${group.days} 天</h3>
        <span>${group.items.length} 筆觀察</span>
      </div>
      <div class="trend-card-grid">
        ${group.items.map(renderTrendCard).join('') || '<p class="muted">目前沒有可顯示的趨勢資料。</p>'}
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
      <td>${escapeHtml(item.target_name)}</td>
      <td>${escapeHtml(item.issue)}</td>
      <td>${Number(item.score || 0)}</td>
      <td><span class="pill">${escapeHtml(item.level)}</span></td>
      <td>${escapeHtml(item.recommended_action)}</td>
    </tr>
  `).join('');
}

function renderDepartmentCards(items) {
  const node = document.querySelector('[data-render="departments"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <article class="card compact">
      <h3>${escapeHtml(item.department)}</h3>
      <p>案件量：${Number(item.total_cases || 0)}｜平均處理天數：${Number(item.avg_processing_days || 0)}</p>
      <p>主要議題：${(item.top_issues || []).map(escapeHtml).join('、')}</p>
      <b>回應指標：${Number(item.response_score || 0)}</b>
    </article>
  `).join('');
}

function renderCouncilorCards(items) {
  const node = document.querySelector('[data-render="councilors"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <article class="card compact">
      <h3>${escapeHtml(item.councilor_name)}</h3>
      <p>${escapeHtml(item.council_term)}｜${escapeHtml(item.district)}</p>
      <p>質詢樣本數：${Number(item.total_questions || 0)}</p>
      <b>主要議題：${(item.top_issues || []).map(escapeHtml).join('、')}</b>
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
