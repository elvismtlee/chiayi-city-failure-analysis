import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_MAP = ROOT / 'dashboard' / 'data' / 'site_map.json'


def test_site_map_prioritizes_public_pages() -> None:
    data = json.loads(SITE_MAP.read_text(encoding='utf-8'))
    first_paths = [item['path'] for item in data[:10]]
    assert './index.html' in first_paths
    assert './map.html' in first_paths
    assert './command-center.html' in first_paths
    assert './sources.html' in first_paths
    assert './methodology.html' in first_paths
    assert './health-check.html' in first_paths
    assert './insights.html' in first_paths
    assert './reports.html' in first_paths
    assert './project-landing.html' in first_paths


def test_site_map_public_descriptions_are_user_facing() -> None:
    text = SITE_MAP.read_text(encoding='utf-8')
    assert '城市問題儀表板' in text
    assert '城市熱點地圖' in text
    assert '城市資料總控台' in text
    assert '資料來源' in text
    assert '城市故障分析方法論' in text
    assert '網站與資料健康檢查' in text
    assert 'public_prototype' in text
