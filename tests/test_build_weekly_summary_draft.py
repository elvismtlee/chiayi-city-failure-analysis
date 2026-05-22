from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_weekly_summary_draft import (
    PUBLIC_USE_STATUS,
    REQUIRED_FIELDS,
    SENSITIVE_FIELDS,
    build_weekly_summary,
    write_weekly_summary,
)


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_issue_candidates.json"
SUMMARY_PATH = ROOT / "dashboard" / "data" / "weekly_summary_draft.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_generated_weekly_summary_exists_and_parses() -> None:
    assert SUMMARY_PATH.exists()
    summary = load_json(SUMMARY_PATH)
    assert isinstance(summary, dict)


def test_write_weekly_summary_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "weekly_summary_draft.json"
    summary = write_weekly_summary(output_path)
    assert output_path.exists()
    assert load_json(output_path) == summary


def test_weekly_summary_required_fields_and_counts() -> None:
    summary = load_json(SUMMARY_PATH)
    candidates = load_json(CANDIDATES_PATH)
    for field in REQUIRED_FIELDS:
        assert field in summary, f"missing field: {field}"
    assert summary["total_candidates"] == len(candidates)
    assert "dashboard/data/cycc_minutes_issue_candidates.json" in summary["source_files"]


def test_weekly_summary_collections_are_structured() -> None:
    summary = load_json(SUMMARY_PATH)
    assert isinstance(summary["department_summary"], (list, dict))
    assert isinstance(summary["keyword_summary"], (list, dict))
    assert isinstance(summary["top_issues"], list)
    assert isinstance(summary["needs_review"], list)
    assert isinstance(summary["suggested_policy_topics"], list)


def test_top_issues_come_from_issue_candidates() -> None:
    summary = load_json(SUMMARY_PATH)
    candidates = load_json(CANDIDATES_PATH)
    candidate_ids = {item["candidate_id"] for item in candidates}
    for item in summary["top_issues"]:
        assert item["source_candidate_id"] in candidate_ids


def test_weekly_summary_public_use_boundary() -> None:
    summary = load_json(SUMMARY_PATH)
    assert summary["public_use_status"] == PUBLIC_USE_STATUS
    notes = summary["notes"].lower()
    assert "internal draft" in notes or "not official" in notes


def test_weekly_summary_does_not_contain_sensitive_fields() -> None:
    summary = load_json(SUMMARY_PATH)
    lowered_keys = {str(key).lower() for key in summary.keys()}
    assert not lowered_keys & SENSITIVE_FIELDS


def test_weekly_summary_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for weekly summary builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_weekly_summary()
