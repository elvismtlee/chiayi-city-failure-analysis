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

function priorityLabel(priority) {
  const labels = {
    needs_metadata_review: '需補 metadata',
    medium: '中優先',
    normal: '一般',
  };
  return labels[priority] || '待判斷';
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

function renderStats(items) {
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="metadata"]', items.filter(item => item.needs_metadata_review).length);
  setText('[data-stat="not-started"]', items.filter(item => item.transcript_status === 'not_started').length);
}

function renderQueue(items) {
  const node = document.querySelector('[data-render="video-review-queue"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有待轉錄候選。</p>';
    return;
  }

  node.innerHTML = items.map(item => `
    <article class="card queue-card">
      <h3>${escapeHtml(item.video_title)} <span class="pill ${escapeHtml(item.priority)}">${priorityLabel(item.priority)}</span></h3>
      <div class="meta">
        <div><b>議員</b>${escapeHtml(item.councilor_name || '待補')}</div>
        <div><b>日期</b>${escapeHtml(item.meeting_date || '待補')}</div>
        <div><b>屆次</b>${escapeHtml(item.council_term)}</div>
        <div><b>會期</b>${escapeHtml(item.session_name)}</div>
        <div><b>平台</b>${escapeHtml(item.video_platform)}</div>
        <div><b>狀態</b>${escapeHtml(item.transcript_status)} / ${escapeHtml(item.review_status)}</div>
        <div><b>議題初判</b>${escapeHtml(item.topic_guess || '待分類')}</div>
        <div><b>建議動作</b>${escapeHtml(item.recommended_action)}</div>
      </div>
      <div class="query">影音連結：${escapeHtml(item.video_url || '缺少影音連結')}</div>
      <p>${escapeHtml(item.notes)}</p>
    </article>
  `).join('');
}

async function bootVideoReview() {
  const items = await readJson('./data/transcript_review_queue.json', []);
  renderStats(items);
  renderQueue(items);
}

bootVideoReview();
