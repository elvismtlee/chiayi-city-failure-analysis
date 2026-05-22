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
      { title: '議會公開 metadata', path: './cycc-metadata.html', file: 'cycc-metadata.html' },
      { title: '影音轉錄審核', path: './video-review.html', file: 'video-review.html' },
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

function makeNavLink(item, currentFile, extraClass = '') {
  const link = document.createElement('a');
  link.href = item.path;
  link.textContent = item.title;
  link.className = extraClass;
  if (item.file === currentFile) link.classList.add('active');
  if (item.external) {
    link.target = '_blank';
    link.rel = 'noopener';
  }
  return link;
}

function renderSharedNav() {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const currentFile = getCurrentFileName();
  const currentGroup = findCurrentGroup(currentFile) || DASHBOARD_NAV_GROUPS[0];
  nav.className = 'nav dashboard-nav';
  nav.textContent = '';

  const mainRow = document.createElement('div');
  mainRow.className = 'dashboard-nav-main';
  DASHBOARD_NAV_GROUPS.forEach(group => {
    const primaryItem = group.items[0];
    const groupLink = document.createElement('a');
    groupLink.href = primaryItem.path;
    groupLink.textContent = group.label;
    groupLink.className = `dashboard-nav-tab dashboard-nav-tab-${group.tone}`;
    if (group.label === currentGroup.label) groupLink.classList.add('active');
    mainRow.appendChild(groupLink);
  });

  const subRow = document.createElement('div');
  subRow.className = `dashboard-nav-sub dashboard-nav-sub-${currentGroup.tone}`;
  const subLabel = document.createElement('span');
  subLabel.className = 'dashboard-nav-sub-label';
  subLabel.textContent = currentGroup.label;
  subRow.appendChild(subLabel);
  currentGroup.items.forEach(item => {
    subRow.appendChild(makeNavLink(item, currentFile, 'dashboard-nav-link'));
  });

  nav.appendChild(mainRow);
  nav.appendChild(subRow);
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
    .hero .dashboard-nav,.dashboard-nav{display:grid!important;grid-template-columns:1fr!important;gap:16px!important;margin:0 0 34px!important;padding:0!important;max-width:1180px!important;width:100%!important}.dashboard-nav a{text-decoration:none!important}.dashboard-nav-main{display:grid!important;grid-template-columns:repeat(5,minmax(0,1fr))!important;gap:14px!important}.dashboard-nav-tab{display:flex!important;justify-content:center!important;align-items:center!important;min-height:58px!important;border-radius:20px!important;border:1px solid rgba(255,255,255,.42)!important;background:rgba(255,255,255,.14)!important;color:#fff!important;font-weight:950!important;font-size:19px!important;letter-spacing:.06em!important;box-shadow:0 12px 28px rgba(0,0,0,.10)!important;line-height:1.1!important}.dashboard-nav-tab.active{background:#fff!important;color:#064e3b!important;border-color:#fff!important;box-shadow:0 18px 42px rgba(0,0,0,.24)!important}.dashboard-nav-sub{display:flex!important;align-items:center!important;gap:12px!important;flex-wrap:wrap!important;border:1px solid rgba(255,255,255,.30)!important;background:rgba(0,0,0,.12)!important;border-radius:24px!important;padding:14px!important;backdrop-filter:blur(8px)!important}.dashboard-nav-sub-label{display:inline-flex!important;align-items:center!important;border-radius:16px!important;background:rgba(255,255,255,.22)!important;color:#fff!important;font-size:15px!important;font-weight:950!important;letter-spacing:.12em!important;padding:11px 14px!important;white-space:nowrap!important}.dashboard-nav-link{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:42px!important;border-radius:999px!important;border:1px solid rgba(255,255,255,.34)!important;background:rgba(255,255,255,.12)!important;color:#fff!important;padding:11px 16px!important;font-size:16px!important;line-height:1!important;font-weight:900!important;white-space:nowrap!important;box-shadow:none!important}.dashboard-nav-link.active{background:#fff!important;border-color:#fff!important;color:#064e3b!important;box-shadow:0 12px 28px rgba(0,0,0,.18)!important}.dashboard-nav-sub-review .dashboard-nav-link.active{color:#075985!important}.dashboard-nav-sub-content .dashboard-nav-link.active{color:#581c87!important}.dashboard-nav-sub-publish .dashboard-nav-link.active{color:#9a3412!important}.dashboard-nav-sub-system .dashboard-nav-link.active{color:#334155!important}@media(max-width:1040px){.dashboard-nav-main{grid-template-columns:repeat(3,minmax(0,1fr))!important}.dashboard-nav-tab{font-size:18px!important;min-height:54px!important}.dashboard-nav-link{font-size:15px!important}}@media(max-width:640px){.hero .dashboard-nav,.dashboard-nav{gap:12px!important;margin-bottom:26px!important}.dashboard-nav-main{grid-template-columns:1fr!important}.dashboard-nav-tab{font-size:18px!important;min-height:50px!important}.dashboard-nav-sub{align-items:flex-start!important;gap:10px!important;padding:12px!important}.dashboard-nav-sub-label{width:100%!important;justify-content:center!important;font-size:14px!important}.dashboard-nav-link{font-size:15px!important;padding:10px 13px!important;min-height:40px!important}}
  `;
  document.head.appendChild(style);
}

injectFooterStyle();
renderSharedNav();
renderBreadcrumb();
renderSharedFooter();
