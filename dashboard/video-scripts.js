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
  setText('[data-stat="needs-review"]', items.filter(item => item.review_status === 'needs_video_review').length);
  setText('[data-stat="solo"]', items.filter(item => (item.scene_plan || []).every(step => step.includes('一人可拍攝'))).length);
}

function renderCards(items) {
  const node = document.querySelector('[data-render="video-scripts"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有可顯示的短影音腳本草稿。</p>';
    return;
  }
  node.innerHTML = items.map(item => `
    <article class="card draft-card">
      <h3>${escapeHtml(item.issue_title)}</h3>
      <p class="excerpt">${escapeHtml(item.hook)}</p>
      <p><b>Opening</b><br>${escapeHtml(item.opening_line)}</p>
      <section><h4>Scene plan</h4>${renderList(item.scene_plan)}</section>
      <section><h4>Voiceover</h4><p>${escapeHtml(item.voiceover)}</p></section>
      <section><h4>Subtitles</h4>${renderList(item.subtitle_lines)}</section>
      <p><b>CTA</b><br>${escapeHtml(item.call_to_action)}</p>
      <p class="muted">${escapeHtml(item.risk_notes)}</p>
    </article>
  `).join('');
}

async function bootVideoScripts() {
  const items = await readJson('./data/short_video_script_drafts.json', []);
  renderStats(items);
  renderCards(items);
}

bootVideoScripts();
