async function readJson(path, fallback) { try { const response = await fetch(path, { cache: 'no-store' }); if (!response.ok) throw new Error(path); return await response.json(); } catch (error) { console.warn('Use fallback:', path, error); return fallback; } }
function setText(selector, value) { const node = document.querySelector(selector); if (node) node.textContent = value; }
function renderStats(items) { const departments = new Set(items.map(item => item.responsible_department).filter(Boolean)); setText('[data-stat="total"]', items.length); setText('[data-stat="needs-review"]', items.filter(item => item.review_status === 'needs_policy_review').length); setText('[data-stat="departments"]', departments.size); }
function renderDrafts(items) { const node = document.querySelector('[data-render="policy-drafts"]'); if (node) node.textContent = `${items.length} policy draft candidates require manual review.`; }
async function bootPolicyDrafts() { const items = await readJson('./data/policy_draft_candidates.json', []); renderStats(items); renderDrafts(items); }
bootPolicyDrafts();
