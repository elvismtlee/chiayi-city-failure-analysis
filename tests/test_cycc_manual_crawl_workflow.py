from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "cycc-manual-crawl.yml"


def test_cycc_workflow_has_manual_trigger() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")
    assert "workflow_dispatch" in content
    assert "push:" not in content
    assert "pull_request:" not in content


def test_cycc_workflow_runs_crawler_and_saves_outputs() -> None:
    content = WORKFLOW.read_text(encoding="utf-8")
    assert "python scripts/crawl_cycc_public_records.py" in content
    assert "actions/upload-artifact@v4" in content
    assert "cycc_minutes_metadata.csv" in content
    assert "cycc_question_video_metadata.csv" in content
    assert "cycc_public_records_crawl_report.json" in content
