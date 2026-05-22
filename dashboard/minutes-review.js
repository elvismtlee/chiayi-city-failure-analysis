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

function statusLabel(status) {
  const labels = {
    parsed_from_fixture: 'fixture 解析',
    unreviewed: '未審核',
    needs_metadata_review: '需補 metadata',
    normal: '一般',
    manual_minutes_review: '人工會議紀錄審核',
  };
  return labels[status] || status || '待確認';
}

function renderStats(items) {
  const departments = new Set(items.map(item => item.department).filter(Boolean));
  const parserStatuses = new Set(items.map(item => item.parser_status).filter(Boolean));
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="pending"]', items.filter(item => item.review_status === 'unreviewed').length);
  setText('[data-stat="departments"]', departments.size);
  setText('[data-stat="parser-statuses"]', parserStatuses.size ? Array.from(parserStatuses).map(statusLabel).join('、') : '–');
}

function renderKeywords(keywords) {
  return (keywords || []).map(keyword => `<span class="pill">${escapeHtml(keyword)}</span>`).join('');
}

function renderQueue(items) {
  const node = document.querySelector('[data-render="minutes-review-queue"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有可顯示的會議紀錄審核候選。</p>';
    return;
  }
  node.innerHTML = items.map(item => `
    <article class="card queue-card">
      <h3>${escapeHtml(item.meeting_name)} <span class="pill review">${statusLabel(item.review_priority)}</span></h3>
      <div class="meta">
        <div><b>日期</b>${escapeHtml(item.meeting_date || '待補')}</div>
        <div><b>議員</b>${escapeHtml(item.councilor_name || '待補')}</div>
        <div><b>局處</b>${escapeHtml(item.department || '待補')}</div>
        <div><b>議程</b>${escapeHtml(item.agenda_item || '待補')}</div>
        <div><b>parser_status</b>${statusLabel(item.parser_status)}</div>
        <div><b>review_status</b>${statusLabel(item.review_status)}</div>
        <div><b>建議動作</b>${statusLabel(item.recommended_action)}</div>
        <div><b>queue_id</b>${escapeHtml(item.queue_id)}</div>
      </div>
      <div class="keywords">${renderKeywords(item.issue_keywords)}</div>
      <p class="excerpt">${escapeHtml(item.raw_text_excerpt)}</p>
      <p><a href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener">公開來源連結</a></p>
      <p class="muted">${escapeHtml(item.notes)}</p>
    </article>
  `).join('');
}

async function bootMinutesReview() {
  const items = await readJson('./data/cycc_minutes_review_queue.json', []);
  renderStats(items);
  renderQueue(items);
}

bootMinutesReview();
