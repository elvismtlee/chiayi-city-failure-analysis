import json
from pathlib import Path

from scripts.build_geocoding_review_queue import (
    build_queue,
    build_suggested_query,
    normalize_place_name,
    score_priority,
    write_queue,
)


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "dashboard" / "data" / "geocoding_review_queue.json"

REQUIRED_FIELDS = [
    "candidate_id",
    "place_name",
    "district",
    "category",
    "department",
    "score",
    "current_lng",
    "current_lat",
    "geo_precision",
    "review_status",
    "suggested_query",
    "suggested_review_method",
    "priority",
    "source",
    "notes",
]

SENSITIVE_FIELDS = {
    "phone",
    "email",
    "address",
    "full_address",
    "national_id",
}


def load_queue() -> list[dict]:
    return json.loads(QUEUE.read_text(encoding="utf-8"))


def test_generated_geocoding_review_queue_exists_and_parses() -> None:
    assert QUEUE.exists()
    data = load_queue()
    assert isinstance(data, list)
    assert data


def test_write_queue_can_generate_json(tmp_path: Path) -> None:
    output_path = tmp_path / "geocoding_review_queue.json"
    queue = write_queue(output_path)

    assert output_path.exists()
    generated = json.loads(output_path.read_text(encoding="utf-8"))
    assert generated == queue
    assert isinstance(generated, list)
    assert generated


def test_build_queue_returns_review_candidates() -> None:
    queue = build_queue()
    assert queue
    assert all(item["geo_precision"] in {"prototype", "unknown", "uncertain"} or item["review_status"] in {"prototype", "uncertain", "unreviewed"} for item in queue)


def test_queue_items_have_required_fields() -> None:
    for item in load_queue():
        for field in REQUIRED_FIELDS:
            assert field in item, f"missing field: {field}"


def test_priority_is_based_on_score() -> None:
    assert score_priority(90) == "high"
    assert score_priority(85) == "high"
    assert score_priority(84.9) == "medium"
    assert score_priority(70) == "medium"
    assert score_priority(69.9) == "low"


def test_suggested_query_mentions_chiayi_city() -> None:
    for item in load_queue():
        assert "嘉義市" in item["suggested_query"]
        assert item["place_name"] in item["suggested_query"]


def test_queue_uses_manual_review_method() -> None:
    for item in load_queue():
        assert item["suggested_review_method"] == "manual_review_with_public_map"
        assert "人工確認" in item["notes"]


def test_queue_does_not_contain_sensitive_fields() -> None:
    for item in load_queue():
        lowered_keys = {str(key).lower() for key in item.keys()}
        assert not lowered_keys & SENSITIVE_FIELDS


def test_queue_does_not_mark_prototype_as_verified() -> None:
    for item in load_queue():
        if item["geo_precision"] == "prototype":
            assert item["review_status"] != "verified"


def test_queue_uses_local_approved_terms() -> None:
    content = QUEUE.read_text(encoding="utf-8")
    assert "文化路商圈" in content
    assert "文化路夜市" not in content


def test_normalize_place_name_replaces_banned_local_term() -> None:
    assert normalize_place_name("文化路夜市") == "文化路商圈"
    assert "文化路夜市" not in build_suggested_query("西區", "文化路夜市")
    assert "文化路商圈" in build_suggested_query("西區", "文化路夜市")
