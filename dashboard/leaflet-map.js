const CHIAYI_CENTER = [23.4801, 120.4491];
const FALLBACK_HOTSPOT_COORDS = [
  [23.4808, 120.4497],
  [23.4787, 120.4456],
  [23.4758, 120.4528],
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
      console.warn('Use empty hotspots fallback:', legacyError);
      return [];
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

async function bootLeafletHotspotMap() {
  const node = document.querySelector('[data-render="leaflet_hotspot_map"]');
  if (!node || typeof L === 'undefined') return;

  const map = L.map(node, { scrollWheelZoom: false }).setView(CHIAYI_CENTER, 15);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  const hotspots = await loadHotspots();
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
