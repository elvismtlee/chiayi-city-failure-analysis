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

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

function renderCountList(items, emptyText) {
  if (!items || !items.length) return `<p class="empty">${escapeHtml(emptyText)}</p>`;
  return `<ul>${items.map(item => `<li><b>${escapeHtml(item.name)}</b><span>${escapeHtml(item.count)}</span></li>`).join('')}</ul>`;
}

function renderTopIssues(items) {
  if (!items || !items.length) return '<p class="empty">目前沒有可顯示的 top issues。</p>';
  return items.map(item => `
    <article class="card item-card">
      <h3>${escapeHtml(item.issue_title)}</h3>
      <p>${escapeHtml(item.summary)}</p>
      <div class="keywords">${(item.issue_keywords || []).map(keyword => `<span class="pill">${escapeHtml(keyword)}</span>`).join('')}</div>
      <p class="muted">${escapeHtml(item.department)} / ${escapeHtml(item.confidence_level)}</p>
    </article>
  `).join('');
}

function renderPolicyTopics(items) {
  if (!items || !items.length) return '<p class="empty">目前沒有建議政策題目。</p>';
  return items.map(item => `
    <article class="card item-card">
      <h3>${escapeHtml(item.topic_title)}</h3>
      <p>${escapeHtml(item.rationale)}</p>
      <div class="keywords">${(item.keywords || []).map(keyword => `<span class="pill">${escapeHtml(keyword)}</span>`).join('')}</div>
    </article>
  `).join('');
}

function renderNeedsReview(items) {
  if (!items || !items.length) return '<p class="empty">目前沒有待人工審核項目。</p>';
  return `<ul>${items.map(item => `<li><b>${escapeHtml(item.issue_title)}</b><span>${escapeHtml(item.review_reason)}</span></li>`).join('')}</ul>`;
}

function renderSourceFiles(items) {
  return `<ul>${(items || []).map(item => `<li><code>${escapeHtml(item)}</code></li>`).join('')}</ul>`;
}

function renderSummary(summary) {
  const departments = summary.department_summary || [];
  const keywords = summary.keyword_summary || [];
  setText('[data-stat="period"]', `${summary.week_start || '–'} 至 ${summary.week_end || '–'}`);
  setText('[data-stat="total"]', summary.total_candidates ?? 0);
  setText('[data-stat="departments"]', departments.length);
  setText('[data-stat="keywords"]', keywords.length);

  const departmentNode = document.querySelector('[data-render="department-summary"]');
  if (departmentNode) departmentNode.innerHTML = renderCountList(departments, '目前沒有局處摘要。');
  const keywordNode = document.querySelector('[data-render="keyword-summary"]');
  if (keywordNode) keywordNode.innerHTML = renderCountList(keywords, '目前沒有關鍵字摘要。');
  const topIssueNode = document.querySelector('[data-render="top-issues"]');
  if (topIssueNode) topIssueNode.innerHTML = renderTopIssues(summary.top_issues || []);
  const topicNode = document.querySelector('[data-render="policy-topics"]');
  if (topicNode) topicNode.innerHTML = renderPolicyTopics(summary.suggested_policy_topics || []);
  const reviewNode = document.querySelector('[data-render="needs-review"]');
  if (reviewNode) reviewNode.innerHTML = renderNeedsReview(summary.needs_review || []);
  const sourceNode = document.querySelector('[data-render="source-files"]');
  if (sourceNode) sourceNode.innerHTML = renderSourceFiles(summary.source_files || []);
}

async function bootWeeklySummary() {
  const summary = await readJson('./data/weekly_summary_draft.json', {});
  renderSummary(summary);
}

bootWeeklySummary();
