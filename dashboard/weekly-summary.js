async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn('Use fallback:', path, error);
    const notice = document.querySelector('.notice');
    if (notice) notice.textContent = `讀取每週摘要資料失敗：${error.message}`;
    return fallback;
  }
}

function valueOrPending(value) {
  return value === undefined || value === null || value === '' ? '待補' : String(value);
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = valueOrPending(value);
}

function chip(label, count) {
  const span = document.createElement('span');
  span.className = 'chip';
  span.textContent = count === undefined ? valueOrPending(label) : `${valueOrPending(label)}：${count}`;
  return span;
}

function renderChipList(selector, items) {
  const node = document.querySelector(selector);
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有資料。';
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(chip(item.name, item.count)));
}

function makeIssueCard(issue) {
  const card = document.createElement('article');
  card.className = 'card issue-card';
  const title = document.createElement('h3');
  title.textContent = valueOrPending(issue.issue_title);
  const badges = document.createElement('div');
  badges.className = 'badge-row';
  [issue.department, issue.review_status, issue.confidence_level].filter(Boolean).forEach((text, index) => {
    const badge = document.createElement('span');
    badge.className = index === 0 ? 'badge' : index === 1 ? 'badge purple' : 'badge orange';
    badge.textContent = text;
    badges.appendChild(badge);
  });
  const summary = document.createElement('p');
  summary.className = 'summary-text';
  summary.textContent = valueOrPending(issue.summary);
  const keywords = document.createElement('div');
  keywords.className = 'chip-list';
  (issue.issue_keywords || []).forEach(keyword => keywords.appendChild(chip(keyword)));
  const meta = document.createElement('div');
  meta.className = 'meta-list';
  const source = document.createElement('div');
  source.textContent = `來源：${valueOrPending(issue.source_url)}`;
  meta.appendChild(source);
  card.append(title, badges, summary, keywords, meta);
  return card;
}

function makePolicyCard(topic) {
  const card = document.createElement('article');
  card.className = 'card issue-card';
  const title = document.createElement('h3');
  title.textContent = valueOrPending(topic.topic_title);
  const badges = document.createElement('div');
  badges.className = 'badge-row';
  const badge = document.createElement('span');
  badge.className = 'badge purple';
  badge.textContent = valueOrPending(topic.review_status);
  badges.appendChild(badge);
  const rationale = document.createElement('p');
  rationale.className = 'summary-text';
  rationale.textContent = valueOrPending(topic.rationale);
  const keywords = document.createElement('div');
  keywords.className = 'chip-list';
  (topic.keywords || []).forEach(keyword => keywords.appendChild(chip(keyword)));
  card.append(title, badges, rationale, keywords);
  return card;
}

function makeReviewCard(item) {
  const card = document.createElement('article');
  card.className = 'card issue-card';
  const title = document.createElement('h3');
  title.textContent = valueOrPending(item.issue_title);
  const meta = document.createElement('div');
  meta.className = 'meta-list';
  ['review_reason', 'recommended_next_step'].forEach(key => {
    const row = document.createElement('div');
    row.textContent = `${key}：${valueOrPending(item[key])}`;
    meta.appendChild(row);
  });
  card.append(title, meta);
  return card;
}

function renderCards(selector, items, factory, emptyText) {
  const node = document.querySelector(selector);
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = emptyText;
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(factory(item)));
}

function renderSourceFiles(files) {
  const node = document.querySelector('[data-render="source-files"]');
  if (!node) return;
  node.textContent = '';
  if (!files.length) {
    const empty = document.createElement('div');
    empty.textContent = '目前沒有來源檔案。';
    node.appendChild(empty);
    return;
  }
  files.forEach(file => {
    const row = document.createElement('div');
    row.textContent = file;
    node.appendChild(row);
  });
}

function renderSummary(summary) {
  const departments = summary.department_summary || [];
  const keywords = summary.keyword_summary || [];
  setText('[data-stat="period"]', `${summary.week_start || '–'} ～ ${summary.week_end || '–'}`);
  setText('[data-stat="total"]', summary.total_candidates ?? 0);
  setText('[data-stat="departments"]', departments.length);
  setText('[data-stat="keywords"]', keywords.length);
  renderCards('[data-render="top-issues"]', summary.top_issues || [], makeIssueCard, '目前沒有重點議題。');
  renderCards('[data-render="policy-topics"]', summary.suggested_policy_topics || [], makePolicyCard, '目前沒有建議政策討論題。');
  renderCards('[data-render="needs-review"]', summary.needs_review || [], makeReviewCard, '目前沒有待人工審核項目。');
  renderChipList('[data-render="department-summary"]', departments);
  renderChipList('[data-render="keyword-summary"]', keywords);
  renderSourceFiles(summary.source_files || []);
}

async function bootWeeklySummary() {
  const summary = await readJson('./data/weekly_summary_draft.json', {});
  renderSummary(summary);
}

bootWeeklySummary();
