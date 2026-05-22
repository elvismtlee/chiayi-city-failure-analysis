from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_cycc_minutes_review_queue import (
    REQUIRED_FIELDS,
    SENSITIVE_FIELDS,
    build_queue,
    build_queue_item,
    review_priority,
    write_queue,
)
from scripts.parse_cycc_minutes_sample import parse_all_fixtures


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_review_queue.json"


def load_queue() -> list[dict]:
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def test_generated_cycc_minutes_review_queue_exists_and_parses() -> None:
    assert QUEUE_PATH.exists()
    data = load_queue()
    assert isinstance(data, list)
    assert data


def test_write_queue_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "cycc_minutes_review_queue.json"
    queue = write_queue(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == queue


def test_queue_id_is_stable() -> None:
    first = build_queue()
    second = build_queue()
    assert [item["queue_id"] for item in first] == [item["queue_id"] for item in second]
    for item in first:
        assert item["queue_id"] == f"cycc-minutes-{item['raw_hash'][:12]}"


def test_queue_items_have_required_fields() -> None:
    for item in load_queue():
        for field in REQUIRED_FIELDS:
            assert field in item, f"missing field: {field}"


def test_issue_keywords_are_lists() -> None:
    for item in load_queue():
        assert isinstance(item["issue_keywords"], list)
        assert item["issue_keywords"]


def test_raw_text_excerpt_is_limited_to_120_chars() -> None:
    for item in load_queue():
        assert len(item["raw_text_excerpt"]) <= 120


def test_parser_and_review_status_are_fixture_initial_values() -> None:
    for item in load_queue():
        assert item["parser_status"] == "parsed_from_fixture"
        assert item["review_status"] == "unreviewed"
        assert item["needs_manual_review"] is True
        assert item["recommended_action"] == "manual_minutes_review"
        assert "fixture-only" in item["notes"]
        assert "not been manually reviewed" in item["notes"]


def test_review_priority_flags_missing_metadata() -> None:
    assert review_priority({"meeting_date": "2026-05-01", "councilor_name": "測試議員"}) == "normal"
    assert review_priority({"meeting_date": "", "councilor_name": "測試議員"}) == "needs_metadata_review"
    assert review_priority({"meeting_date": "2026-05-01", "councilor_name": ""}) == "needs_metadata_review"


def test_queue_does_not_contain_sensitive_fields() -> None:
    for item in load_queue():
        lowered_keys = {str(key).lower() for key in item.keys()}
        assert not lowered_keys & SENSITIVE_FIELDS


def test_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for fixture queue builder")
    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_queue()


def test_builder_uses_fixture_parser_output() -> None:
    fixture_records = parse_all_fixtures()
    queue = build_queue()
    assert len(queue) == len(fixture_records)
    assert queue[0] == build_queue_item(fixture_records[0])
