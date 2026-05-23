async function loadJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(path);
    return await response.json();
  } catch (error) {
    console.warn('Use fallback:', path, error);
    return fallback;
  }
}

function renderSourcesTable(items) {
  const node = document.querySelector('[data-render="sources"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <tr>
      <td>${item.source_name}</td>
      <td>${item.source_type}</td>
      <td><span class="pill">${item.status}</span></td>
      <td>${item.latest_update}</td>
      <td>${item.record_count}</td>
      <td><a href="${item.source_url}" target="_blank" rel="noopener">來源</a></td>
      <td>${item.notes}</td>
    </tr>
  `).join('');
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

function valueOrPending(value) {
  return value === undefined || value === null || value === '' ? '待補' : String(value);
}

function renderCrawlerStatus(report) {
  const note = document.querySelector('[data-render="pipeline-note"]');
  if (!note) return;

  if (!report || !report.public_use_status) {
    setText('[data-pipeline="status"]', '已建立');
    setText('[data-pipeline="scope"]', 'metadata only');
    setText('[data-pipeline="files"]', '尚未產出');
    setText('[data-pipeline="records"]', '0');
    note.innerHTML = '<strong>嘉義市議會公開資料 crawler 已進入程式碼主線。</strong>目前尚未偵測到正式抓取報告，代表尚未將 live crawl 產出提交到 dashboard。下一步是手動執行 crawler、人工審核輸出，再決定是否接入儀表板。';
    return;
  }

  const outputFiles = report.output_files || [];
  const recordCount = outputFiles.reduce((sum, item) => sum + Number(item.record_count || 0), 0);
  setText('[data-pipeline="status"]', report.public_use_status === 'internal_crawl_report' ? '已有報告' : '待確認');
  setText('[data-pipeline="scope"]', report.crawl_scope || 'metadata only');
  setText('[data-pipeline="files"]', String(outputFiles.length));
  setText('[data-pipeline="records"]', String(recordCount));
  note.innerHTML = `<strong>已讀取 crawler 報告。</strong>最近抓取時間：${report.crawled_at || report.generated_at || '未標示'}。此資料仍為 internal metadata，需要人工審核後才可對外使用。`;
}

function getCyccCount(report, pattern) {
  const outputFiles = report?.output_files || [];
  const match = outputFiles.find(item => String(item.path || '').includes(pattern));
  return Number(match?.record_count || 0);
}

function renderCyccReview(report) {
  const note = document.querySelector('[data-render="cycc-note"]');
  if (!note) return;

  if (!report || !report.public_use_status) {
    setText('[data-cycc="minutes"]', '0');
    setText('[data-cycc="videos"]', '0');
    setText('[data-cycc="total"]', '0');
    setText('[data-cycc="status"]', '待抓取');
    note.innerHTML = '<strong>尚未讀取到 CYCC crawl report。</strong>請先執行 CYCC Manual Crawl，並將審核後 summary report 接入 dashboard/data。';
    return;
  }

  const minutes = getCyccCount(report, 'cycc_minutes_metadata.csv');
  const videos = getCyccCount(report, 'cycc_question_video_metadata.csv');
  const total = minutes + videos;
  setText('[data-cycc="minutes"]', String(minutes));
  setText('[data-cycc="videos"]', String(videos));
  setText('[data-cycc="total"]', String(total));
  setText('[data-cycc="status"]', report.public_use_status === 'internal_crawl_report' ? '內部審核' : '待確認');
  note.innerHTML = `<strong>已接入嘉義市議會公開資料 summary report。</strong>最近抓取時間：${report.crawled_at || '未標示'}。目前只顯示內部 metadata 統計，不公開 raw CSV，不自動發布，不產生競選文案。人工審核狀態：${report.manual_review_required ? 'required' : 'not marked'}。`;
}

function normalizeCyccMetadata(minutesPayload, videosPayload) {
  const minutes = Array.isArray(minutesPayload?.items) ? minutesPayload.items : [];
  const videos = Array.isArray(videosPayload?.items) ? videosPayload.items : [];
  return [...minutes, ...videos];
}

function filterCyccMetadata(items) {
  const query = String(document.querySelector('#cyccSearch')?.value || '').trim().toLowerCase();
  const type = String(document.querySelector('#cyccType')?.value || 'all');
  return items.filter(item => {
    const title = String(item.title || '').toLowerCase();
    const matchQuery = !query || title.includes(query);
    const matchType = type === 'all' || item.source_type === type;
    return matchQuery && matchType;
  });
}

function renderCyccMetadataTable(items) {
  const tbody = document.querySelector('[data-render="cycc-table"]');
  const summary = document.querySelector('[data-render="cycc-summary"]');
  if (!tbody) return;
  tbody.textContent = '';
  if (summary) summary.textContent = `目前顯示 ${items.length} 筆逐筆 metadata`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 6;
    cell.textContent = '目前沒有符合條件的 metadata。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const sourceType = document.createElement('td');
    const sourcePill = document.createElement('span');
    sourcePill.className = 'pill';
    sourcePill.textContent = valueOrPending(item.source_type);
    sourceType.appendChild(sourcePill);

    const title = document.createElement('td');
    title.textContent = valueOrPending(item.title);

    const date = document.createElement('td');
    date.textContent = valueOrPending(item.date || item.published_at || item.updated_at);

    const urls = document.createElement('td');
    const sourceLink = document.createElement('a');
    sourceLink.href = valueOrPending(item.source_url);
    sourceLink.target = '_blank';
    sourceLink.rel = 'noopener';
    sourceLink.textContent = 'source';
    urls.appendChild(sourceLink);
    if (item.detail_url && item.detail_url !== item.source_url) {
      urls.appendChild(document.createTextNode(' / '));
      const detailLink = document.createElement('a');
      detailLink.href = item.detail_url;
      detailLink.target = '_blank';
      detailLink.rel = 'noopener';
      detailLink.textContent = 'detail';
      urls.appendChild(detailLink);
    }

    const viewCount = document.createElement('td');
    viewCount.textContent = valueOrPending(item.view_count);

    const reviewStatus = document.createElement('td');
    reviewStatus.textContent = valueOrPending(item.review_status);

    row.append(sourceType, title, date, urls, viewCount, reviewStatus);
    tbody.appendChild(row);
  });
}

function setupCyccReviewTable(minutesPayload, videosPayload) {
  const allItems = normalizeCyccMetadata(minutesPayload, videosPayload);
  const render = () => renderCyccMetadataTable(filterCyccMetadata(allItems));
  const searchInput = document.querySelector('#cyccSearch');
  const typeSelect = document.querySelector('#cyccType');
  if (searchInput) searchInput.addEventListener('input', render);
  if (typeSelect) typeSelect.addEventListener('change', render);
  render();
}

function renderReports(items) {
  const node = document.querySelector('[data-render="reports"]');
  if (!node) return;
  node.innerHTML = items.map(item => `
    <article class="card">
      <div class="eyebrow">${item.week_start} - ${item.week_end}</div>
      <h3>${item.title}</h3>
      <p>${item.summary}</p>
      <p><b>主要議題：</b>${item.top_issue}</p>
      <a class="btn" href="${item.report_url}">查看週報</a>
    </article>
  `).join('');
}

async function bootSitePages() {
  const page = document.body.dataset.page;
  if (page === 'sources') {
    const sources = await loadJson('./data/data_sources.json', []);
    renderSourcesTable(sources);
    const crawlerReport = await loadJson('./data/cycc_public_records_crawl_report.json', null);
    renderCrawlerStatus(crawlerReport);
  }
  if (page === 'cycc-review') {
    const [crawlerReport, minutesPayload, videosPayload] = await Promise.all([
      loadJson('./data/cycc_public_records_crawl_report.json', null),
      loadJson('./data/cycc_minutes_metadata.json', { items: [] }),
      loadJson('./data/cycc_question_video_metadata.json', { items: [] }),
    ]);
    renderCyccReview(crawlerReport);
    setupCyccReviewTable(minutesPayload, videosPayload);
  }
  if (page === 'reports') {
    const reports = await loadJson('./data/reports_index.json', []);
    renderReports(reports);
  }
}

bootSitePages();
