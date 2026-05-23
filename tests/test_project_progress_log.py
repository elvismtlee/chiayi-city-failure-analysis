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


def test_project_progress_log_records_next_phase() -> None:
    content = LOG.read_text(encoding="utf-8")
    assert "feat/open-data-url-inventory-dashboard" in content
    assert "traffic_parking" in content
    assert "complaints_service" in content
    assert "不啟動 live crawler" in content
