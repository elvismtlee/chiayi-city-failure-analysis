from __future__ import annotations

import json
from pathlib import Path

from scripts.build_public_material_review_queue import build_public_material_review_queue, write_public_material_review_queue


def test_build_public_material_review_queue_has_required_fields() -> None:
    data = build_public_material_review_queue(
        social_records=[{"post_id": "post-001", "headline": "測試標題", "issue_title": "測試議題"}],
        video_records=[],
    )
    assert data["public_use_status"] == "internal_public_review_queue"
    assert data["generated_at"].endswith("+08:00")
    assert data["items"]
    item = data["items"][0]
    for field in ["review_id", "item_type", "title", "risk_level", "review_status", "evidence_status", "required_action", "notes"]:
        assert field in item
    assert item["review_status"] == "needs_review"


def test_write_public_material_review_queue_outputs_valid_json(tmp_path: Path) -> None:
    output = tmp_path / "public_material_review_queue.json"
    data = write_public_material_review_queue(output)
    assert output.exists()
    assert output.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(output.read_text(encoding="utf-8")) == data
