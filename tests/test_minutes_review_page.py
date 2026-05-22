from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "minutes-review.html"
SCRIPT = DASHBOARD_DIR / "minutes-review.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_minutes_review_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_minutes_review_page_discloses_fixture_only_safety_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "會議紀錄解析審核清單" in content
    assert "fixture-only" in content or "fixture" in content
    assert "不連網" in content
    assert "不使用 credential" in content
    assert "不寫入 Google Sheet" in content
    assert "unreviewed" in content


def test_minutes_review_page_does_not_use_polling_terms() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "民調" not in content
    assert "支持度調查" not in content


def test_minutes_review_page_has_required_render_targets() -> None:
    content = HTML.read_text(encoding="utf-8")
    for target in [
        'data-stat="total"',
        'data-stat="pending"',
        'data-stat="departments"',
        'data-stat="parser-statuses"',
        'data-render="minutes-review-queue"',
    ]:
        assert target in content


def test_minutes_review_renderer_reads_queue_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/cycc_minutes_review_queue.json" in content
    assert "bootMinutesReview" in content
    assert "renderStats" in content
    assert "renderQueue" in content


def test_minutes_review_renderer_keeps_existing_json_rendering_patterns() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "readJson" in content
    assert "escapeHtml" in content
    assert "issue_keywords" in content
    assert "raw_text_excerpt" in content
    assert "manual_minutes_review" in content


def test_minutes_review_page_is_in_site_map() -> None:
    content = SITE_MAP.read_text(encoding="utf-8")
    assert "會議紀錄審核" in content
    assert "./minutes-review.html" in content


def test_minutes_review_page_is_in_shared_nav() -> None:
    content = SHARED_NAV.read_text(encoding="utf-8")
    assert "會議紀錄審核" in content
    assert "./minutes-review.html" in content
