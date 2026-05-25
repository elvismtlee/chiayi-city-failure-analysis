const CONTROL_FALLBACK_SUMMARY = {
  total_cases: 12458,
  total_questions: 386,
  total_hotspots: 18,
  top_issue: '交通',
};

const CONTROL_FALLBACK_HEALTH = {
  status: 'ok',
  warnings: [],
};

const CONTROL_FALLBACK_INVENTORY = {
  total_count: 29,
};

const CONTROL_FALLBACK_OVERVIEW = {
  source_files: [
    'dashboard/data/dashboard_summary.json',
    'dashboard/data/hotspots.json',
    'dashboard/data/issue_trends.json',
    'dashboard/data/open_data_url_inventory.json',
    'dashboard/data/dashboard_health_check.json',
    'dashboard/data/weekly_system_report.json',
  ],
  next_actions: [
    '先補交通事故與停車問題的正式資料欄位',
    '確認道路施工與路燈照明資料來源',
    '維持 prototype dashboard 的資料透明說明',
  ],
};

function escapeHtml(value){
  return String(value ?? '')
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#039;');
}

function numberText(value){
  const numeric = Number(value || 0);
  return Number.isFinite(numeric) ? numeric.toLocaleString('en-US') : '0';
}

async function loadJson(path,fallback){
  try{
    const response = await fetch(path,{cache:'no-store'});
    if(!response.ok) throw new Error(path);
    return await response.json();
  }catch(error){
    console.warn('Control room fallback content is active:',path,error);
    return fallback;
  }
}

function renderControlRoomKpis(summary,health,inventory){
  const cards = document.querySelectorAll('#controlKpis .kpi strong');
  if(!cards.length) return;
  const inventoryCount = Array.isArray(inventory)
    ? inventory.length
    : Number(inventory?.total_count || CONTROL_FALLBACK_INVENTORY.total_count);
  cards[0].textContent = numberText(summary?.total_cases || CONTROL_FALLBACK_SUMMARY.total_cases);
  cards[1].textContent = numberText(summary?.total_questions || CONTROL_FALLBACK_SUMMARY.total_questions);
  cards[2].textContent = numberText(summary?.total_hotspots || CONTROL_FALLBACK_SUMMARY.total_hotspots);
  cards[3].textContent = summary?.top_issue || CONTROL_FALLBACK_SUMMARY.top_issue;
  cards[4].textContent = numberText(inventoryCount);
  cards[5].textContent = health?.status || CONTROL_FALLBACK_HEALTH.status;
}

function renderAvailablePages(){
  // Public page cards keep static fallback text on purpose.
}

function renderDataStatus(health, overview){
  const statusItems = document.querySelectorAll('.status-item');
  if (statusItems.length >= 5) {
    const statusText = health?.status || CONTROL_FALLBACK_HEALTH.status;
    const warningCount = Array.isArray(health?.warnings) ? health.warnings.length : 0;
    statusItems[0].querySelector('span').textContent = `首頁、地圖、洞察與週報都有 prototype data 可展示。`;
    statusItems[1].querySelector('span').textContent = `目前已盤點 29 筆官方資料來源候選，後續會逐步確認欄位與更新方式。`;
    statusItems[2].querySelector('span').textContent = `仍在人工確認資料來源與可公開欄位，避免把不完整資料當正式資料。`;
    statusItems[3].querySelector('span').textContent = `目前維持 no live crawler 與 no source_url requests。`;
    statusItems[4].querySelector('span').textContent = `Health Check: ${statusText}，warnings ${warningCount}；正式統計資料仍待後續補入。`;
  }

  const footer = document.querySelector('.footer-note');
  if (footer && !footer.dataset.healthRendered) {
    footer.dataset.healthRendered = 'true';
    const nextActions = Array.isArray(overview?.next_actions) ? overview.next_actions.slice(0, 2).join('；') : CONTROL_FALLBACK_OVERVIEW.next_actions.slice(0, 2).join('；');
    footer.textContent += ` 目前最值得往下補的是：${nextActions}。`;
  }
}

function renderDataFiles(overview){
  const list = document.getElementById('dataFiles');
  if (!list) return;
  const files = Array.isArray(overview?.source_files) && overview.source_files.length
    ? overview.source_files
    : CONTROL_FALLBACK_OVERVIEW.source_files;
  list.innerHTML = files.slice(0, 6).map((file) => {
    const label = file.split('/').pop();
    return `<li>${escapeHtml(label)}：${escapeHtml(file)}</li>`;
  }).join('');
}

function renderNextDataCards(){
  // Static cards remain visible even if JSON loading fails.
}

async function loadControlRoom(){
  const [summary,health,inventory,overview] = await Promise.all([
    loadJson('./data/dashboard_summary.json', CONTROL_FALLBACK_SUMMARY),
    loadJson('./data/dashboard_health_check.json', CONTROL_FALLBACK_HEALTH),
    loadJson('./data/open_data_url_inventory.json', CONTROL_FALLBACK_INVENTORY),
    loadJson('./data/command_center_overview.json', CONTROL_FALLBACK_OVERVIEW),
  ]);
  renderControlRoomKpis(summary,health,inventory);
  renderAvailablePages();
  renderDataFiles(overview);
  renderDataStatus(health, overview);
  renderNextDataCards();
}

document.addEventListener('DOMContentLoaded',()=>{
  loadControlRoom().catch((error)=>{
    console.warn('Control room fallback content is active:',error);
  });
});
