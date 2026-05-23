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

function clearChildren(node) {
  if (!node) return;
  while (node.firstChild) node.removeChild(node.firstChild);
}

function appendText(node, text) {
  node.appendChild(document.createTextNode(text));
}

function createCell(text, className = '') {
  const cell = document.createElement('td');
  if (className) cell.className = className;
  cell.textContent = valueOrPending(text);
  return cell;
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

function topicGroupLabel(topicGroup) {
  const labels = {
    traffic_parking: '交通停車',
    social_welfare: '社福長照',
    culture_events: '文化活動',
    public_works_environment: '工程環境',
    complaints_service: '1999 / 服務入口',
  };
  return labels[topicGroup] || valueOrPending(topicGroup);
}

function readinessLevelClass(level) {
  if (level === 'blocked') return 'pill blocked';
  if (level === 'medium') return 'pill medium';
  return 'pill';
}

function reviewPriorityClass(priority) {
  if (priority === 'P3') return 'pill p3';
  if (priority === 'P2') return 'pill p2';
  return 'pill';
}

function crawlerSpecStatusClass(status) {
  if (status === 'blocked') return 'pill risk';
  if (status === 'license_review_required' || status === 'parser_design_required') return 'pill warn';
  return 'pill';
}

function approvalGateStatusClass(status) {
  if (status === 'blocked' || status === 'needs_risk_review') return 'pill risk';
  if (status === 'needs_license_review' || status === 'needs_format_review') return 'pill warn';
  return 'pill';
}

function engineeringReviewStatusClass(status) {
  if (status === 'rejected' || status === 'blocked_by_risk_review') return 'pill risk';
  if (
    status === 'blocked_by_source_review' ||
    status === 'blocked_by_license_review' ||
    status === 'blocked_by_format_review'
  ) return 'pill warn';
  return 'pill';
}

function setOpenDataKpi(payload) {
  const counts = payload?.topic_groups || {};
  setText('[data-open-data="total"]', String(payload?.total_count || 0));
  setText('[data-open-data="traffic"]', String(counts.traffic_parking || 0));
  setText('[data-open-data="social"]', String(counts.social_welfare || 0));
  setText('[data-open-data="culture"]', String(counts.culture_events || 0));
  setText('[data-open-data="works"]', String(counts.public_works_environment || 0));
  setText('[data-open-data="complaints"]', String(counts.complaints_service || 0));
  setText('[data-render="open-data-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataInventoryNote(payload) {
  const note = document.querySelector('[data-render="open-data-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是第二批真實資料來源盤點。';
  note.appendChild(strong);
  appendText(
    note,
    ` 來源數：${payload?.total_count || 0}。來源：嘉義市政府與官方公開資料入口。狀態：internal_url_inventory，manual review required。這一階段只審核 URL，不啟動 live crawler，不抓個資、不抓私人陳情全文、不自動發布，no auto publish。`,
  );
}

function filterOpenDataInventory(items) {
  const query = String(document.querySelector('#openDataSearch')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataTopicGroup')?.value || 'all');
  return items.filter(item => {
    const title = String(item.title || '').toLowerCase();
    const owner = String(item.source_owner || '').toLowerCase();
    const matchesQuery = !query || title.includes(query) || owner.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    return matchesQuery && matchesGroup;
  });
}

function renderOpenDataInventoryTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-table"]');
  const summary = document.querySelector('[data-render="open-data-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆候選來源`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 9;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的候選來源。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const topicCell = document.createElement('td');
    const pill = document.createElement('span');
    pill.className = 'pill';
    pill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(pill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const typeCell = createCell(item.source_type);

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    const formatCell = createCell(item.expected_format);
    const cadenceCell = createCell(item.update_cadence);
    const reviewCell = createCell(item.review_status);
    const useCell = createCell(item.dashboard_use);

    row.append(
      topicCell,
      titleCell,
      ownerCell,
      typeCell,
      urlCell,
      formatCell,
      cadenceCell,
      reviewCell,
      useCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataInventory(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  setOpenDataKpi(payload);
  renderOpenDataInventoryNote(payload);

  const render = () => renderOpenDataInventoryTable(filterOpenDataInventory(items), items.length);
  const searchInput = document.querySelector('#openDataSearch');
  const groupSelect = document.querySelector('#openDataTopicGroup');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  render();
}

function setOpenDataReviewKpi(payload) {
  const counts = payload?.topic_groups || {};
  const items = Array.isArray(payload?.items) ? payload.items : [];
  setText('[data-open-review="total"]', String(payload?.total_count || 0));
  setText(
    '[data-open-review="needs-review"]',
    String(items.filter(item => item.url_review_status === 'needs_manual_url_review').length),
  );
  setText(
    '[data-open-review="crawler-candidate"]',
    String(items.filter(item => item.crawler_candidate === true).length),
  );
  setText(
    '[data-open-review="do-not-crawl"]',
    String(items.filter(item => item.url_review_status === 'do_not_crawl').length),
  );
  setText('[data-open-review="traffic"]', String(counts.traffic_parking || 0));
  setText('[data-open-review="complaints"]', String(counts.complaints_service || 0));
  setText('[data-render="open-data-review-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataReviewNote(payload) {
  const note = document.querySelector('[data-render="open-data-review-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是人工審核佇列。';
  note.appendChild(strong);
  appendText(
    note,
    ` 總數：${payload?.total_count || 0}。狀態：internal_url_review_queue。這不是 live crawler，不抓個資，不抓私人陳情全文，不自動發布。crawler_candidate 只是候選，不代表已批准爬取。`,
  );
}

function filterOpenDataReviewQueue(items) {
  const query = String(document.querySelector('#openDataReviewSearch')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataReviewTopicGroup')?.value || 'all');
  const status = String(document.querySelector('#openDataReviewStatus')?.value || 'all');
  const priority = String(document.querySelector('#openDataReviewPriority')?.value || 'all');
  return items.filter(item => {
    const haystack = [
      String(item.title || ''),
      String(item.source_owner || ''),
      String(item.review_notes || ''),
    ].join(' ').toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    const matchesStatus = status === 'all' || item.url_review_status === status;
    const matchesPriority = priority === 'all' || item.crawler_priority === priority;
    return matchesQuery && matchesGroup && matchesStatus && matchesPriority;
  });
}

function renderOpenDataReviewTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-review-table"]');
  const summary = document.querySelector('[data-render="open-data-review-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆人工審核佇列`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 11;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的審核項目。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const topicCell = document.createElement('td');
    const topicPill = document.createElement('span');
    topicPill.className = 'pill';
    topicPill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(topicPill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    const formatCell = createCell(item.expected_format);
    const licenseCell = createCell(item.license_status);
    const statusCell = createCell(item.url_review_status);
    const reachabilityCell = createCell(item.source_reachability);
    const candidateCell = createCell(item.crawler_candidate ? 'true' : 'false');
    const priorityCell = createCell(item.crawler_priority);
    const notesCell = createCell(item.review_notes, 'compact');

    row.append(
      topicCell,
      titleCell,
      ownerCell,
      urlCell,
      formatCell,
      licenseCell,
      statusCell,
      reachabilityCell,
      candidateCell,
      priorityCell,
      notesCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataReviewQueue(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  setOpenDataReviewKpi(payload);
  renderOpenDataReviewNote(payload);

  const render = () => renderOpenDataReviewTable(filterOpenDataReviewQueue(items), items.length);
  const searchInput = document.querySelector('#openDataReviewSearch');
  const groupSelect = document.querySelector('#openDataReviewTopicGroup');
  const statusSelect = document.querySelector('#openDataReviewStatus');
  const prioritySelect = document.querySelector('#openDataReviewPriority');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  if (prioritySelect) prioritySelect.addEventListener('change', render);
  render();
}

function setOpenDataReadinessKpi(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  const levels = payload?.readiness_levels || {};
  const groups = payload?.topic_groups || {};
  const highRiskCount = items.filter(
    item => item.readiness_level === 'blocked' || Number(item?.score_breakdown?.crawler_risk_score || 0) >= 5,
  ).length;
  setText('[data-open-readiness="total"]', String(payload?.total_count || 0));
  setText('[data-open-readiness="high"]', String(levels.high || 0));
  setText('[data-open-readiness="medium"]', String(levels.medium || 0));
  setText('[data-open-readiness="low"]', String(levels.low || 0));
  setText('[data-open-readiness="blocked"]', String(highRiskCount));
  setText('[data-open-readiness="complaints"]', String(groups.complaints_service || 0));
  setText('[data-render="open-data-readiness-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataReadinessNote(payload) {
  const note = document.querySelector('[data-render="open-data-readiness-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是 readiness report。';
  note.appendChild(strong);
  appendText(
    note,
    ` 總數：${payload?.total_count || 0}。狀態：internal_readiness_report。這不是 crawler，不啟動 live crawler，不抓個資，不抓私人陳情全文，不自動發布。readiness score 只是內部排序，不代表正式評價或結論。`,
  );
}

function filterOpenDataReadiness(items) {
  const query = String(document.querySelector('#openDataReadinessSearch')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataReadinessTopicGroup')?.value || 'all');
  const level = String(document.querySelector('#openDataReadinessLevel')?.value || 'all');
  const stage = String(document.querySelector('#openDataReadinessStage')?.value || 'all');
  return items.filter(item => {
    const haystack = [
      String(item.title || ''),
      String(item.source_owner || ''),
      String(item.readiness_notes || ''),
    ].join(' ').toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    const matchesLevel = level === 'all' || item.readiness_level === level;
    const matchesStage = stage === 'all' || item.crawler_stage === stage;
    return matchesQuery && matchesGroup && matchesLevel && matchesStage;
  });
}

function renderOpenDataReadinessTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-readiness-table"]');
  const summary = document.querySelector('[data-render="open-data-readiness-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆 readiness 排序`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 11;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的 readiness 項目。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const levelCell = document.createElement('td');
    const levelPill = document.createElement('span');
    levelPill.className = readinessLevelClass(item.readiness_level);
    levelPill.textContent = valueOrPending(item.readiness_level);
    levelCell.appendChild(levelPill);

    const scoreCell = createCell(item.readiness_score);

    const topicCell = document.createElement('td');
    const topicPill = document.createElement('span');
    topicPill.className = 'pill';
    topicPill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(topicPill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const formatCell = createCell(item.expected_format);
    const licenseCell = createCell(item.license_status);
    const cadenceCell = createCell(item.update_cadence);
    const stageCell = createCell(item.crawler_stage);
    const notesCell = createCell(item.readiness_notes, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      levelCell,
      scoreCell,
      topicCell,
      titleCell,
      ownerCell,
      formatCell,
      licenseCell,
      cadenceCell,
      stageCell,
      notesCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataReadiness(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  setOpenDataReadinessKpi(payload);
  renderOpenDataReadinessNote(payload);

  const render = () => {
    const filtered = filterOpenDataReadiness(items).sort((a, b) => {
      if (b.readiness_score !== a.readiness_score) return b.readiness_score - a.readiness_score;
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataReadinessTable(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataReadinessSearch');
  const groupSelect = document.querySelector('#openDataReadinessTopicGroup');
  const levelSelect = document.querySelector('#openDataReadinessLevel');
  const stageSelect = document.querySelector('#openDataReadinessStage');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  if (levelSelect) levelSelect.addEventListener('change', render);
  if (stageSelect) stageSelect.addEventListener('change', render);
  render();
}

function setOpenDataTop10Kpi(payload) {
  const groups = payload?.topic_groups || {};
  const priorities = payload?.review_priority_counts || {};
  const levels = payload?.readiness_levels || {};
  setText('[data-open-top10="total"]', String(payload?.total_count || 0));
  setText('[data-open-top10="p1"]', String(priorities.P1 || 0));
  setText('[data-open-top10="p2"]', String(priorities.P2 || 0));
  setText('[data-open-top10="p3"]', String(priorities.P3 || 0));
  setText('[data-open-top10="high"]', String(levels.high || 0));
  setText('[data-open-top10="complaints"]', String(groups.complaints_service || 0));
  setText('[data-render="open-data-top10-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataTop10Note(payload) {
  const note = document.querySelector('[data-render="open-data-top10-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是人工審核任務清單。';
  note.appendChild(strong);
  appendText(
    note,
    ` Top 10 總數：${payload?.total_count || 0}。狀態：internal_top10_review_tasks。這不是 crawler，不啟動 live crawler，不抓個資，不抓私人陳情全文，不自動發布。Top 10 只是內部工作排序，crawler_candidate 或 readiness_score 都不代表批准爬取。`,
  );
}

function filterOpenDataTop10Tasks(items) {
  const query = String(document.querySelector('#openDataTop10Search')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataTop10TopicGroup')?.value || 'all');
  const priority = String(document.querySelector('#openDataTop10Priority')?.value || 'all');
  const status = String(document.querySelector('#openDataTop10Status')?.value || 'all');
  return items.filter(item => {
    const haystack = [
      String(item.title || ''),
      String(item.source_owner || ''),
      String(item.next_action || ''),
      String(item.reviewer_notes || ''),
    ].join(' ').toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    const matchesPriority = priority === 'all' || item.review_priority === priority;
    const matchesStatus = status === 'all' || item.review_status === status;
    return matchesQuery && matchesGroup && matchesPriority && matchesStatus;
  });
}

function renderOpenDataTop10Table(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-top10-table"]');
  const summary = document.querySelector('[data-render="open-data-top10-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆 Top 10 任務`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 11;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的 Top 10 任務。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const priorityCell = document.createElement('td');
    const priorityPill = document.createElement('span');
    priorityPill.className = reviewPriorityClass(item.review_priority);
    priorityPill.textContent = valueOrPending(item.review_priority);
    priorityCell.appendChild(priorityPill);

    const scoreCell = createCell(item.readiness_score);

    const topicCell = document.createElement('td');
    const topicPill = document.createElement('span');
    topicPill.className = 'pill';
    topicPill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(topicPill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const formatCell = createCell(item.expected_format);
    const licenseCell = createCell(item.license_status);
    const minutesCell = createCell(item.estimated_review_minutes);
    const statusCell = createCell(item.review_status);
    const actionCell = createCell(item.next_action, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      priorityCell,
      scoreCell,
      topicCell,
      titleCell,
      ownerCell,
      formatCell,
      licenseCell,
      minutesCell,
      statusCell,
      actionCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataTop10Tasks(payload) {
  const items = Array.isArray(payload?.tasks) ? payload.tasks : [];
  setOpenDataTop10Kpi(payload);
  renderOpenDataTop10Note(payload);

  const render = () => {
    const filtered = filterOpenDataTop10Tasks(items).sort((a, b) => {
      if (a.review_priority !== b.review_priority) return String(a.review_priority).localeCompare(String(b.review_priority));
      if (b.readiness_score !== a.readiness_score) return b.readiness_score - a.readiness_score;
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataTop10Table(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataTop10Search');
  const groupSelect = document.querySelector('#openDataTop10TopicGroup');
  const prioritySelect = document.querySelector('#openDataTop10Priority');
  const statusSelect = document.querySelector('#openDataTop10Status');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  if (prioritySelect) prioritySelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  render();
}

function setOpenDataCrawlerSpecKpi(payload) {
  const fetchMethods = payload?.proposed_fetch_methods || {};
  const items = Array.isArray(payload?.specs) ? payload.specs : [];
  const groups = payload?.topic_groups || {};
  setText('[data-open-crawler-spec="total"]', String(payload?.total_count || 0));
  setText(
    '[data-open-crawler-spec="disabled"]',
    String(items.filter(item => item.crawler_execution_allowed === false).length),
  );
  setText('[data-open-crawler-spec="csv"]', String(fetchMethods.csv_download_later || 0));
  setText(
    '[data-open-crawler-spec="html"]',
    String((fetchMethods.html_page_parse_later || 0) + (fetchMethods.not_recommended || 0)),
  );
  setText(
    '[data-open-crawler-spec="high-risk"]',
    String(items.filter(item => item.personal_data_risk === 'high').length),
  );
  setText('[data-open-crawler-spec="complaints"]', String(groups.complaints_service || 0));
  setText('[data-render="open-data-crawler-spec-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataCrawlerSpecNote(payload) {
  const note = document.querySelector('[data-render="open-data-crawler-spec-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是 crawler spec 草稿。';
  note.appendChild(strong);
  appendText(
    note,
    ` 規格數：${payload?.total_count || 0}。狀態：internal_crawler_spec_drafts。這不是 crawler，不啟動 live crawler，不抓個資，不抓私人陳情全文，不自動發布。crawler_execution_allowed 永遠是 false，spec draft 不代表批准爬取。`,
  );
}

function filterOpenDataCrawlerSpecs(items) {
  const query = String(document.querySelector('#openDataCrawlerSpecSearch')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataCrawlerSpecTopicGroup')?.value || 'all');
  const status = String(document.querySelector('#openDataCrawlerSpecStatus')?.value || 'all');
  const fetchMethod = String(document.querySelector('#openDataCrawlerSpecFetchMethod')?.value || 'all');
  const risk = String(document.querySelector('#openDataCrawlerSpecRisk')?.value || 'all');
  return items.filter(item => {
    const haystack = [
      String(item.title || ''),
      String(item.source_owner || ''),
      String(item.next_action || ''),
      String(item.safety_notes || ''),
    ].join(' ').toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    const matchesStatus = status === 'all' || item.crawler_spec_status === status;
    const matchesFetchMethod = fetchMethod === 'all' || item.proposed_fetch_method === fetchMethod;
    const matchesRisk = risk === 'all' || item.personal_data_risk === risk;
    return matchesQuery && matchesGroup && matchesStatus && matchesFetchMethod && matchesRisk;
  });
}

function renderOpenDataCrawlerSpecTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-crawler-spec-table"]');
  const summary = document.querySelector('[data-render="open-data-crawler-spec-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆 crawler spec 草稿`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 10;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的 crawler spec 草稿。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const statusCell = document.createElement('td');
    const statusPill = document.createElement('span');
    statusPill.className = crawlerSpecStatusClass(item.crawler_spec_status);
    statusPill.textContent = valueOrPending(item.crawler_spec_status);
    statusCell.appendChild(statusPill);

    const topicCell = document.createElement('td');
    const topicPill = document.createElement('span');
    topicPill.className = 'pill';
    topicPill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(topicPill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const fetchCell = createCell(item.proposed_fetch_method);
    const parserCell = createCell(item.proposed_parser_type);
    const personalRiskCell = createCell(item.personal_data_risk);
    const complaintRiskCell = createCell(item.private_complaint_risk);
    const actionCell = createCell(item.next_action, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      statusCell,
      topicCell,
      titleCell,
      ownerCell,
      fetchCell,
      parserCell,
      personalRiskCell,
      complaintRiskCell,
      actionCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataCrawlerSpecs(payload) {
  const items = Array.isArray(payload?.specs) ? payload.specs : [];
  setOpenDataCrawlerSpecKpi(payload);
  renderOpenDataCrawlerSpecNote(payload);

  const render = () => {
    const filtered = filterOpenDataCrawlerSpecs(items).sort((a, b) => {
      if (a.personal_data_risk !== b.personal_data_risk) return String(b.personal_data_risk).localeCompare(String(a.personal_data_risk));
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataCrawlerSpecTable(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataCrawlerSpecSearch');
  const groupSelect = document.querySelector('#openDataCrawlerSpecTopicGroup');
  const statusSelect = document.querySelector('#openDataCrawlerSpecStatus');
  const fetchMethodSelect = document.querySelector('#openDataCrawlerSpecFetchMethod');
  const riskSelect = document.querySelector('#openDataCrawlerSpecRisk');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  if (fetchMethodSelect) fetchMethodSelect.addEventListener('change', render);
  if (riskSelect) riskSelect.addEventListener('change', render);
  render();
}

function setOpenDataHumanReviewKpi(payload) {
  const reviewCounts = payload?.review_status_counts || {};
  const gateCounts = payload?.approval_gate_status_counts || {};
  const items = Array.isArray(payload?.records) ? payload.records : [];
  setText('[data-open-human-review="total"]', String(payload?.total_count || 0));
  setText('[data-open-human-review="not-started"]', String(reviewCounts.not_started || 0));
  setText('[data-open-human-review="pending"]', String(gateCounts.pending_manual_review || 0));
  setText('[data-open-human-review="ready"]', String(gateCounts.ready_for_engineering_review || 0));
  setText('[data-open-human-review="engineering"]', String(payload?.engineering_review_allowed_count || 0));
  setText(
    '[data-open-human-review="crawler-disabled"]',
    String(items.filter(item => item.crawler_execution_allowed === false).length),
  );
  setText('[data-render="open-data-human-review-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataHumanReviewNote(payload) {
  const note = document.querySelector('[data-render="open-data-human-review-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是人工審核工作簿。';
  note.appendChild(strong);
  appendText(
    note,
    ` 紀錄數：${payload?.total_count || 0}。狀態：internal_human_review_workbook。這不是 crawler，不啟動 live crawler，不抓個資，不抓私人陳情全文，不自動發布。engineering_review_allowed 預設 false，crawler_execution_allowed 永遠 false，必須人工審核後另開 PR 才能改變狀態。`,
  );
}

function filterOpenDataHumanReview(items) {
  const query = String(document.querySelector('#openDataHumanReviewSearch')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataHumanReviewTopicGroup')?.value || 'all');
  const reviewStatus = String(document.querySelector('#openDataHumanReviewStatus')?.value || 'all');
  const gateStatus = String(document.querySelector('#openDataHumanReviewGate')?.value || 'all');
  const fetchMethod = String(document.querySelector('#openDataHumanReviewFetchMethod')?.value || 'all');
  return items.filter(item => {
    const haystack = [
      String(item.title || ''),
      String(item.source_owner || ''),
      String(item.next_action || ''),
      String(item.reviewer_notes || ''),
    ].join(' ').toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    const matchesReviewStatus = reviewStatus === 'all' || item.review_status === reviewStatus;
    const matchesGateStatus = gateStatus === 'all' || item.approval_gate_status === gateStatus;
    const matchesFetchMethod = fetchMethod === 'all' || item.proposed_fetch_method === fetchMethod;
    return matchesQuery && matchesGroup && matchesReviewStatus && matchesGateStatus && matchesFetchMethod;
  });
}

function renderOpenDataHumanReviewTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-human-review-table"]');
  const summary = document.querySelector('[data-render="open-data-human-review-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆人工審核紀錄`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 15;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的人工審核紀錄。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const gateCell = document.createElement('td');
    const gatePill = document.createElement('span');
    gatePill.className = approvalGateStatusClass(item.approval_gate_status);
    gatePill.textContent = valueOrPending(item.approval_gate_status);
    gateCell.appendChild(gatePill);

    const reviewCell = createCell(item.review_status);

    const topicCell = document.createElement('td');
    const topicPill = document.createElement('span');
    topicPill.className = 'pill';
    topicPill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(topicPill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const methodCell = createCell(item.proposed_fetch_method);
    const sourceVerifiedCell = createCell(item.official_source_verified ? 'true' : 'false');
    const licenseCell = createCell(item.license_reviewed ? 'true' : 'false');
    const formatCell = createCell(item.format_checked ? 'true' : 'false');
    const personalCell = createCell(item.personal_data_checked ? 'true' : 'false');
    const complaintCell = createCell(item.private_complaint_checked ? 'true' : 'false');
    const engineeringCell = createCell(item.engineering_review_allowed ? 'true' : 'false');
    const crawlerCell = createCell(item.crawler_execution_allowed ? 'true' : 'false');
    const actionCell = createCell(item.next_action, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      gateCell,
      reviewCell,
      topicCell,
      titleCell,
      ownerCell,
      methodCell,
      sourceVerifiedCell,
      licenseCell,
      formatCell,
      personalCell,
      complaintCell,
      engineeringCell,
      crawlerCell,
      actionCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataHumanReview(payload) {
  const items = Array.isArray(payload?.records) ? payload.records : [];
  setOpenDataHumanReviewKpi(payload);
  renderOpenDataHumanReviewNote(payload);

  const render = () => {
    const filtered = filterOpenDataHumanReview(items).sort((a, b) => {
      if (a.approval_gate_status !== b.approval_gate_status) {
        return String(a.approval_gate_status).localeCompare(String(b.approval_gate_status));
      }
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataHumanReviewTable(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataHumanReviewSearch');
  const groupSelect = document.querySelector('#openDataHumanReviewTopicGroup');
  const statusSelect = document.querySelector('#openDataHumanReviewStatus');
  const gateSelect = document.querySelector('#openDataHumanReviewGate');
  const methodSelect = document.querySelector('#openDataHumanReviewFetchMethod');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  if (gateSelect) gateSelect.addEventListener('change', render);
  if (methodSelect) methodSelect.addEventListener('change', render);
  render();
}

function setOpenDataEngineeringReviewKpi(payload) {
  const statusCounts = payload?.engineering_review_status_counts || {};
  const items = Array.isArray(payload?.checklists) ? payload.checklists : [];
  const blockedGateCount = items.reduce((sum, item) => {
    const gateKeys = Object.keys(item).filter(key => key.endsWith('_gate'));
    return sum + gateKeys.filter(key => ['blocked', 'needs_review'].includes(String(item[key]))).length;
  }, 0);
  setText('[data-open-engineering-review="total"]', String(payload?.total_count || 0));
  setText('[data-open-engineering-review="waiting"]', String(statusCounts.waiting_for_human_review || 0));
  setText('[data-open-engineering-review="ready"]', String(statusCounts.ready_for_engineering_review || 0));
  setText('[data-open-engineering-review="engineering"]', String(payload?.engineering_review_allowed_count || 0));
  setText(
    '[data-open-engineering-review="crawler-disabled"]',
    String(items.filter(item => item.crawler_execution_allowed === false).length),
  );
  setText('[data-open-engineering-review="gates"]', String(blockedGateCount));
  setText('[data-render="open-data-engineering-review-updated"]', `最近更新：${payload?.generated_at || '未標示'}`);
}

function renderOpenDataEngineeringReviewNote(payload) {
  const note = document.querySelector('[data-render="open-data-engineering-review-note"]');
  if (!note) return;
  clearChildren(note);

  const strong = document.createElement('strong');
  strong.textContent = '這是 engineering review checklist。';
  note.appendChild(strong);
  appendText(
    note,
    ` 清單數：${payload?.total_count || 0}。狀態：internal_engineering_review_checklist。這不是 crawler，不啟動 live crawler，不對 source_url 發出網路請求，不抓個資，不抓私人陳情全文，不自動發布。engineering_review_allowed 預設 false，crawler_execution_allowed 永遠 false，必須人工審核完成後另開 PR 才能改變狀態。`,
  );
}

function filterOpenDataEngineeringReview(items) {
  const query = String(document.querySelector('#openDataEngineeringReviewSearch')?.value || '').trim().toLowerCase();
  const topicGroup = String(document.querySelector('#openDataEngineeringReviewTopicGroup')?.value || 'all');
  const status = String(document.querySelector('#openDataEngineeringReviewStatus')?.value || 'all');
  const fetchMethod = String(document.querySelector('#openDataEngineeringReviewFetchMethod')?.value || 'all');
  const sourceGate = String(document.querySelector('#openDataEngineeringReviewSourceGate')?.value || 'all');
  return items.filter(item => {
    const haystack = [
      String(item.title || ''),
      String(item.source_owner || ''),
      String(item.next_action || ''),
      String(item.engineering_notes || ''),
    ].join(' ').toLowerCase();
    const matchesQuery = !query || haystack.includes(query);
    const matchesGroup = topicGroup === 'all' || item.topic_group === topicGroup;
    const matchesStatus = status === 'all' || item.engineering_review_status === status;
    const matchesFetchMethod = fetchMethod === 'all' || item.proposed_fetch_method === fetchMethod;
    const matchesSourceGate = sourceGate === 'all' || item.source_review_gate === sourceGate;
    return matchesQuery && matchesGroup && matchesStatus && matchesFetchMethod && matchesSourceGate;
  });
}

function renderOpenDataEngineeringReviewTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-engineering-review-table"]');
  const summary = document.querySelector('[data-render="open-data-engineering-review-summary"]');
  if (!tbody) return;

  clearChildren(tbody);
  if (summary) summary.textContent = `目前顯示 ${items.length} / ${totalCount} 筆工程審查清單`;

  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 14;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的工程審查清單。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');

    const statusCell = document.createElement('td');
    const statusPill = document.createElement('span');
    statusPill.className = engineeringReviewStatusClass(item.engineering_review_status);
    statusPill.textContent = valueOrPending(item.engineering_review_status);
    statusCell.appendChild(statusPill);

    const topicCell = document.createElement('td');
    const topicPill = document.createElement('span');
    topicPill.className = 'pill';
    topicPill.textContent = topicGroupLabel(item.topic_group);
    topicCell.appendChild(topicPill);

    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const fetchCell = createCell(item.proposed_fetch_method);
    const sourceGateCell = createCell(item.source_review_gate);
    const licenseGateCell = createCell(item.license_review_gate);
    const formatGateCell = createCell(item.format_review_gate);
    const personalGateCell = createCell(item.personal_data_gate);
    const complaintGateCell = createCell(item.private_complaint_gate);
    const engineeringCell = createCell(item.engineering_review_allowed ? 'true' : 'false');
    const crawlerCell = createCell(item.crawler_execution_allowed ? 'true' : 'false');
    const actionCell = createCell(item.next_action, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      statusCell,
      topicCell,
      titleCell,
      ownerCell,
      fetchCell,
      sourceGateCell,
      licenseGateCell,
      formatGateCell,
      personalGateCell,
      complaintGateCell,
      engineeringCell,
      crawlerCell,
      actionCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataEngineeringReview(payload) {
  const items = Array.isArray(payload?.checklists) ? payload.checklists : [];
  setOpenDataEngineeringReviewKpi(payload);
  renderOpenDataEngineeringReviewNote(payload);

  const render = () => {
    const filtered = filterOpenDataEngineeringReview(items).sort((a, b) => {
      if (a.engineering_review_status !== b.engineering_review_status) {
        return String(a.engineering_review_status).localeCompare(String(b.engineering_review_status));
      }
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataEngineeringReviewTable(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataEngineeringReviewSearch');
  const groupSelect = document.querySelector('#openDataEngineeringReviewTopicGroup');
  const statusSelect = document.querySelector('#openDataEngineeringReviewStatus');
  const methodSelect = document.querySelector('#openDataEngineeringReviewFetchMethod');
  const sourceGateSelect = document.querySelector('#openDataEngineeringReviewSourceGate');
  if (searchInput) searchInput.addEventListener('input', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  if (methodSelect) methodSelect.addEventListener('change', render);
  if (sourceGateSelect) sourceGateSelect.addEventListener('change', render);
  render();
}

function sessionStatusClass(status) {
  if (status === 'blocked') return 'pill risk';
  if (status === 'needs_follow_up' || status === 'in_progress') return 'pill warn';
  return 'pill';
}

function setOpenDataReviewSessionKpi(payload) {
  const dayCounts = payload?.review_days || {};
  setText('[data-open-review-session="total"]', String(payload?.total_count ?? 0));
  setText('[data-open-review-session="day-1"]', String(dayCounts.day_1 ?? 0));
  setText('[data-open-review-session="day-2"]', String(dayCounts.day_2 ?? 0));
  setText('[data-open-review-session="day-3"]', String(dayCounts.day_3 ?? 0));
  setText('[data-open-review-session="minutes"]', String(payload?.total_estimated_minutes ?? 0));
  const crawlerDisabled = Array.isArray(payload?.session_tasks)
    ? payload.session_tasks.filter(item => item.crawler_execution_allowed === false).length
    : 0;
  setText('[data-open-review-session="crawler-disabled"]', String(crawlerDisabled));
  setText('[data-render="open-data-review-session-updated"]', formatUpdatedText(payload?.generated_at));
}

function renderOpenDataReviewSessionNote(payload) {
  const node = document.querySelector('[data-render="open-data-review-session-note"]');
  if (!node) return;
  node.textContent = '';
  const lines = [
    `public_use_status：${valueOrPending(payload?.public_use_status)}`,
    '這是人工審核執行工作台，不是 crawler。',
    'manual review required / no auto publish / no live crawler。',
    '不對 source_url 發出網路請求，不抓個資，不抓私人陳情全文。',
    `engineering_review_allowed_count：${valueOrPending(payload?.engineering_review_allowed_count)}`,
    `crawler_execution_allowed：${payload?.crawler_execution_allowed === false ? 'false' : valueOrPending(payload?.crawler_execution_allowed)}`,
  ];
  lines.forEach((text, index) => {
    if (index > 0) node.appendChild(document.createElement('br'));
    node.appendChild(document.createTextNode(text));
  });
}

function filterOpenDataReviewSessions(items) {
  const keyword = normalizedValue(document.querySelector('#openDataReviewSessionSearch')?.value);
  const reviewDay = document.querySelector('#openDataReviewSessionDay')?.value || 'all';
  const reviewBatch = document.querySelector('#openDataReviewSessionBatch')?.value || 'all';
  const status = document.querySelector('#openDataReviewSessionStatus')?.value || 'all';
  const topicGroup = document.querySelector('#openDataReviewSessionTopicGroup')?.value || 'all';

  return items.filter(item => {
    if (reviewDay !== 'all' && item.review_day !== reviewDay) return false;
    if (reviewBatch !== 'all' && item.review_batch !== reviewBatch) return false;
    if (status !== 'all' && item.session_status !== status) return false;
    if (topicGroup !== 'all' && item.topic_group !== topicGroup) return false;
    if (!keyword) return true;

    const haystack = [
      item.title,
      item.source_owner,
      item.next_action_after_session,
      item.reviewer_notes_template,
    ].map(normalizedValue).join(' ');
    return haystack.includes(keyword);
  });
}

function renderOpenDataReviewSessionTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-review-session-table"]');
  const summary = document.querySelector('[data-render="open-data-review-session-summary"]');
  if (!tbody) return;

  if (summary) {
    summary.textContent = `共 ${totalCount} 筆 session task，篩選後 ${items.length} 筆。`;
  }

  tbody.textContent = '';
  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 14;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的人工審核執行任務。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');
    const statusCell = document.createElement('td');
    const statusPill = document.createElement('span');
    statusPill.className = sessionStatusClass(item.session_status);
    statusPill.textContent = valueOrPending(item.session_status);
    statusCell.appendChild(statusPill);

    const dayCell = createCell(item.review_day);
    const batchCell = createCell(item.review_batch);
    const topicCell = createCell(item.topic_group);
    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const minutesCell = createCell(String(item.estimated_minutes ?? ''));
    const sourceCheckCell = createCell(item.source_open_check);
    const officialCheckCell = createCell(item.official_source_check);
    const licenseCell = createCell(item.license_terms_check);
    const personalCell = createCell(item.personal_data_check);
    const complaintCell = createCell(item.private_complaint_check);
    const actionCell = createCell(item.next_action_after_session, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      dayCell,
      batchCell,
      statusCell,
      topicCell,
      titleCell,
      ownerCell,
      minutesCell,
      sourceCheckCell,
      officialCheckCell,
      licenseCell,
      personalCell,
      complaintCell,
      actionCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataReviewSessions(payload) {
  const items = Array.isArray(payload?.session_tasks) ? payload.session_tasks : [];
  setOpenDataReviewSessionKpi(payload);
  renderOpenDataReviewSessionNote(payload);

  const render = () => {
    const filtered = filterOpenDataReviewSessions(items).sort((a, b) => {
      if (a.review_day !== b.review_day) {
        return String(a.review_day || '').localeCompare(String(b.review_day || ''));
      }
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataReviewSessionTable(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataReviewSessionSearch');
  const daySelect = document.querySelector('#openDataReviewSessionDay');
  const batchSelect = document.querySelector('#openDataReviewSessionBatch');
  const statusSelect = document.querySelector('#openDataReviewSessionStatus');
  const groupSelect = document.querySelector('#openDataReviewSessionTopicGroup');
  if (searchInput) searchInput.addEventListener('input', render);
  if (daySelect) daySelect.addEventListener('change', render);
  if (batchSelect) batchSelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
  render();
}

function evidenceStatusClass(status) {
  if (status === 'blocked') return 'pill risk';
  if (status === 'needs_follow_up' || status === 'collecting') return 'pill warn';
  return 'pill';
}

function setOpenDataReviewEvidenceKpi(payload) {
  const dayCounts = payload?.review_days || {};
  setText('[data-open-review-evidence="total"]', String(payload?.total_count ?? 0));
  setText('[data-open-review-evidence="not-started"]', String(payload?.evidence_status_counts?.not_started ?? 0));
  setText('[data-open-review-evidence="day-1"]', String(dayCounts.day_1 ?? 0));
  setText('[data-open-review-evidence="day-2"]', String(dayCounts.day_2 ?? 0));
  setText('[data-open-review-evidence="day-3"]', String(dayCounts.day_3 ?? 0));
  const crawlerDisabled = Array.isArray(payload?.evidence_packs)
    ? payload.evidence_packs.filter(item => item.crawler_execution_allowed === false).length
    : 0;
  setText('[data-open-review-evidence="crawler-disabled"]', String(crawlerDisabled));
  setText('[data-render="open-data-review-evidence-updated"]', formatUpdatedText(payload?.generated_at));
}

function renderOpenDataReviewEvidenceNote(payload) {
  const node = document.querySelector('[data-render="open-data-review-evidence-note"]');
  if (!node) return;
  node.textContent = '';
  const lines = [
    `public_use_status：${valueOrPending(payload?.public_use_status)}`,
    '這是人工審核證據包，不是 crawler。',
    'manual review required / no auto publish / no live crawler。',
    '不對 source_url 發出網路請求，不抓個資，不抓私人陳情全文。',
    `engineering_review_allowed_count：${valueOrPending(payload?.engineering_review_allowed_count)}`,
    `crawler_execution_allowed：${payload?.crawler_execution_allowed === false ? 'false' : valueOrPending(payload?.crawler_execution_allowed)}`,
  ];
  lines.forEach((text, index) => {
    if (index > 0) node.appendChild(document.createElement('br'));
    node.appendChild(document.createTextNode(text));
  });
}

function filterOpenDataReviewEvidence(items) {
  const keyword = normalizedValue(document.querySelector('#openDataReviewEvidenceSearch')?.value);
  const reviewDay = document.querySelector('#openDataReviewEvidenceDay')?.value || 'all';
  const reviewBatch = document.querySelector('#openDataReviewEvidenceBatch')?.value || 'all';
  const status = document.querySelector('#openDataReviewEvidenceStatus')?.value || 'all';
  const topicGroup = document.querySelector('#openDataReviewEvidenceTopicGroup')?.value || 'all';

  return items.filter(item => {
    if (reviewDay !== 'all' && item.review_day !== reviewDay) return false;
    if (reviewBatch !== 'all' && item.review_batch !== reviewBatch) return false;
    if (status !== 'all' && item.evidence_status !== status) return false;
    if (topicGroup !== 'all' && item.topic_group !== topicGroup) return false;
    if (!keyword) return true;

    const haystack = [
      item.title,
      item.source_owner,
      item.next_action,
      item.reviewer_summary_template,
    ].map(normalizedValue).join(' ');
    return haystack.includes(keyword);
  });
}

function renderOpenDataReviewEvidenceTable(items, totalCount) {
  const tbody = document.querySelector('[data-render="open-data-review-evidence-table"]');
  const summary = document.querySelector('[data-render="open-data-review-evidence-summary"]');
  if (!tbody) return;

  if (summary) {
    summary.textContent = `共 ${totalCount} 筆 evidence pack，篩選後 ${items.length} 筆。`;
  }

  tbody.textContent = '';
  if (!items.length) {
    const row = document.createElement('tr');
    const cell = document.createElement('td');
    cell.colSpan = 11;
    cell.className = 'empty';
    cell.textContent = '目前沒有符合條件的審核證據包。';
    row.appendChild(cell);
    tbody.appendChild(row);
    return;
  }

  items.forEach(item => {
    const row = document.createElement('tr');
    const statusCell = document.createElement('td');
    const statusPill = document.createElement('span');
    statusPill.className = evidenceStatusClass(item.evidence_status);
    statusPill.textContent = valueOrPending(item.evidence_status);
    statusCell.appendChild(statusPill);

    const dayCell = createCell(item.review_day);
    const batchCell = createCell(item.review_batch);
    const topicCell = createCell(item.topic_group);
    const titleCell = createCell(item.title);
    const ownerCell = createCell(item.source_owner);
    const requiredCell = createCell(String(Array.isArray(item.required_evidence_items) ? item.required_evidence_items.length : 0));
    const placeholderCell = createCell(String(Array.isArray(item.evidence_file_placeholders) ? item.evidence_file_placeholders.length : 0));
    const notesCell = createCell(item.reviewer_notes_required ? 'true' : 'false');
    const actionCell = createCell(item.next_action, 'compact');

    const urlCell = document.createElement('td');
    const link = document.createElement('a');
    link.className = 'url-link';
    link.href = valueOrPending(item.source_url);
    link.target = '_blank';
    link.rel = 'noopener';
    link.textContent = valueOrPending(item.source_url);
    urlCell.appendChild(link);

    row.append(
      statusCell,
      dayCell,
      batchCell,
      topicCell,
      titleCell,
      ownerCell,
      requiredCell,
      placeholderCell,
      notesCell,
      actionCell,
      urlCell,
    );
    tbody.appendChild(row);
  });
}

function setupOpenDataReviewEvidence(payload) {
  const items = Array.isArray(payload?.evidence_packs) ? payload.evidence_packs : [];
  setOpenDataReviewEvidenceKpi(payload);
  renderOpenDataReviewEvidenceNote(payload);

  const render = () => {
    const filtered = filterOpenDataReviewEvidence(items).sort((a, b) => {
      if (a.review_day !== b.review_day) {
        return String(a.review_day || '').localeCompare(String(b.review_day || ''));
      }
      return String(a.title || '').localeCompare(String(b.title || ''), 'zh-Hant');
    });
    renderOpenDataReviewEvidenceTable(filtered, items.length);
  };
  const searchInput = document.querySelector('#openDataReviewEvidenceSearch');
  const daySelect = document.querySelector('#openDataReviewEvidenceDay');
  const batchSelect = document.querySelector('#openDataReviewEvidenceBatch');
  const statusSelect = document.querySelector('#openDataReviewEvidenceStatus');
  const groupSelect = document.querySelector('#openDataReviewEvidenceTopicGroup');
  if (searchInput) searchInput.addEventListener('input', render);
  if (daySelect) daySelect.addEventListener('change', render);
  if (batchSelect) batchSelect.addEventListener('change', render);
  if (statusSelect) statusSelect.addEventListener('change', render);
  if (groupSelect) groupSelect.addEventListener('change', render);
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
  if (page === 'open-data-inventory') {
    const payload = await loadJson('./data/open_data_url_inventory.json', {
      generated_at: '',
      public_use_status: 'internal_url_inventory',
      total_count: 0,
      topic_groups: {},
      items: [],
    });
    setupOpenDataInventory(payload);
  }
  if (page === 'open-data-review') {
    const payload = await loadJson('./data/open_data_url_review_queue.json', {
      generated_at: '',
      public_use_status: 'internal_url_review_queue',
      total_count: 0,
      topic_groups: {},
      items: [],
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataReviewQueue(payload);
  }
  if (page === 'open-data-readiness') {
    const payload = await loadJson('./data/open_data_readiness_report.json', {
      generated_at: '',
      public_use_status: 'internal_readiness_report',
      total_count: 0,
      topic_groups: {},
      readiness_levels: {},
      items: [],
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataReadiness(payload);
  }
  if (page === 'open-data-top10-tasks') {
    const payload = await loadJson('./data/open_data_top10_review_tasks.json', {
      generated_at: '',
      public_use_status: 'internal_top10_review_tasks',
      total_count: 0,
      topic_groups: {},
      readiness_levels: {},
      review_priority_counts: {},
      tasks: [],
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataTop10Tasks(payload);
  }
  if (page === 'open-data-crawler-specs') {
    const payload = await loadJson('./data/open_data_crawler_spec_drafts.json', {
      generated_at: '',
      public_use_status: 'internal_crawler_spec_drafts',
      total_count: 0,
      topic_groups: {},
      proposed_fetch_methods: {},
      parser_types: {},
      specs: [],
      crawler_execution_allowed: false,
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataCrawlerSpecs(payload);
  }
  if (page === 'open-data-human-review') {
    const payload = await loadJson('./data/open_data_human_review_workbook.json', {
      generated_at: '',
      public_use_status: 'internal_human_review_workbook',
      total_count: 0,
      topic_groups: {},
      review_status_counts: {},
      approval_gate_status_counts: {},
      engineering_review_allowed_count: 0,
      records: [],
      crawler_execution_allowed: false,
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataHumanReview(payload);
  }
  if (page === 'open-data-engineering-review') {
    const payload = await loadJson('./data/open_data_engineering_review_checklist.json', {
      generated_at: '',
      public_use_status: 'internal_engineering_review_checklist',
      total_count: 0,
      topic_groups: {},
      engineering_review_status_counts: {},
      engineering_review_allowed_count: 0,
      checklists: [],
      crawler_execution_allowed: false,
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataEngineeringReview(payload);
  }
  if (page === 'open-data-review-sessions') {
    const payload = await loadJson('./data/open_data_review_session_planner.json', {
      generated_at: '',
      public_use_status: 'internal_review_session_planner',
      total_count: 0,
      review_days: {},
      review_batches: {},
      topic_groups: {},
      session_status_counts: {},
      total_estimated_minutes: 0,
      engineering_review_allowed_count: 0,
      session_tasks: [],
      crawler_execution_allowed: false,
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataReviewSessions(payload);
  }
  if (page === 'open-data-review-evidence') {
    const payload = await loadJson('./data/open_data_review_evidence_pack.json', {
      generated_at: '',
      public_use_status: 'internal_review_evidence_pack',
      total_count: 0,
      review_days: {},
      review_batches: {},
      topic_groups: {},
      evidence_status_counts: {},
      engineering_review_allowed_count: 0,
      evidence_packs: [],
      crawler_execution_allowed: false,
      no_live_crawler: true,
      manual_review_required: true,
      no_auto_publish: true,
      no_personal_data: true,
    });
    setupOpenDataReviewEvidence(payload);
  }
  if (page === 'reports') {
    const reports = await loadJson('./data/reports_index.json', []);
    renderReports(reports);
  }
}

bootSitePages();
