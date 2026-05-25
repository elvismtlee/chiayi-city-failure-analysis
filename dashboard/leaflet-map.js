const CHIAYI_CENTER = [23.4801, 120.4491];
const FALLBACK_HOTSPOT_COORDS = [
  [23.4808, 120.4497],
  [23.4787, 120.4456],
  [23.4758, 120.4528],
];
const FALLBACK_HOTSPOTS = [
  {
    name: '文化路商圈',
    district: '西區',
    category: '停車 / 人行',
    department: '交通處',
    score: 92,
    action: '商圈動線與停車熱點專案',
    lat: 23.4808,
    lng: 120.4497,
    isPrototype: true,
    sourceType: 'fallback',
  },
  {
    name: '市場周邊',
    district: '西區',
    category: '垃圾 / 動線',
    department: '環保局 / 建設處',
    score: 78,
    action: '市場周邊環境改善與卸貨規劃',
    lat: 23.4787,
    lng: 120.4456,
    isPrototype: true,
    sourceType: 'fallback',
  },
  {
    name: '學校周邊',
    district: '西區',
    category: '通學安全',
    department: '交通處 / 教育處',
    score: 71,
    action: '通學步道與接送區改善',
    lat: 23.4758,
    lng: 120.4528,
    isPrototype: true,
    sourceType: 'fallback',
  },
];

async function readJson(path) {
  const response = await fetch(path, { cache: 'no-store' });
  if (!response.ok) throw new Error(path);
  return await response.json();
}

async function loadHotspots() {
  try {
    const geojson = await readJson('./data/hotspots.geojson');
    return normalizeGeoJsonHotspots(geojson);
  } catch (geojsonError) {
    console.warn('Use hotspots.json fallback:', geojsonError);
    try {
      const hotspots = await readJson('./data/hotspots.json');
      return normalizeLegacyHotspots(hotspots);
    } catch (legacyError) {
      console.warn('Use built-in hotspots fallback:', legacyError);
      return FALLBACK_HOTSPOTS;
    }
  }
}

function normalizeGeoJsonHotspots(geojson) {
  if (!geojson || geojson.type !== 'FeatureCollection' || !Array.isArray(geojson.features)) {
    throw new Error('Invalid hotspots.geojson');
  }

  return geojson.features.map((feature, index) => {
    const properties = feature.properties || {};
    const coordinates = feature.geometry?.coordinates || [];
    const lng = Number(coordinates[0]);
    const lat = Number(coordinates[1]);
    const hasCoordinates = Number.isFinite(lat) && Number.isFinite(lng);
    const fallback = FALLBACK_HOTSPOT_COORDS[index % FALLBACK_HOTSPOT_COORDS.length];
    const isPrototype = properties.geo_precision === 'prototype' || properties.review_status === 'prototype';

    return {
      name: properties.name,
      district: properties.district,
      category: properties.category,
      department: properties.department,
      score: properties.score,
      action: properties.action,
      lat: hasCoordinates ? lat : fallback[0],
      lng: hasCoordinates ? lng : fallback[1],
      isPrototype: isPrototype || !hasCoordinates,
      sourceType: 'geojson',
    };
  });
}

function normalizeLegacyHotspots(hotspots) {
  if (!Array.isArray(hotspots)) return [];
  return hotspots.map((hotspot, index) => {
    const { lat, lng, isPrototype } = getHotspotLatLng(hotspot, index);
    return {
      ...hotspot,
      lat,
      lng,
      isPrototype,
      sourceType: 'legacy-json',
    };
  });
}

function getHotspotLatLng(hotspot, index) {
  const lat = Number(hotspot.lat);
  const lng = Number(hotspot.lng);
  if (Number.isFinite(lat) && Number.isFinite(lng)) {
    return { lat, lng, isPrototype: false };
  }
  const fallback = FALLBACK_HOTSPOT_COORDS[index % FALLBACK_HOTSPOT_COORDS.length];
  return { lat: fallback[0], lng: fallback[1], isPrototype: true };
}

function getScoreClass(score) {
  const numeric = Number(score || 0);
  if (numeric >= 85) return 'high';
  if (numeric >= 70) return 'medium';
  return 'low';
}

function createMarkerIcon(score) {
  const scoreClass = getScoreClass(score);
  return L.divIcon({
    className: `cyfa-marker cyfa-marker-${scoreClass}`,
    html: `<span>${Number(score || 0)}</span>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -18],
  });
}

function createPopupContent(hotspot) {
  const prototypeNote = hotspot.isPrototype ? '<p class="map-note">prototype 座標，待正式地理資料更新。</p>' : '';
  const sourceNote = hotspot.sourceType === 'geojson' ? '<p class="map-note">資料格式：GeoJSON</p>' : '';
  return `
    <section class="map-popup">
      <h3>${hotspot.name || '未命名熱點'}</h3>
      <p><b>行政區：</b>${hotspot.district || '待確認'}</p>
      <p><b>議題：</b>${hotspot.category || '待分類'}</p>
      <p><b>對應局處：</b>${hotspot.department || '待確認'}</p>
      <p><b>城市故障指數：</b>${hotspot.score || 0}</p>
      <p><b>建議行動：</b>${hotspot.action || '待研擬'}</p>
      ${prototypeNote}
      ${sourceNote}
    </section>
  `;
}

function renderFallbackMap(node, hotspots) {
  const items = hotspots.length ? hotspots : FALLBACK_HOTSPOTS;
  node.innerHTML = `
    <div class="map-fallback-shell">
      <div class="map-fallback-header">
        <strong>prototype map fallback</strong>
        <span>外部地圖底圖未載入時，仍保留熱點內容與行動建議。</span>
      </div>
      <div class="map-fallback-grid">
        <article class="map-fallback-panel">
          <div class="map-fallback-canvas">
            ${items.map((hotspot) => `
              <div class="map-fallback-pin" style="left:${((hotspot.lng - 120.44) * 420).toFixed(0)}px;top:${((23.485 - hotspot.lat) * 900).toFixed(0)}px;">
                <span>${hotspot.score}</span>
              </div>
              <div class="map-fallback-bubble" style="left:${(((hotspot.lng - 120.44) * 420) + 16).toFixed(0)}px;top:${(((23.485 - hotspot.lat) * 900) - 12).toFixed(0)}px;">
                <strong>${hotspot.name}</strong>
                ${hotspot.category}
              </div>
            `).join('')}
          </div>
        </article>
        <aside class="map-fallback-list">
          ${items.map((hotspot) => `
            <article class="map-fallback-item">
              <div>
                <strong>${hotspot.name}</strong>
                <p>${hotspot.category}｜${hotspot.department}</p>
              </div>
              <div>
                <b>${hotspot.score}</b>
                <span>${hotspot.action}</span>
              </div>
            </article>
          `).join('')}
        </aside>
      </div>
    </div>
  `;
}

async function bootLeafletHotspotMap() {
  const node = document.querySelector('[data-render="leaflet_hotspot_map"]');
  if (!node) return;

  const hotspots = await loadHotspots();
  if (typeof L === 'undefined') {
    renderFallbackMap(node, hotspots);
    return;
  }

  const map = L.map(node, { scrollWheelZoom: false }).setView(CHIAYI_CENTER, 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  const bounds = [];

  hotspots.forEach(hotspot => {
    const marker = L.marker([hotspot.lat, hotspot.lng], { icon: createMarkerIcon(hotspot.score) })
      .addTo(map)
      .bindPopup(createPopupContent(hotspot));
    bounds.push(marker.getLatLng());
  });

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [34, 34], maxZoom: 16 });
  }
}

bootLeafletHotspotMap();
