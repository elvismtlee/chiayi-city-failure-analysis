from __future__ import annotations

import json
import socket
from pathlib import Path

from scripts.build_short_video_script_drafts import (
    PUBLIC_USE_STATUS,
    RECOMMENDED_NEXT_STEP,
    REVIEW_STATUS,
    SENSITIVE_FIELDS,
    build_short_video_script_drafts,
    script_id,
    write_short_video_script_drafts,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "dashboard" / "data" / "short_video_script_drafts.json"


def load_data() -> list[dict]:
    return json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))


def test_short_video_script_drafts_json_exists() -> None:
    assert OUTPUT_PATH.exists()
    assert isinstance(load_data(), list)
    assert load_data()


def test_video_script_ids_are_stable() -> None:
    first = build_short_video_script_drafts()
    second = build_short_video_script_drafts()
    assert [item["script_id"] for item in first] == [item["script_id"] for item in second]
    for item in first:
        assert item["script_id"] == script_id(item["source_post_id"])


def test_video_scripts_have_required_review_fields() -> None:
    for item in load_data():
        assert isinstance(item["scene_plan"], list)
        assert isinstance(item["subtitle_lines"], list)
        assert item["review_status"] == REVIEW_STATUS
        assert item["public_use_status"] == PUBLIC_USE_STATUS
        assert item["recommended_next_step"] == RECOMMENDED_NEXT_STEP


def test_video_scripts_avoid_sensitive_fields_and_disallowed_requests() -> None:
    serialized = json.dumps(load_data(), ensure_ascii=False)
    for term in ["深偽", "冒充", "誤導剪輯"]:
        assert term not in serialized
    for item in load_data():
        assert not ({key.lower() for key in item} & SENSITIVE_FIELDS)


def test_write_short_video_script_drafts_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "short_video_script_drafts.json"
    data = write_short_video_script_drafts(output_path)
    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8")) == data


def test_short_video_builder_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for short video script builder")

    monkeypatch.setattr(socket, "socket", fail_socket)
    assert build_short_video_script_drafts()
