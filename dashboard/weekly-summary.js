async function readJson(path, fallback) { try { const response = await fetch(path, { cache: 'no-store' }); if (!response.ok) throw new Error(path); return await response.json(); } catch (error) { console.warn('Use fallback:', path, error); return fallback; } }
function setText(selector, value) { const node = document.querySelector(selector); if (node) node.textContent = value; }
function renderSummary(summary) { const departments = summary.department_summary || []; const keywords = summary.keyword_summary || []; setText('[data-stat="period"]', `${summary.week_start || '–'} 至 ${summary.week_end || '–'}`); setText('[data-stat="total"]', summary.total_candidates ?? 0); setText('[data-stat="departments"]', departments.length); setText('[data-stat="keywords"]', keywords.length); }
async function bootWeeklySummary() { const summary = await readJson('./data/weekly_summary_draft.json', {}); renderSummary(summary); }
bootWeeklySummary();
