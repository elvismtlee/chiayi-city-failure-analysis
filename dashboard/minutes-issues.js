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
    reviewed: '已審核範例',
    internal_reviewed_sample: '內部審核範例',
    sample_only: 'sample_only',
    manual_policy_review: '人工政策審核',
  };
  return labels[status] || status || '待確認';
}

function renderStats(items) {
  const departments = new Set(items.map(item => item.department).filter(Boolean));
  const keywords = new Set(items.flatMap(item => item.issue_keywords || []).filter(Boolean));
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="departments"]', departments.size);
  setText('[data-stat="keywords"]', keywords.size);
  setText('[data-stat="sample-only"]', items.filter(item => item.confidence_level === 'sample_only').length);
}

function renderKeywords(keywords) {
  return (keywords || []).map(keyword => `<span class="pill">${escapeHtml(keyword)}</span>`).join('');
}

function renderCandidates(items) {
  const node = document.querySelector('[data-render="minutes-issue-candidates"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有可顯示的會議紀錄議題候選。</p>';
    return;
  }
  node.innerHTML = items.map(item => `
    <article class="card candidate-card">
      <h3>${escapeHtml(item.issue_title)} <span class="pill status">${statusLabel(item.confidence_level)}</span></h3>
      <div class="meta">
        <div><b>局處</b>${escapeHtml(item.department || '待補')}</div>
        <div><b>日期</b>${escapeHtml(item.meeting_date || '待補')}</div>
        <div><b>review_status</b>${statusLabel(item.review_status)}</div>
        <div><b>建議後續</b>${statusLabel(item.recommended_follow_up)}</div>
      </div>
      <div class="keywords">${renderKeywords(item.issue_keywords)}</div>
      <p class="excerpt">${escapeHtml(item.issue_summary)}</p>
      <p><a href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener">公開來源連結</a></p>
      <p class="muted">${escapeHtml(item.notes)}</p>
    </article>
  `).join('');
}

async function bootMinutesIssues() {
  const items = await readJson('./data/cycc_minutes_issue_candidates.json', []);
  renderStats(items);
  renderCandidates(items);
}

bootMinutesIssues();
