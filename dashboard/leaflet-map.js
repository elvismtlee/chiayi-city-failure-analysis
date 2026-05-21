const CHIAYI_CENTER = [23.4801, 120.4491];
const FALLBACK_HOTSPOT_COORDS = [
  [23.4808, 120.4497],
  [23.4787, 120.4456],
  [23.4758, 120.4528],
];

async function loadHotspots() {
  try {
    const response = await fetch('./data/hotspots.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('hotspots.json');
    return await response.json();
  } catch (error) {
    console.warn('Use empty hotspots fallback:', error);
    return [];
  }
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

function createPopupContent(hotspot, isPrototype) {
  const prototypeNote = isPrototype ? '<p class="map-note">prototype 座標，待正式地理資料更新。</p>' : '';
  return `
    <section class="map-popup">
      <h3>${hotspot.name || '未命名熱點'}</h3>
      <p><b>行政區：</b>${hotspot.district || '待確認'}</p>
      <p><b>議題：</b>${hotspot.category || '待分類'}</p>
      <p><b>對應局處：</b>${hotspot.department || '待確認'}</p>
      <p><b>城市故障指數：</b>${hotspot.score || 0}</p>
      <p><b>建議行動：</b>${hotspot.action || '待研擬'}</p>
      ${prototypeNote}
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

  hotspots.forEach((hotspot, index) => {
    const { lat, lng, isPrototype } = getHotspotLatLng(hotspot, index);
    const marker = L.marker([lat, lng], { icon: createMarkerIcon(hotspot.score) })
      .addTo(map)
      .bindPopup(createPopupContent(hotspot, isPrototype));
    bounds.push(marker.getLatLng());
  });

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [34, 34], maxZoom: 16 });
  }
}

bootLeafletHotspotMap();
