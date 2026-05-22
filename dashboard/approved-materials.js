async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    const node = document.querySelector('[data-render="approved-materials"]');
    if (node) node.textContent = `讀取已核准素材失敗：${error.message}`;
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
  badge.textContent = valueOrPending(item.item_type);
  const meta = document.createElement('div');
  meta.className = 'meta';
  [
    ['核准時間', item.approved_at],
    ['核准者', item.approved_by],
    ['使用提醒', item.public_use_notes],
    ['來源檔案', Array.isArray(item.source_files) ? item.source_files.join(', ') : item.source_files],
  ].forEach(([label, value]) => {
    const row = document.createElement('div');
    row.textContent = `${label}：${valueOrPending(value)}`;
    meta.appendChild(row);
  });
  card.append(title, badge, meta);
  return card;
}

async function bootApprovedMaterials() {
  const payload = await readJson('./data/approved_materials_sample.json', { items: [] });
  const items = Array.isArray(payload) ? payload : payload.items || [];
  const node = document.querySelector('[data-render="approved-materials"]');
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有已核准素材樣本。approved 仍需人工手動發布。';
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(makeCard(item)));
}

bootApprovedMaterials();
