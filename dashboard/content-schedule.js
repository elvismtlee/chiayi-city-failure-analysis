async function readJson(path, fallback) {
  try {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: ${response.status}`);
    return await response.json();
  } catch (error) {
    const node = document.querySelector('[data-render="content-schedule"]');
    if (node) node.textContent = `讀取內容排程失敗：${error.message}`;
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
  badge.textContent = valueOrPending(item.status);
  const meta = document.createElement('div');
  meta.className = 'meta';
  [
    ['日期', item.date],
    ['Channel', item.channel],
    ['來源議題', item.source_issue],
    ['審核需求', item.review_required ? '需要人工審核' : '待確認'],
    ['備註', item.notes],
  ].forEach(([label, value]) => {
    const row = document.createElement('div');
    row.textContent = `${label}：${valueOrPending(value)}`;
    meta.appendChild(row);
  });
  card.append(title, badge, meta);
  return card;
}

async function bootContentSchedule() {
  const payload = await readJson('./data/content_schedule.json', { items: [] });
  const items = Array.isArray(payload) ? payload : payload.items || [];
  const node = document.querySelector('[data-render="content-schedule"]');
  if (!node) return;
  node.textContent = '';
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '目前沒有內容排程項目。internal / manual review / manual publishing only。';
    node.appendChild(empty);
    return;
  }
  items.forEach(item => node.appendChild(makeCard(item)));
}

bootContentSchedule();
