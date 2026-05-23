from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-day1-operation-board.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_day1_operation_board_page_exists_with_required_sections() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "openDataDay1OperationBoard" in content
    assert "Day 1 人工審核操作看板" in content
    assert "timeline" in content
    assert "task-card" in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_day1_operation_board() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_day1_manual_review_operation_board.json" in content
    assert "setupOpenDataDay1OperationBoard" in content
    assert "open-data-day1-operation-board" in content
