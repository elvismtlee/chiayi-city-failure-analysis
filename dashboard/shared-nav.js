const DASHBOARD_NAV_ITEMS = [
  { title: '城市儀表板首頁', path: './index.html', file: 'index.html' },
  { title: '城市熱點地圖', path: './map.html', file: 'map.html' },
  { title: '座標審核', path: './geocoding-review.html', file: 'geocoding-review.html' },
  { title: '影音轉錄審核', path: './video-review.html', file: 'video-review.html' },
  { title: '會議紀錄審核', path: './minutes-review.html', file: 'minutes-review.html' },
  { title: '會議紀錄議題', path: './minutes-issues.html', file: 'minutes-issues.html' },
  { title: '每週摘要', path: './weekly-summary.html', file: 'weekly-summary.html' },
  { title: '政策草稿', path: './policy-drafts.html', file: 'policy-drafts.html' },
  { title: '城市洞察分析', path: './insights.html', file: 'insights.html' },
  { title: '資料來源', path: './sources.html', file: 'sources.html' },
  { title: '方法論', path: './methodology.html', file: 'methodology.html' },
  { title: '城市週報', path: './reports.html', file: 'reports.html' },
];

const DASHBOARD_DISCLOSURE = '本平台資料來自公開資訊、官方資料與原型資料整理。分析結果為城市治理與地方議題研究用途，不代表完整民意調查，也不作為個人評價結論。';

function getCurrentFileName() {
  const pathname = window.location.pathname || '';
  const fileName = pathname.split('/').filter(Boolean).pop();
  return fileName || 'index.html';
}

function renderSharedNav() {
  const nav = document.querySelector('.nav');
  if (!nav) return;
  const currentFile = getCurrentFileName();
  nav.innerHTML = DASHBOARD_NAV_ITEMS.map(item => {
    const active = item.file === currentFile ? ' class="active"' : '';
    return `<a${active} href="${item.path}">${item.title}</a>`;
  }).join('') + '<a href="https://www.chiayi2026.com/" target="_blank" rel="noopener">競選官網</a>';
}

function renderSharedFooter() {
  if (document.querySelector('.site-footer')) return;
  const main = document.querySelector('main');
  if (!main) return;
  const footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML = `<p>${DASHBOARD_DISCLOSURE}</p>`;
  main.insertAdjacentElement('afterend', footer);
}

function injectFooterStyle() {
  if (document.getElementById('shared-nav-style')) return;
  const style = document.createElement('style');
  style.id = 'shared-nav-style';
  style.textContent = `
    .site-footer{max-width:1180px;margin:0 auto 42px;padding:0 24px;color:#64748b;font-size:14px;line-height:1.7}
    .site-footer p{border-top:1px solid rgba(15,118,110,.18);padding-top:18px;margin:0}
  `;
  document.head.appendChild(style);
}

renderSharedNav();
injectFooterStyle();
renderSharedFooter();
