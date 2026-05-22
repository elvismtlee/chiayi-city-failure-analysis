from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_policy_draft_candidates import (
    PUBLIC_USE_STATUS,
    RECOMMENDED_NEXT_STEP,
    REQUIRED_FIELDS,
    REVIEW_STATUS,
    SENSITIVE_FIELDS,
    build_policy_drafts,
    draft_id,
    write_policy_drafts,
)


ROOT = Path(__file__).resolve().parents[1]
POLICY_DRAFTS_PATH = ROOT / "dashboard" / "data" / "policy_draft_candidates.json"


def load_policy_drafts() -> list[dict]:
    return json.loads(POLICY_DRAFTS_PATH.read_text(encoding="utf-8"))


def test_generated_policy_drafts_exist_and_parse() -> None:
    assert POLICY_DRAFTS_PATH.exists()
    data = load_policy_drafts()
    assert isinstance(data, list)
    assert data


def test_write_policy_drafts_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "policy_draft_candidates.json"
    drafts = write_policy_drafts(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == drafts


def test_policy_draft_id_is_stable() -> None:
    first = build_policy_drafts()
    second = build_policy_drafts()
    assert [item["draft_id"] for item in first] == [item["draft_id"] for item in second]
    for item in first:
        assert item["draft_id"] == draft_id(item["source_candidate_id"])


def test_policy_drafts_have_required_fields() -> None:
    for item in load_policy_drafts():
        for field in REQUIRED_FIELDS:
            assert field in item, f"missing field: {field}"


def test_policy_draft_values_require_review() -> None:
    for item in load_policy_drafts():
        assert isinstance(item["possible_root_causes"], list)
        assert isinstance(item["policy_options"], list)
        assert len(item["policy_options"]) >= 3
        assert item["review_status"] == REVIEW_STATUS
        assert item["public_use_status"] == PUBLIC_USE_STATUS
        assert item["recommended_next_step"] == RECOMMENDED_NEXT_STEP
        assert "人工確認" in item["risk_notes"]


def test_policy_drafts_do_not_contain_sensitive_fields_or_official_policy_claims() -> None:
    for item in load_policy_drafts():
        lowered_keys = {str(key).lower() for key in item.keys()}
        assert not lowered_keys & SENSITIVE_FIELDS
        serialized = json.dumps(item, ensure_ascii=False)
        assert "正式政見" not in serialized


def test_policy_draft_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for policy draft builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_policy_drafts()
