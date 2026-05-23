import json
from pathlib import Path

from scripts import build_open_data_top10_review_tasks as builder


ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "dashboard" / "data" / "open_data_readiness_report.json"


def test_build_open_data_top10_review_tasks_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_top10_review_tasks.json"
    payload = builder.build_open_data_top10_review_tasks(READINESS, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_top10_review_tasks"
    assert data["public_use_status"] == "internal_top10_review_tasks"
    assert data["total_count"] == 10
    assert data["source_report_count"] == 29
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_top10_review_tasks_task_defaults_and_rules(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_top10_review_tasks.json"
    data = builder.build_open_data_top10_review_tasks(READINESS, output_path)

    for task in data["tasks"]:
        assert task["review_status"] == "not_started"
        assert task["no_live_crawler"] is True
        assert len(task["review_steps"]) >= 5
        assert len(task["acceptance_criteria"]) >= 5
        assert task["readiness_level"] != "blocked"
