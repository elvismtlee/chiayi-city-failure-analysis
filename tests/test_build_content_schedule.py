from __future__ import annotations

import json
from pathlib import Path

from scripts.build_content_schedule import build_content_schedule, write_content_schedule


def test_build_content_schedule_has_required_fields() -> None:
    data = build_content_schedule([
        {
            "post_id": "post-001",
            "channel": "facebook",
            "headline": "測試標題",
            "issue_title": "測試議題",
        }
    ])
    assert data["public_use_status"] == "internal_content_schedule"
    assert data["generated_at"].endswith("+08:00")
    assert data["items"]
    item = data["items"][0]
    for field in ["schedule_id", "date", "channel", "title", "status", "review_required", "source_issue", "notes"]:
        assert field in item
    assert item["review_required"] is True
    assert "manual publishing" in item["notes"]


def test_write_content_schedule_outputs_valid_json(tmp_path: Path) -> None:
    output = tmp_path / "content_schedule.json"
    data = write_content_schedule(output)
    assert output.exists()
    assert output.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(output.read_text(encoding="utf-8")) == data
