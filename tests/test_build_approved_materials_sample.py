from __future__ import annotations

import json
from pathlib import Path

from scripts.build_approved_materials_sample import build_approved_materials_sample, write_approved_materials_sample


def test_build_approved_materials_sample_has_required_fields() -> None:
    data = build_approved_materials_sample({
        "items": [
            {
                "item_type": "social_post",
                "title": "測試素材",
                "review_status": "approved",
            }
        ]
    })
    assert data["public_use_status"] == "internal_approved_materials_sample"
    assert data["generated_at"].endswith("+08:00")
    assert data["items"]
    item = data["items"][0]
    for field in ["material_id", "item_type", "title", "approved_at", "approved_by", "source_files", "public_use_notes"]:
        assert field in item
    assert "Manual publishing" in " ".join(data["notes"])


def test_write_approved_materials_sample_outputs_valid_json(tmp_path: Path) -> None:
    output = tmp_path / "approved_materials_sample.json"
    data = write_approved_materials_sample(output)
    assert output.exists()
    assert output.read_text(encoding="utf-8").endswith("\n")
    assert json.loads(output.read_text(encoding="utf-8")) == data
