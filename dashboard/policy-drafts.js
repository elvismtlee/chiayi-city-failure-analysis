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

function renderList(items) {
  return `<ul>${(items || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

function renderStats(items) {
  const departments = new Set(items.map(item => item.responsible_department).filter(Boolean));
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="needs-review"]', items.filter(item => item.review_status === 'needs_policy_review').length);
  setText('[data-stat="departments"]', departments.size);
}

function renderDrafts(items) {
  const node = document.querySelector('[data-render="policy-drafts"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有可顯示的政策草稿候選。</p>';
    return;
  }
  node.innerHTML = items.map(item => `
    <article class="card draft-card">
      <h3>${escapeHtml(item.issue_title)} <span class="pill">${escapeHtml(item.public_use_status)}</span></h3>
      <p class="excerpt">${escapeHtml(item.problem_statement)}</p>
      <div class="meta">
        <div><b>局處</b>${escapeHtml(item.responsible_department || '待補')}</div>
        <div><b>下一步</b>${escapeHtml(item.recommended_next_step)}</div>
        <div><b>第一步</b>${escapeHtml(item.first_action)}</div>
        <div><b>狀態</b>${escapeHtml(item.review_status)}</div>
      </div>
      <section><h4>待確認可能成因</h4>${renderList(item.possible_root_causes)}</section>
      <section><h4>內部可討論方向</h4>${renderList(item.policy_options)}</section>
      <p class="muted">${escapeHtml(item.risk_notes)}</p>
    </article>
  `).join('');
}

async function bootPolicyDrafts() {
  const items = await readJson('./data/policy_draft_candidates.json', []);
  renderStats(items);
  renderDrafts(items);
}

bootPolicyDrafts();
