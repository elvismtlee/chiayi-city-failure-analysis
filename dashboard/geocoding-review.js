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
  const labels = { high: '高優先', medium: '中優先', low: '低優先' };
  return labels[priority] || '待判斷';
}

function reviewMethodLabel(method) {
  const labels = {
    manual_review_with_public_map: '人工比對公開地圖',
  };
  return labels[method] || '人工確認';
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

function renderStats(items) {
  setText('[data-stat="total"]', items.length);
  setText('[data-stat="high"]', items.filter(item => item.priority === 'high').length);
  setText('[data-stat="prototype"]', items.filter(item => item.geo_precision === 'prototype').length);
}

function renderQueue(items) {
  const node = document.querySelector('[data-render="geocoding-queue"]');
  if (!node) return;
  if (!items.length) {
    node.innerHTML = '<p class="empty">目前沒有需要人工審核的座標候選。</p>';
    return;
  }

  node.innerHTML = items.map(item => `
    <article class="card queue-card">
      <h3>${escapeHtml(item.place_name)} <span class="pill ${escapeHtml(item.priority)}">${priorityLabel(item.priority)}</span></h3>
      <div class="meta">
        <div><b>行政區</b>${escapeHtml(item.district)}</div>
        <div><b>議題</b>${escapeHtml(item.category)}</div>
        <div><b>局處</b>${escapeHtml(item.department)}</div>
        <div><b>分數</b>${Number(item.score || 0)}</div>
        <div><b>目前座標</b>${Number(item.current_lat || 0)}, ${Number(item.current_lng || 0)}</div>
        <div><b>狀態</b>${escapeHtml(item.geo_precision)} / ${escapeHtml(item.review_status)}</div>
        <div><b>審核方式</b>${reviewMethodLabel(item.suggested_review_method)}</div>
        <div><b>method</b>${escapeHtml(item.suggested_review_method || 'manual_review_with_public_map')}</div>
      </div>
      <div class="query">建議查詢：${escapeHtml(item.suggested_query)}</div>
      <p>${escapeHtml(item.notes)}</p>
    </article>
  `).join('');
}

async function bootGeocodingReview() {
  const items = await readJson('./data/geocoding_review_queue.json', []);
  renderStats(items);
  renderQueue(items);
}

bootGeocodingReview();
