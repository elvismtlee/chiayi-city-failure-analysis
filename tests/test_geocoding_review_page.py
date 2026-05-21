from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "geocoding-review.html"
SCRIPT = DASHBOARD_DIR / "geocoding-review.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"


def test_geocoding_review_page_exists_and_loads_scripts() -> None:
    assert HTML.exists()
    content = HTML.read_text(encoding="utf-8")
    assert "地理校正審核清單" in content
    assert "./shared-nav.js" in content
    assert "./geocoding-review.js" in content
    assert "./data/geocoding_review_queue.json" in content


def test_geocoding_review_page_has_required_render_targets() -> None:
    content = HTML.read_text(encoding="utf-8")
    for target in [
        'data-stat="total"',
        'data-stat="high"',
        'data-stat="prototype"',
        'data-render="geocoding-queue"',
    ]:
        assert target in content


def test_geocoding_review_renderer_reads_queue_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/geocoding_review_queue.json" in content
    assert "bootGeocodingReview" in content
    assert "renderStats" in content
    assert "renderQueue" in content


def test_geocoding_review_renderer_shows_priority_and_manual_review() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    for text in ["高優先", "中優先", "低優先", "manual_review_with_public_map", "suggested_query"]:
        assert text in content


def test_geocoding_review_page_is_in_site_map() -> None:
    content = SITE_MAP.read_text(encoding="utf-8")
    assert "座標審核" in content
    assert "./geocoding-review.html" in content


def test_geocoding_review_page_uses_safe_terms() -> None:
    content = HTML.read_text(encoding="utf-8") + SCRIPT.read_text(encoding="utf-8")
    assert "文化路夜市" not in content
    assert "支持度調查" not in content
    assert "個人評價" not in content or "不作為個人評價" in content
