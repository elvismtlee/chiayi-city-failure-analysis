from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.build_issue_trends import build_issue_trends
from src.analyzers.issue_trend_analyzer import VALID_TRENDS


def write_json(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def write_raw_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["video_url", "meeting_date", "crawled_at"])
        writer.writeheader()
        writer.writerows(rows)


def test_build_issue_trends_writes_dashboard_json(tmp_path: Path) -> None:
    classified = tmp_path / "issue_classified_sample.json"
    raw = tmp_path / "cycc_question_video_metadata.csv"
    hotspots = tmp_path / "hotspots.json"
    output = tmp_path / "issue_trends.json"

    write_json(
        classified,
        [
            {
                "video_url": "https://example.test/a",
                "primary_issue": "other",
                "confidence": 0.4,
            }
        ],
    )
    write_raw_csv(
        raw,
        [
            {
                "video_url": "https://example.test/a",
                "meeting_date": "",
                "crawled_at": "2026-05-21T00:00:00+00:00",
            }
        ],
    )
    write_json(hotspots, [{"name": "文化路商圈", "category": "停車 / 人行", "district": "西區 / 東區交界"}])

    trends = build_issue_trends(
        classified_source=classified,
        raw_source=raw,
        hotspots_source=hotspots,
        output=output,
    )

    assert output.exists()
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written == trends
    assert {item["window_days"] for item in written} == {7, 30, 90}
    assert all(item["trend"] in VALID_TRENDS for item in written)
    assert all(item["review_status"] == "prototype" for item in written)


def test_build_issue_trends_falls_back_to_raw_metadata_when_classified_sample_missing(tmp_path: Path) -> None:
    classified = tmp_path / "missing_issue_classified_sample.json"
    raw = tmp_path / "cycc_question_video_metadata.csv"
    hotspots = tmp_path / "hotspots.json"
    output = tmp_path / "issue_trends.json"

    write_raw_csv(
        raw,
        [
            {
                "video_url": "https://example.test/a",
                "meeting_date": "",
                "crawled_at": "2026-05-21T00:00:00+00:00",
            }
        ],
    )
    write_json(hotspots, [])

    trends = build_issue_trends(
        classified_source=classified,
        raw_source=raw,
        hotspots_source=hotspots,
        output=output,
    )

    assert output.exists()
    assert trends
    assert {item["window_days"] for item in trends} == {7, 30, 90}
