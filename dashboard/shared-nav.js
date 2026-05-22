const DASHBOARD_NAV_GROUPS = [
  {
    label: '總覽',
    tone: 'overview',
    items: [
      { title: '儀表板首頁', path: './index.html', file: 'index.html' },
      { title: '總控台', path: './command-center.html', file: 'command-center.html' },
      { title: '健康檢查', path: './health-check.html', file: 'health-check.html' },
      { title: '每週系統報告', path: './weekly-system-report.html', file: 'weekly-system-report.html' },
    ],
  },
  {
    label: '資料審核',
    tone: 'review',
    items: [
      { title: '城市熱點地圖', path: './map.html', file: 'map.html' },
      { title: '座標審核', path: './geocoding-review.html', file: 'geocoding-review.html' },
      { title: '影音審核', path: './video-review.html', file: 'video-review.html' },
      { title: '會議紀錄審核', path: './minutes-review.html', file: 'minutes-review.html' },
      { title: '會議紀錄議題', path: './minutes-issues.html', file: 'minutes-issues.html' },
    ],
  },
  {
    label: '內容產出',
    tone: 'content',
    items: [
      { title: '每週摘要', path: './weekly-summary.html', file: 'weekly-summary.html' },
      { title: '政策草稿', path: './policy-drafts.html', file: 'policy-drafts.html' },
      { title: '社群草稿', path: './social-drafts.html', file: 'social-drafts.html' },
      { title: '短影音腳本', path: './video-scripts.html', file: 'video-scripts.html' },
      { title: '拍攝清單', path: './filming-checklists.html', file: 'filming-checklists.html' },
      { title: '內容排程', path: './content-schedule.html', file: 'content-schedule.html' },
    ],
  },
  {
    label: '發布管理',
    tone: 'publish',
    items: [
      { title: '公開審核', path: './public-review.html', file: 'public-review.html' },
      { title: '已核准素材', path: './approved-materials.html', file: 'approved-materials.html' },
      { title: '每日執行', path: './daily-execution.html', file: 'daily-execution.html' },
    ],
  },
  {
    label: '系統說明',
    tone: 'system',
    items: [
      { title: '城市洞察', path: './insights.html', file: 'insights.html' },
      { title: '資料來源', path: './sources.html', file: 'sources.html' },
      { title: '方法論', path: './methodology.html', file: 'methodology.html' },
      { title: '城市週報', path: './reports.html', file: 'reports.html' },
      { title: '競選官網', path: 'https://www.chiayi2026.com/', file: 'external', external: true },
    ],
  },
];

const DASHBOARD_NAV_ITEMS = DASHBOARD_NAV_GROUPS.flatMap(group => group.items);
const DASHBOARD_DISCLOSURE = '本平台資料來自公開資訊、官方資料與原型資料整理。分析結果為城市治理與地方議題研究用途，不代表完整民意調查，也不作為個人評價結論。';

function getCurrentFileName() {
  const pathname = window.location.pathname || '';
  const fileName = pathname.split('/').filter(Boolean).pop();
  return fileName || 'index.html';
}

function findCurrentGroup(currentFile) {
  return DASHBOARD_NAV_GROUPS.find(group => group.items.some(item => item.file === currentFile));
}

function renderSharedNav() {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const currentFile = getCurrentFileName();
  nav.classList.add('grouped-nav');
  nav.textContent = '';
  DASHBOARD_NAV_GROUPS.forEach(group => {
    const groupNode = document.createElement('div');
    groupNode.className = `nav-group nav-group-${group.tone}`;
    const isGroupActive = group.items.some(item => item.file === currentFile);
    if (isGroupActive) groupNode.classList.add('active-group');

    const label = document.createElement('div');
    label.className = 'nav-group-label';
    label.textContent = group.label;
    groupNode.appendChild(label);

    const links = document.createElement('div');
    links.className = 'nav-group-links';
    group.items.forEach(item => {
      const link = document.createElement('a');
      link.href = item.path;
      link.textContent = item.title;
      if (item.file === currentFile) link.className = 'active';
      if (item.external) {
        link.target = '_blank';
        link.rel = 'noopener';
      }
      links.appendChild(link);
    });
    groupNode.appendChild(links);
    nav.appendChild(groupNode);
  });
}

function renderBreadcrumb() {
  const breadcrumb = document.querySelector('[data-render="breadcrumb"]');
  if (!breadcrumb) return;
  const currentFile = getCurrentFileName();
  const group = findCurrentGroup(currentFile);
  const current = DASHBOARD_NAV_ITEMS.find(item => item.file === currentFile);
  breadcrumb.textContent = group && current ? `${group.label} / ${current.title}` : '嘉義城市故障分析中心';
}

function renderSharedFooter() {
  if (document.querySelector('.site-footer')) return;
  const main = document.querySelector('main');
  if (!main) return;
  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  const paragraph = document.createElement('p');
  paragraph.textContent = DASHBOARD_DISCLOSURE;
  footer.appendChild(paragraph);
  main.insertAdjacentElement('afterend', footer);
}

function injectFooterStyle() {
  if (document.getElementById('shared-nav-style')) return;
  const style = document.createElement('style');
  style.id = 'shared-nav-style';
  style.textContent = `
    .site-footer{max-width:1180px;margin:0 auto 42px;padding:0 24px;color:#64748b;font-size:14px;line-height:1.7}.site-footer p{border-top:1px solid rgba(15,118,110,.18);padding-top:18px;margin:0}
    .grouped-nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-bottom:28px}.nav-group{border:1px solid rgba(255,255,255,.22);border-radius:20px;padding:10px;background:rgba(255,255,255,.10);backdrop-filter:blur(8px)}.nav-group.active-group{background:rgba(255,255,255,.18);box-shadow:0 14px 36px rgba(0,0,0,.16)}.nav-group-label{font-size:12px;letter-spacing:.12em;color:rgba(255,255,255,.72);margin:0 0 8px;font-weight:800}.nav-group-links{display:flex;flex-wrap:wrap;gap:7px}.nav-group a{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 10px;font-size:14px;line-height:1;background:rgba(255,255,255,.08)}.nav-group a.active{background:#fff;color:#064e3b;font-weight:900;border-color:#fff}.nav-group-review a.active{color:#075985}.nav-group-content a.active{color:#581c87}.nav-group-publish a.active{color:#9a3412}.nav-group-system a.active{color:#334155}@media(max-width:760px){.grouped-nav{grid-template-columns:1fr}.nav-group-links{gap:8px}.nav-group a{font-size:13px}}
  `;
  document.head.appendChild(style);
}

renderSharedNav();
renderBreadcrumb();
injectFooterStyle();
renderSharedFooter();
