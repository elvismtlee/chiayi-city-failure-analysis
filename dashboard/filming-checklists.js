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
  return String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

function renderList(items) {
  return `<ul>${(items || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

function renderStats(items) {
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="needs-review"]', items.filter(item => item.review_status === 'needs_filming_review').length);
  setText('[data-stat="minutes"]', items.reduce((sum, item) => sum + (Number(item.estimated_minutes) || 0), 0));
}

function renderCards(items) {
  const node = document.querySelector('[data-render="filming-checklists"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有可顯示的拍攝清單。</p>';
    return;
  }
  node.innerHTML = items.map(item => `
    <article class="card draft-card">
      <h3>${escapeHtml(item.issue_title)} <span>${escapeHtml(item.location_type)}</span></h3>
      <p class="excerpt">${escapeHtml(item.shooting_goal)}</p>
      <section><h4>Scene tasks</h4>${renderList(item.scene_tasks)}</section>
      <p><b>A-roll</b><br>${escapeHtml(item.a_roll_notes)}</p>
      <p><b>B-roll</b><br>${escapeHtml(item.b_roll_notes)}</p>
      <section><h4>Props</h4>${renderList(item.props_needed)}</section>
      <p><b>Estimated minutes</b><br>${escapeHtml(item.estimated_minutes)}</p>
      <p class="muted">${escapeHtml(item.risk_notes)}</p>
    </article>
  `).join('');
}

async function bootFilmingChecklists() {
  const items = await readJson('./data/filming_checklists.json', []);
  renderStats(items);
  renderCards(items);
}

bootFilmingChecklists();
