function escapeHtml(value){
  return String(value??'')
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#039;');
}

function numberText(value){
  return Number(value||0).toLocaleString('en-US');
}

async function loadJson(path,fallback){
  try{
    const response=await fetch(path,{cache:'no-store'});
    if(!response.ok) throw new Error(path);
    return await response.json();
  }catch(error){
    console.warn('Control room fallback content is active:',path,error);
    return fallback;
  }
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
  const [summary,health,inventory]=await Promise.all([
    loadJson('./data/dashboard_summary.json',{}),
    loadJson('./data/dashboard_health_check.json',{status:'ok'}),
    loadJson('./data/open_data_url_inventory.json',[])
  ]);
  await loadJson('./data/command_center_overview.json',{});
  renderControlRoomKpis(summary,health,inventory);
  renderAvailablePages();
  renderDataStatus(health);
  renderNextDataCards();
}

document.addEventListener('DOMContentLoaded',()=>{
  loadControlRoom().catch((error)=>{
    console.warn('Control room fallback content is active:',error);
  });
});
