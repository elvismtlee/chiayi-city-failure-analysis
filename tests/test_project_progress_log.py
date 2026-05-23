from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "docs" / "project_progress_log.md"


def test_project_progress_log_records_cycc_completion() -> None:
    content = LOG.read_text(encoding="utf-8")
    assert "嘉義城市故障分析資料庫進度紀錄" in content
    assert "141 筆" in content
    assert "PR #142" in content
    assert "PR #146" in content
    assert "CYCC Manual Crawl" in content


def test_project_progress_log_records_review_governance() -> None:
    content = LOG.read_text(encoding="utf-8")
    assert "PR #148" in content
    assert "PR #150" in content
    assert "CYCC review gate" in content
    assert "CYCC review queue schema" in content
    assert "citation_ready" in content
    assert "不自動發布" in content


def test_project_progress_log_records_open_data_inventory() -> None:
    content = LOG.read_text(encoding="utf-8")
    assert "PR #152" in content
    assert "29 筆" in content
    assert "internal_url_inventory" in content
    assert "open-data-inventory.html" in content
    assert "PR #149" in content
    assert "已由 PR #152 取代" in content


def test_project_progress_log_records_next_phase() -> None:
    content = LOG.read_text(encoding="utf-8")
    assert "feat/open-data-review-queue" in content
    assert "traffic_parking" in content
    assert "complaints_service" in content
    assert "不啟動 live crawler" in content
