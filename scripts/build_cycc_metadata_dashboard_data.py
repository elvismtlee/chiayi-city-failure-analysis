from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dashboard" / "data"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check(path: Path, source_type: str, expected_count: int) -> None:
    payload = read(path)
    items = payload.get("items", [])
    assert payload.get("source_type") == source_type
    assert payload.get("total_count") == expected_count
    assert len(items) == expected_count
    assert payload.get("manual_review_required") is True
    assert payload.get("no_auto_publish") is True
    assert payload.get("metadata_only") is True
    for item in items:
        assert item.get("source_type") == source_type
        assert item.get("title")
        assert item.get("source_url")
        assert item.get("detail_url")
        assert item.get("review_status") == "needs_review"


def main() -> None:
    check(DATA / "cycc_minutes_metadata.json", "minutes", 10)
    check(DATA / "cycc_question_video_metadata.json", "question_videos", 131)
    print("CYCC metadata OK: total=141")


if __name__ == "__main__":
    main()
