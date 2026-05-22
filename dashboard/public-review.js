async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    const node = document.querySelector('[data-render="public-review"]');
    if (node) node.textContent = `讀取公開審核佇列失敗：${error.message}`;
    return fallback;
  }
}

function valueOrPending(value) {
  return value === undefined || value === null || value === '' ? '待補' : String(value);
}

function makeCard(item) {
  const card = document.createElement('article');
  card.className = 'card';
  const title = document.createElement('h3');
  title.textContent = valueOrPending(item.title);
  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.textContent = `${valueOrPending(item.risk_level)} / ${valueOrPending(item.review_status)}`;
  const meta = document.createElement('div');
  meta.className = 'meta';
  [
    ['類型', item.item_type],
    ['證據狀態', item.evidence_status],
    ['必要動作', item.required_action],
    ['備註', item.notes],
  ].forEach(([label, value]) => {
    const row = document.createElement('div');
    row.textContent = `${label}：${valueOrPending(value)}`;
    meta.appendChild(row);
  });
  card.append(title, badge, meta);
  return card;
}

async function bootPublicReview() {
  const payload = await readJson('./data/public_material_review_queue.json', { items: [] });
  const items = Array.isArray(payload) ? payload : payload.items || [];
  const node = document.querySelector('[data-render="public-review"]');
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有公開審核項目。未通過人工審核，不可公開使用。';
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(makeCard(item)));
}

bootPublicReview();
