from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "cycc-review.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"
MINUTES_JSON = ROOT / "dashboard" / "data" / "cycc_minutes_metadata.json"
VIDEOS_JSON = ROOT / "dashboard" / "data" / "cycc_question_video_metadata.json"


def test_cycc_review_page_exists_with_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "CYCC 公開資料審核" in content
    assert "internal metadata" in content
    assert "manual review required" in content
    assert "no auto publish" in content
    assert "data-page=\"cycc-review\"" in content
    assert "data-cycc=\"minutes\"" in content
    assert "data-cycc=\"videos\"" in content
    assert "data-cycc=\"total\"" in content


def test_cycc_review_page_has_search_filter_and_table() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "搜尋 title" in content
    assert "question_videos" in content
    assert "141 筆逐筆 metadata" in content
    assert "review_status" in content


def test_site_pages_renders_cycc_review_report_and_table() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "renderCyccReview" in content
    assert "renderCyccMetadataTable" in content
    assert "setupCyccReviewTable" in content
    assert "cycc_minutes_metadata.csv" in content
    assert "cycc_question_video_metadata.csv" in content
    assert "./data/cycc_minutes_metadata.json" in content
    assert "./data/cycc_question_video_metadata.json" in content
    assert "./data/cycc_public_records_crawl_report.json" in content
    assert "data-cycc=\"total\"" in content


def test_cycc_review_json_files_exist() -> None:
    assert MINUTES_JSON.exists()
    assert VIDEOS_JSON.exists()
