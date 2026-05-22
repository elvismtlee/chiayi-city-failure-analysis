async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    const area = document.querySelector('[data-render="table-area"]');
    const summary = document.querySelector('[data-render="result-summary"]');
    if (summary) summary.textContent = `讀取 metadata 資料失敗：${error.message}`;
    if (area) {
      area.textContent = '';
      const empty = document.createElement('p');
      empty.className = 'empty';
      empty.textContent = `讀取 metadata 資料失敗：${error.message}`;
      area.appendChild(empty);
    }
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

function makeLink(url) {
  if (!url) return document.createTextNode('待補');
  const link = document.createElement('a');
  link.href = url;
  link.target = '_blank';
  link.rel = 'noopener';
  link.textContent = url;
  return link;
}

function formatVolume(item) {
  if (item.view_count !== undefined && item.view_count !== null && item.view_count !== '') {
    return `${item.view_count}`;
  }
  if (item.record_count !== undefined && item.record_count !== null && item.record_count !== '') {
    return `${item.record_count}`;
  }
  return '待補';
}

function makeTable(items) {
  const table = document.createElement('table');
  table.className = 'metadata-table';
  const thead = document.createElement('thead');
  const headRow = document.createElement('tr');
  ['source_type', 'title', 'date', 'source_url / detail_url', 'record_count / view_count', 'review_status'].forEach(text => {
    const th = document.createElement('th');
    th.textContent = text;
    headRow.appendChild(th);
  });
  thead.appendChild(headRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  items.forEach(item => {
    const row = document.createElement('tr');

    const sourceType = document.createElement('td');
    const sourceBadge = document.createElement('span');
    sourceBadge.className = 'badge';
    sourceBadge.textContent = valueOrPending(item.source_type);
    sourceType.appendChild(sourceBadge);

    const titleCell = document.createElement('td');
    titleCell.className = 'title-cell';
    const title = document.createElement('strong');
    title.textContent = valueOrPending(item.title);
    const note = document.createElement('small');
    note.textContent = item.source_type === 'minutes'
      ? valueOrPending(item.department)
      : `${valueOrPending(item.councilor_name)} / ${valueOrPending(item.session_name)}`;
    titleCell.append(title, note);

    const date = document.createElement('td');
    date.textContent = valueOrPending(item.date);

    const urlCell = document.createElement('td');
    const sourceWrap = document.createElement('div');
    sourceWrap.appendChild(makeLink(item.source_url));
    const detailWrap = document.createElement('div');
    detailWrap.appendChild(makeLink(item.detail_url));
    urlCell.append(sourceWrap, detailWrap);

    const volume = document.createElement('td');
    volume.textContent = formatVolume(item);

    const review = document.createElement('td');
    const reviewBadge = document.createElement('span');
    reviewBadge.className = 'badge manual';
    reviewBadge.textContent = valueOrPending(item.review_status);
    review.appendChild(reviewBadge);

    row.append(sourceType, titleCell, date, urlCell, volume, review);
    tbody.appendChild(row);
  });

  table.appendChild(tbody);
  return table;
}

function renderTable(items) {
  const area = document.querySelector('[data-render="table-area"]');
  const summary = document.querySelector('[data-render="result-summary"]');
  if (!area) return;
  area.textContent = '';
  if (summary) summary.textContent = `目前顯示 ${items.length} 筆 internal metadata。`;
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有符合條件的 metadata。所有資料仍需人工審核後才能對外引用。';
    area.appendChild(empty);
    return;
  }
  area.appendChild(makeTable(items));
}

function normalizeItems(minutesPayload, videosPayload) {
  const minutes = Array.isArray(minutesPayload.items) ? minutesPayload.items : [];
  const videos = Array.isArray(videosPayload.items) ? videosPayload.items : [];
  return [...minutes, ...videos];
}

function applyFilters(items) {
  const searchInput = document.querySelector('#search-input');
  const filterSelect = document.querySelector('#source-filter');
  const query = (searchInput?.value || '').trim().toLowerCase();
  const sourceType = filterSelect?.value || 'all';
  return items.filter(item => {
    const matchesType = sourceType === 'all' || item.source_type === sourceType;
    const matchesQuery = !query || String(item.title || '').toLowerCase().includes(query);
    return matchesType && matchesQuery;
  });
}

function bindFilters(items) {
  const render = () => renderTable(applyFilters(items));
  document.querySelector('#search-input')?.addEventListener('input', render);
  document.querySelector('#source-filter')?.addEventListener('change', render);
  render();
}

function renderStats(minutesPayload, videosPayload, report) {
  const minutesCount = Number(minutesPayload.total_count || 0);
  const videosCount = Number(videosPayload.total_count || 0);
  const totalCount = minutesCount + videosCount;
  const latestCrawl = report.crawled_at || minutesPayload.latest_crawl_at || videosPayload.latest_crawl_at || '';
  setText('[data-stat="minutes-count"]', minutesCount);
  setText('[data-stat="videos-count"]', videosCount);
  setText('[data-stat="total-count"]', totalCount);
  setText('[data-stat="latest-crawl"]', latestCrawl);
  setText('[data-stat="source-name"]', report.source_name || minutesPayload.source_name || '嘉義市議會公開資料');
}

async function bootCyccMetadataPage() {
  const [minutesPayload, videosPayload, report] = await Promise.all([
    readJson('./data/cycc_minutes_metadata.json', { items: [], total_count: 0 }),
    readJson('./data/cycc_question_video_metadata.json', { items: [], total_count: 0 }),
    readJson('./data/cycc_public_records_crawl_report.json', {}),
  ]);

  renderStats(minutesPayload, videosPayload, report);
  bindFilters(normalizeItems(minutesPayload, videosPayload));
}

bootCyccMetadataPage();
