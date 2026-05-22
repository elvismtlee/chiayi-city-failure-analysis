async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    const node = document.querySelector('[data-render="daily-execution"]');
    if (node) node.textContent = `讀取每日執行清單失敗：${error.message}`;
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
  title.textContent = valueOrPending(item.task);
  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.textContent = `${valueOrPending(item.priority)} / ${valueOrPending(item.status)}`;
  const meta = document.createElement('div');
  meta.className = 'meta';
  [
    ['預估時間', `${valueOrPending(item.estimated_minutes)} 分鐘`],
    ['相關頁面', item.related_dashboard],
    ['備註', item.notes],
  ].forEach(([label, value]) => {
    const row = document.createElement('div');
    row.textContent = `${label}：${valueOrPending(value)}`;
    meta.appendChild(row);
  });
  card.append(title, badge, meta);
  return card;
}

async function bootDailyExecution() {
  const payload = await readJson('./data/daily_execution_list.json', { items: [] });
  const items = Array.isArray(payload) ? payload : payload.items || [];
  const node = document.querySelector('[data-render="daily-execution"]');
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有每日執行項目。internal / manual review / manual publishing only。';
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(makeCard(item)));
}

bootDailyExecution();
