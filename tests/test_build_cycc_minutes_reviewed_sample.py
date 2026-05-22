from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_cycc_minutes_reviewed_sample import (
    PUBLIC_USE_STATUS,
    REQUIRED_FIELDS,
    SENSITIVE_FIELDS,
    build_reviewed_sample,
    reviewed_id,
    write_reviewed_sample,
)


ROOT = Path(__file__).resolve().parents[1]
REVIEWED_PATH = ROOT / "data" / "processed" / "cycc_minutes_reviewed_sample.json"


def load_reviewed_sample() -> list[dict]:
    return json.loads(REVIEWED_PATH.read_text(encoding="utf-8"))


def test_generated_reviewed_sample_exists_and_parses() -> None:
    assert REVIEWED_PATH.exists()
    data = load_reviewed_sample()
    assert isinstance(data, list)
    assert data


def test_write_reviewed_sample_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "cycc_minutes_reviewed_sample.json"
    sample = write_reviewed_sample(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == sample


def test_reviewed_id_is_stable() -> None:
    first = build_reviewed_sample()
    second = build_reviewed_sample()
    assert [item["reviewed_id"] for item in first] == [item["reviewed_id"] for item in second]
    for item in first:
        assert item["reviewed_id"] == reviewed_id(item["raw_hash"])


def test_reviewed_sample_has_required_fields() -> None:
    for item in load_reviewed_sample():
        for field in REQUIRED_FIELDS:
            assert field in item, f"missing field: {field}"


def test_reviewed_sample_status_and_public_use_boundary() -> None:
    for item in load_reviewed_sample():
        assert item["review_status"] == "reviewed"
        assert item["public_use_status"] == PUBLIC_USE_STATUS
        assert "sample" in item["public_use_notes"].lower() or "not official" in item["public_use_notes"].lower()
        assert item["reviewer"] == "campaign_ops"
        assert item["reviewed_at"] == "2026-05-22"


def test_reviewed_sample_does_not_contain_sensitive_fields() -> None:
    for item in load_reviewed_sample():
        lowered_keys = {str(key).lower() for key in item.keys()}
        assert not lowered_keys & SENSITIVE_FIELDS


def test_reviewed_sample_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for reviewed sample builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_reviewed_sample()
