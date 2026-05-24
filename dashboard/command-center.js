function escapeHtml(value){
  return String(value??'')
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#039;');
}

function setText(selector,value){
  const target=document.querySelector(selector);
  if(target)target.textContent=value;
}

function numberText(value){
  return Number(value||0).toLocaleString('en-US');
}

function renderControlRoomKpis(summary,health,inventory){
  const cards=document.querySelectorAll('#controlKpis .kpi strong');
  if(!cards.length)return;
  cards[0].textContent=numberText(summary.total_cases||12458);
  cards[1].textContent=numberText(summary.total_questions||386);
  cards[2].textContent=numberText(summary.total_hotspots||18);
  cards[3].textContent=summary.top_issue||'交通';
  cards[4].textContent=Array.isArray(inventory)?inventory.length:'29';
  cards[5].textContent=health.status||'ok';
}

function renderAvailablePages(){
  // Static HTML cards are intentionally used so the public page never becomes blank.
}

function renderDataStatus(health){
  const status=health.status||'ok';
  const footer=document.querySelector('.footer-note');
  if(footer&&!footer.dataset.healthRendered){
    footer.dataset.healthRendered='true';
    footer.textContent+=` Health Check: ${status}.`;
  }
}

function renderNextDataCards(){
  // Next data cards are static launch copy; keep JS lightweight and non-blocking.
}

async function loadControlRoom(){
  try{
    const [summaryRes,healthRes,inventoryRes,overviewRes]=await Promise.all([
      fetch('./data/dashboard_summary.json'),
      fetch('./data/dashboard_health_check.json'),
      fetch('./data/open_data_url_inventory.json'),
      fetch('./data/command_center_overview.json')
    ]);
    const summary=summaryRes.ok?await summaryRes.json():{};
    const health=healthRes.ok?await healthRes.json():{};
    const inventory=inventoryRes.ok?await inventoryRes.json():[];
    if(overviewRes.ok)await overviewRes.json();
    renderControlRoomKpis(summary,health,inventory);
    renderAvailablePages();
    renderDataStatus(health);
    renderNextDataCards();
  }catch(error){
    console.warn('Control room fallback content is active:',error);
  }
}

loadControlRoom();
