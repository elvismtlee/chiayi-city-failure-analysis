from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "video-review.html"
SCRIPT = DASHBOARD_DIR / "video-review.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_video_review_page_exists_and_loads_scripts() -> None:
    assert HTML.exists()
    content = HTML.read_text(encoding="utf-8")
    assert "影音轉錄審核清單" in content
    assert "./shared-nav.js" in content
    assert "./video-review.js" in content
    assert "./data/transcript_review_queue.json" in content


def test_video_review_page_has_required_render_targets() -> None:
    content = HTML.read_text(encoding="utf-8")
    for target in [
        'data-stat="total"',
        'data-stat="metadata"',
        'data-stat="not-started"',
        'data-render="video-review-queue"',
    ]:
        assert target in content


def test_video_review_renderer_reads_queue_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/transcript_review_queue.json" in content
    assert "bootVideoReview" in content
    assert "renderStats" in content
    assert "renderQueue" in content


def test_video_review_renderer_shows_metadata_status() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    for text in ["需補 metadata", "中優先", "not_started", "recommended_action"]:
        assert text in content


def test_video_review_page_is_in_site_map_and_nav() -> None:
    site_map = SITE_MAP.read_text(encoding="utf-8")
    shared_nav = SHARED_NAV.read_text(encoding="utf-8")
    assert "影音轉錄審核" in site_map
    assert "./video-review.html" in site_map
    assert "影音轉錄審核" in shared_nav
    assert "video-review.html" in shared_nav


def test_video_review_page_uses_safe_terms() -> None:
    content = HTML.read_text(encoding="utf-8") + SCRIPT.read_text(encoding="utf-8")
    assert "下載影音" in content
    assert "不下載影音" in content
    assert "不呼叫 Whisper" in content
    assert "API key" in content
    assert "已完成轉錄" not in content
    assert "民調" not in content
    assert "支持度調查" not in content
