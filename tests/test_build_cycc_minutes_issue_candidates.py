from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_cycc_minutes_issue_candidates import (
    BANNED_TERMS,
    REQUIRED_FIELDS,
    SENSITIVE_FIELDS,
    build_issue_candidates,
    candidate_id,
    write_issue_candidates,
)


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_issue_candidates.json"


def load_candidates() -> list[dict]:
    return json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))


def test_generated_issue_candidates_exist_and_parse() -> None:
    assert CANDIDATES_PATH.exists()
    data = load_candidates()
    assert isinstance(data, list)
    assert data


def test_write_issue_candidates_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "cycc_minutes_issue_candidates.json"
    candidates = write_issue_candidates(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == candidates


def test_candidate_id_is_stable() -> None:
    first = build_issue_candidates()
    second = build_issue_candidates()
    assert [item["candidate_id"] for item in first] == [item["candidate_id"] for item in second]
    for item in first:
        assert item["candidate_id"] == candidate_id(item["reviewed_id"])


def test_issue_candidates_have_required_fields() -> None:
    for item in load_candidates():
        for field in REQUIRED_FIELDS:
            assert field in item, f"missing field: {field}"


def test_issue_candidate_values_are_sample_only() -> None:
    for item in load_candidates():
        assert isinstance(item["issue_keywords"], list)
        assert item["confidence_level"] == "sample_only"
        assert item["recommended_follow_up"] == "manual_policy_review"
        assert "sample" in item["notes"].lower() or "not official" in item["notes"].lower()


def test_issue_candidates_do_not_contain_sensitive_fields_or_polling_terms() -> None:
    for item in load_candidates():
        lowered_keys = {str(key).lower() for key in item.keys()}
        assert not lowered_keys & SENSITIVE_FIELDS
        serialized = json.dumps(item, ensure_ascii=False)
        for term in BANNED_TERMS:
            assert term not in serialized


def test_issue_candidate_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for issue candidate builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_issue_candidates()
