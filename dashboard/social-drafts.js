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

function renderStats(items) {
  const channels = items.reduce((counts, item) => {
    counts[item.channel] = (counts[item.channel] || 0) + 1;
    return counts;
  }, {});
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="needs-review"]', items.filter(item => item.review_status === 'needs_communication_review').length);
  setText('[data-stat="channels"]', Object.entries(channels).map(([key, count]) => `${key}: ${count}`).join(' / ') || '0');
}

function renderCards(items) {
  const node = document.querySelector('[data-render="social-drafts"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有可顯示的社群文案草稿。</p>';
    return;
  }
  node.innerHTML = items.map(item => `
    <article class="card draft-card">
      <h3><span>${escapeHtml(item.headline)}</span><b>${escapeHtml(item.channel)}</b></h3>
      <p>${escapeHtml(item.body)}</p>
      <p class="excerpt">${escapeHtml(item.short_version)}</p>
      <div class="meta"><div><b>Call to action</b>${escapeHtml(item.call_to_action)}</div><div><b>狀態</b>${escapeHtml(item.review_status)}</div></div>
      <p class="muted">${escapeHtml(item.risk_notes)}</p>
      <ul>${(item.source_urls || []).map(url => `<li><a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(url)}</a></li>`).join('')}</ul>
    </article>
  `).join('');
}

async function bootSocialDrafts() {
  const items = await readJson('./data/social_post_drafts.json', []);
  renderStats(items);
  renderCards(items);
}

bootSocialDrafts();
