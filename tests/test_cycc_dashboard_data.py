import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "dashboard" / "data" / "cycc_public_records_crawl_report.json"


def test_cycc_dashboard_report_exists_and_is_internal() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    assert report["public_use_status"] == "internal_crawl_report"
    assert report["manual_review_required"] is True
    assert report["no_auto_publish"] is True
    assert report["no_personal_data"] is True
    assert report["crawl_scope"] == "metadata_only"
    assert report["source_id"] == "CYCC_PUBLIC_RECORDS"


def test_cycc_dashboard_report_has_expected_counts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    output_files = report["output_files"]
    counts = {item["path"]: item["record_count"] for item in output_files}
    assert counts["data/raw/cycc_minutes_metadata.csv"] == 10
    assert counts["data/raw/cycc_question_video_metadata.csv"] == 131
    assert sum(counts.values()) == 141
    assert report["artifact"]["artifact_id"] == 7169377174
