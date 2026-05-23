const LABELS={
  minutes_review:'會議紀錄審核',
  reviewed_minutes_sample:'已審會議範例',
  issue_candidates:'議題候選',
  weekly_summary:'每週摘要',
  policy_drafts:'政策草稿',
  social_drafts:'社群草稿',
  video_scripts:'短影音腳本',
  filming_checklists:'拍攝清單',
  content_schedule:'內容排程',
  daily_execution_list:'每日執行',
  public_review_queue:'公開審核',
  approved_materials:'已核准素材'
};

const NOTES={
  minutes_review:'等待人工確認的會議紀錄。',
  reviewed_minutes_sample:'可作為抽取規則校正樣本。',
  issue_candidates:'可轉成地方議題與政策素材。',
  weekly_summary:'週報草稿，發布前需人工確認。',
  policy_drafts:'政策語言與證據仍需人工審核。',
  social_drafts:'社群文案草稿，不自動發布。',
  video_scripts:'短影音拍攝前仍需確認地點與敘事。',
  filming_checklists:'一人團隊可執行的拍攝準備。',
  content_schedule:'內容節奏規劃，需人工排定。',
  daily_execution_list:'每日可執行工作清單。',
  public_review_queue:'公開前最後審核佇列。',
  approved_materials:'已通過審核才可對外使用。'
};

function escapeHtml(value){
  return String(value??'')
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;')
    .replaceAll('"','&quot;')
    .replaceAll("'",'&#039;');
}

function humanLabel(key){
  return LABELS[key]||String(key).replaceAll('_',' ');
}

function renderKeyCounts(data){
  const keyCounts=document.querySelector('#key-counts');
  const entries=Object.entries(data.key_counts||{});
  keyCounts.innerHTML=entries.map(([name,value])=>`
    <article class="metric">
      <span>${escapeHtml(humanLabel(name))}</span>
      <strong>${escapeHtml(value)}</strong>
      <em>${escapeHtml(NOTES[name]||'已納入 command center 總覽。')}</em>
    </article>
  `).join('')||'<div class="empty-state">目前沒有可顯示的 KPI。</div>';
}

function renderPipeline(data){
  const pipeline=document.querySelector('#pipeline-status');
  pipeline.innerHTML=(data.pipeline_status||[]).map((item)=>`
    <tr>
      <td data-label="項目">
        ${escapeHtml(item.name)}
        <span class="source-path">${escapeHtml(item.source_file)}</span>
      </td>
      <td data-label="狀態"><span class="status-pill">${escapeHtml(item.status)}</span></td>
      <td data-label="數量"><span class="count-pill">${escapeHtml(item.record_count)}</span></td>
      <td data-label="下一步">${escapeHtml(item.next_step)}</td>
    </tr>
  `).join('')||'<tr><td colspan="4">目前沒有 pipeline status。</td></tr>';
}

function renderBacklog(data){
  const backlog=document.querySelector('#review-backlog');
  backlog.innerHTML=Object.entries(data.review_backlog||{}).map(([name,value])=>`
    <article class="backlog-card">
      <div>
        <b>${escapeHtml(humanLabel(name))}</b>
        <span>${escapeHtml(NOTES[name]||'需要人工確認。')}</span>
      </div>
      <strong>${escapeHtml(value)}</strong>
    </article>
  `).join('')||'<div class="empty-state">目前沒有待審 backlog。</div>';
}

function renderList(selector,items,emptyText){
  const target=document.querySelector(selector);
  target.innerHTML=(items||[]).map((item)=>`<li>${escapeHtml(item)}</li>`).join('')||`<li>${escapeHtml(emptyText)}</li>`;
}

function renderMeta(data){
  const status=document.querySelector('#public-use-status');
  const generatedAt=document.querySelector('#generated-at');
  if(status)status.textContent=data.public_use_status||'internal_command_center';
  if(generatedAt)generatedAt.textContent=data.generated_at||'not recorded';
}

async function loadCommandCenter(){
  const response=await fetch('./data/command_center_overview.json');
  if(!response.ok)throw new Error(`HTTP ${response.status}`);
  const data=await response.json();
  renderMeta(data);
  renderKeyCounts(data);
  renderPipeline(data);
  renderBacklog(data);
  renderList('#next-actions',data.next_actions,'目前沒有下一步 action。');
  renderList('#warnings',data.warnings,'目前沒有 warning。');
}

loadCommandCenter().catch((error)=>{
  document.querySelector('#warnings').innerHTML=`<li>讀取 command_center_overview.json 失敗：${escapeHtml(error.message)}</li>`;
  document.querySelector('#key-counts').innerHTML='<div class="empty-state">KPI 尚未載入，請確認本地 JSON 路徑。</div>';
});
