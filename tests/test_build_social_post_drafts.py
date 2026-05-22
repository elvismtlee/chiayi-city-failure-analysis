from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_social_post_drafts import (
    CHANNELS,
    PUBLIC_USE_STATUS,
    RECOMMENDED_NEXT_STEP,
    REVIEW_STATUS,
    SENSITIVE_FIELDS,
    build_social_post_drafts,
    post_id,
    write_social_post_drafts,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "dashboard" / "data" / "social_post_drafts.json"


def load_data() -> list[dict]:
    return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))


def test_social_post_drafts_json_exists() -> None:
    assert OUTPUT_PATH.exists()
    assert isinstance(load_data(), list)
    assert load_data()


def test_social_post_ids_are_stable() -> None:
    first = build_social_post_drafts()
    second = build_social_post_drafts()
    assert [item["post_id"] for item in first] == [item["post_id"] for item in second]
    for item in first:
        assert item["post_id"] == post_id(item["channel"], item["source_draft_id"])


def test_social_channels_and_review_statuses() -> None:
    data = load_data()
    assert {item["channel"] for item in data} == set(CHANNELS)
    for item in data:
        assert item["review_status"] == REVIEW_STATUS
        assert item["public_use_status"] == PUBLIC_USE_STATUS
        assert item["recommended_next_step"] == RECOMMENDED_NEXT_STEP


def test_social_drafts_avoid_sensitive_fields_and_banned_terms() -> None:
    serialized = json.dumps(load_data(), ensure_ascii=False)
    assert "民調" not in serialized
    assert "支持度調查" not in serialized
    for item in load_data():
        assert not ({key.lower() for key in item} & SENSITIVE_FIELDS)


def test_write_social_post_drafts_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "social_post_drafts.json"
    data = write_social_post_drafts(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == data


def test_social_post_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for social post builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_social_post_drafts()
