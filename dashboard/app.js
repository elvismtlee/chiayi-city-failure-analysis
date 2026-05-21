async function loadJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(path);
    return await response.json();
  } catch (error) {
    console.warn('Use fallback data:', path, error);
    return fallback;
  }
}

function formatNumber(value) {
  return typeof value === 'number' ? value.toLocaleString('zh-TW') : value;
}

function setText(selector, value) {
  const node = document.querySelector(selector);
  if (node) node.textContent = value;
}

async function bootDashboard() {
  const summary = await loadJson('./data/dashboard_summary.json', {
    total_cases: 12458,
    total_questions: 386,
    total_hotspots: 18,
    top_issue: '交通',
    updated_at: 'prototype'
  });

  const issues = await loadJson('./data/issue_ranking.json', []);
  const hotspots = await loadJson('./data/hotspots.json', []);

  setText('[data-kpi="total_cases"]', formatNumber(summary.total_cases));
  setText('[data-kpi="top_issue"]', summary.top_issue || '—');
  setText('[data-kpi="total_hotspots"]', formatNumber(summary.total_hotspots));
  setText('[data-kpi="total_questions"]', formatNumber(summary.total_questions));
  setText('[data-kpi="updated_at"]', `資料更新：${summary.updated_at || 'prototype'}`);

  const issueBox = document.querySelector('[data-render="issue_ranking"]');
  if (issueBox && issues.length) {
    issueBox.innerHTML = issues.map(item => `
      <div class="chart-row">
        <span>${item.issue}</span>
        <div class="bar-bg"><div class="bar" style="width:${Math.min(item.score, 100)}%"></div></div>
        <b>${item.score}</b>
      </div>
    `).join('');
  }

  const mapBox = document.querySelector('[data-render="hotspot_map"]');
  if (mapBox && hotspots.length) {
    mapBox.innerHTML = '<div class="map-grid"></div>' + hotspots.map((h, index) => {
      const color = index % 3 === 1 ? 'orange' : index % 3 === 2 ? 'blue' : '';
      return `
        <div class="hotspot ${color}" style="left:${h.x}%; top:${h.y}%;"></div>
        <div class="place" style="left:${Math.max(h.x - 4, 2)}%; top:${Math.max(h.y - 11, 2)}%;">${h.name}</div>
      `;
    }).join('');
  }

  const tableBody = document.querySelector('[data-render="hotspot_table"]');
  if (tableBody && hotspots.length) {
    tableBody.innerHTML = hotspots.map(h => `
      <tr>
        <td>${h.name}</td>
        <td><span class="pill">${h.category}</span></td>
        <td>${h.department}</td>
        <td>${h.score}</td>
        <td>${h.action}</td>
      </tr>
    `).join('');
  }
}

bootDashboard();
