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
  node.innerHTML = items.map(item => `<li>${item}</li>`).join('');
}

function issueTrendTitle(item) {
  return item.display_name || item.issue || '未分類議題';
}

function renderTrendCards(items) {
  const node = document.querySelector('[data-render="trends"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <article class="card">
      <div class="eyebrow">${item.district}｜${item.trend}</div>
      <h3>${issueTrendTitle(item)} <span>${item.change_percent}%</span></h3>
      <p>${item.summary}</p>
      <b>建議：${item.recommended_action}</b>
    </article>
  `).join('');
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
