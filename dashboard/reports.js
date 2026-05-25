const REPORT_FALLBACK = {
  week_start: '2026-05-18',
  week_end: '2026-05-24',
  system_status: 'ok',
  recommended_next_actions: [
    '優先確認交通事故與停車問題的正式資料欄位。',
    '整理市場周邊與學校周邊的熱點追蹤格式。',
    '維持 prototype dashboard 的資料透明說明。',
  ],
};

const REPORT_FALLBACK_SUMMARY = {
  summary_title: '本週嘉義城市故障觀察',
  summary: '目前平台先用公開可讀的 prototype data 呈現城市問題全貌，重點在交通停車、市場商圈與通學安全三個方向。',
  top_findings: [
    '交通停車仍是目前最值得優先追蹤的城市問題類型。',
    '市場周邊同時牽涉環境、動線與卸貨規劃，適合整合改善。',
    '學校周邊適合先從通學步道與接送區改善開始。',
  ],
};

async function loadReportJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(path);
    return await response.json();
  } catch (error) {
    console.warn('Weekly report fallback content is active:', path, error);
    return fallback;
  }
}

function reportText(value, fallback = '') {
  if (value === undefined || value === null || value === '') return fallback;
  return String(value);
}

function renderReportHeader(report) {
  const range = document.getElementById('report-week-range');
  const status = document.getElementById('report-status-pill');
  if (range) {
    range.textContent = `週期：${reportText(report?.week_start, REPORT_FALLBACK.week_start)} 至 ${reportText(report?.week_end, REPORT_FALLBACK.week_end)}`;
  }
  if (status) {
    status.textContent = `系統狀態：${reportText(report?.system_status, REPORT_FALLBACK.system_status)}`;
  }
}

function renderReportHighlights(summary) {
  const target = document.getElementById('weekly-report-highlights');
  if (!target) return;
  const findings = Array.isArray(summary?.top_findings) && summary.top_findings.length
    ? summary.top_findings.slice(0, 3)
    : REPORT_FALLBACK_SUMMARY.top_findings;
  const tones = ['accent-orange', 'accent-green', 'accent-blue'];
  target.innerHTML = findings.map((item, index) => `
    <article class="card report-card ${tones[index] || 'accent-orange'}">
      <span class="pill">焦點 ${index + 1}</span>
      <h3>${reportText(item, REPORT_FALLBACK_SUMMARY.top_findings[index] || '本週觀察')}</h3>
      <p>${index === 0 ? '先從這裡看本週最明顯的城市問題方向。' : index === 1 ? '這是目前最值得延伸到熱點與局處改善的題組。' : '這一項適合作為下一步資料補強與地點型改善重點。'}</p>
    </article>
  `).join('');
}

function renderReportBody(report, summary) {
  const summaryNode = document.getElementById('weekly-report-summary');
  const actionsNode = document.getElementById('weekly-report-actions');
  if (summaryNode) {
    summaryNode.textContent = reportText(summary?.summary, REPORT_FALLBACK_SUMMARY.summary);
  }
  if (actionsNode) {
    const actions = Array.isArray(report?.recommended_next_actions) && report.recommended_next_actions.length
      ? report.recommended_next_actions
      : REPORT_FALLBACK.recommended_next_actions;
    actionsNode.innerHTML = actions.map((item) => `<li>${reportText(item, '持續補充資料與熱點觀察。')}</li>`).join('');
  }
}

async function initWeeklyReport() {
  const [report, summary] = await Promise.all([
    loadReportJson('./data/weekly_system_report.json', REPORT_FALLBACK),
    loadReportJson('./data/ai_issue_summary.json', REPORT_FALLBACK_SUMMARY),
  ]);
  renderReportHeader(report);
  renderReportHighlights(summary);
  renderReportBody(report, summary);
}

document.addEventListener('DOMContentLoaded', () => {
  initWeeklyReport().catch((error) => {
    console.warn('Weekly report fallback content is active:', error);
  });
});
