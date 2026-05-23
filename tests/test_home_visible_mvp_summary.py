import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "dashboard" / "data" / "home_visible_mvp_summary.json"


def test_home_visible_mvp_summary_exists() -> None:
    assert SUMMARY_PATH.exists()


def test_home_visible_mvp_summary_values() -> None:
    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))

    assert summary["public_use_status"] == "internal_visible_mvp_home_summary"
    assert summary["visible_kpis"]["official_url_inventory_count"] == 29
    assert summary["visible_kpis"]["top10_review_tasks_count"] == 10
    assert summary["visible_kpis"]["day1_task_count"] == 3
    assert summary["visible_kpis"]["patch_draft_count"] == 10
    assert summary["visible_kpis"]["sample_result_count"] == 3
    assert summary["visible_kpis"]["manual_review_form_count"] == 3
    assert summary["visible_kpis"]["health_status"] == "ok"
    assert summary["no_live_crawler"] is True
    assert summary["manual_review_required"] is True
    assert summary["no_auto_publish"] is True
    assert summary["no_personal_data"] is True
    assert summary["crawler_execution_allowed"] is False
