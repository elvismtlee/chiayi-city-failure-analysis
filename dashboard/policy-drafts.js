async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn('Use fallback:', path, error);
    const notice = document.querySelector('.notice');
    if (notice) notice.textContent = `讀取政策草稿資料失敗：${error.message}`;
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

function badge(text, className = '') {
  const node = document.createElement('span');
  node.className = `badge ${className}`.trim();
  node.textContent = valueOrPending(text);
  return node;
}

function chip(text) {
  const node = document.createElement('span');
  node.className = 'chip';
  node.textContent = valueOrPending(text);
  return node;
}

function renderStats(items) {
  const departments = new Set(items.map(item => item.responsible_department).filter(Boolean));
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="needs-review"]', items.filter(item => item.review_status === 'needs_policy_review').length);
  setText('[data-stat="departments"]', departments.size);
  setText('[data-stat="next-step"]', items.filter(item => item.recommended_next_step).length);
}

function listFromArray(items) {
  const list = document.createElement('ul');
  list.className = 'option-list';
  if (!Array.isArray(items) || !items.length) {
    const item = document.createElement('li');
    item.textContent = '待補';
    list.appendChild(item);
    return list;
  }
  items.forEach(text => {
    const item = document.createElement('li');
    item.textContent = valueOrPending(text);
    list.appendChild(item);
  });
  return list;
}

function makeDraftCard(item) {
  const card = document.createElement('article');
  card.className = 'card draft-card';

  const title = document.createElement('h3');
  title.textContent = valueOrPending(item.issue_title);

  const badges = document.createElement('div');
  badges.className = 'badge-row';
  badges.appendChild(badge(item.responsible_department));
  badges.appendChild(badge(item.review_status, 'purple'));
  badges.appendChild(badge(item.public_use_status, 'orange'));

  const problem = document.createElement('p');
  problem.className = 'summary-text';
  problem.textContent = valueOrPending(item.problem_statement);

  const rootTitle = document.createElement('strong');
  rootTitle.textContent = '可能真因';
  const roots = listFromArray(item.possible_root_causes);

  const optionTitle = document.createElement('strong');
  optionTitle.textContent = '政策選項';
  const options = listFromArray(item.policy_options);

  const meta = document.createElement('div');
  meta.className = 'meta-list';
  [
    ['第一步', item.first_action],
    ['下一步', item.recommended_next_step],
    ['風險提醒', item.risk_notes],
  ].forEach(([label, value]) => {
    const row = document.createElement('div');
    row.textContent = `${label}：${valueOrPending(value)}`;
    meta.appendChild(row);
  });

  const sourceBox = document.createElement('div');
  sourceBox.className = 'chip-list';
  (item.source_urls || []).forEach(url => sourceBox.appendChild(chip(url)));

  card.append(title, badges, problem, rootTitle, roots, optionTitle, options, meta, sourceBox);
  return card;
}

function renderDrafts(items) {
  const node = document.querySelector('[data-render="policy-drafts"]');
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有政策草稿候選。';
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(makeDraftCard(item)));
}

async function bootPolicyDrafts() {
  const items = await readJson('./data/policy_draft_candidates.json', []);
  renderStats(items);
  renderDrafts(items);
}

bootPolicyDrafts();
