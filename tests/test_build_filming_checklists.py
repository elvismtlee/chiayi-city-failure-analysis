from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_filming_checklists import (
    PUBLIC_USE_STATUS,
    RECOMMENDED_NEXT_STEP,
    REVIEW_STATUS,
    SENSITIVE_FIELDS,
    build_filming_checklists,
    checklist_id,
    write_filming_checklists,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "dashboard" / "data" / "filming_checklists.json"


def load_data() -> list[dict]:
    return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))


def test_filming_checklists_json_exists() -> None:
    assert OUTPUT_PATH.exists()
    assert isinstance(load_data(), list)
    assert load_data()


def test_filming_checklist_ids_are_stable() -> None:
    first = build_filming_checklists()
    second = build_filming_checklists()
    assert [item["checklist_id"] for item in first] == [item["checklist_id"] for item in second]
    for item in first:
        assert item["checklist_id"] == checklist_id(item["source_script_id"])


def test_filming_checklists_have_required_review_fields() -> None:
    for item in load_data():
        assert isinstance(item["scene_tasks"], list)
        assert isinstance(item["props_needed"], list)
        assert isinstance(item["estimated_minutes"], int)
        assert item["review_status"] == REVIEW_STATUS
        assert item["public_use_status"] == PUBLIC_USE_STATUS
        assert item["recommended_next_step"] == RECOMMENDED_NEXT_STEP


def test_filming_checklists_avoid_sensitive_fields_and_privacy_violations() -> None:
    serialized = json.dumps(load_data(), ensure_ascii=False)
    for term in ["偷拍", "侵犯隱私"]:
        assert term not in serialized
    for item in load_data():
        assert not ({key.lower() for key in item} & SENSITIVE_FIELDS)


def test_write_filming_checklists_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "filming_checklists.json"
    data = write_filming_checklists(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == data


def test_filming_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for filming checklist builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_filming_checklists()
