from __future__ import annotations

from src.analyzers.issue_trend_analyzer import (
    VALID_TRENDS,
    analyze_issue_trends,
    infer_hotspot_issues,
    parse_event_date,
)
from src.classifiers.issue_classifier import TAXONOMY_CODES


REQUIRED_FIELDS = {
    "issue",
    "current_count",
    "previous_count",
    "change_percent",
    "trend",
    "window_days",
    "confidence",
    "summary",
    "review_status",
}


def test_parse_event_date_accepts_iso_and_slash_dates() -> None:
    assert parse_event_date("2026-05-21").isoformat() == "2026-05-21"
    assert parse_event_date("2026/05/21").isoformat() == "2026-05-21"
    assert parse_event_date("") is None


def test_infer_hotspot_issues_from_dashboard_hotspots() -> None:
    counts = infer_hotspot_issues(
        [
            {"name": "文化路商圈", "category": "停車 / 人行", "action": "商圈動線"},
            {"name": "學校周邊", "category": "通學安全"},
        ]
    )

    assert counts["traffic"] >= 1
    assert counts["pedestrian"] >= 1
    assert counts["market"] >= 1
    assert counts["school"] >= 1


def test_analyze_issue_trends_returns_prototype_when_dates_are_missing() -> None:
    trends = analyze_issue_trends(
        classified_records=[
            {
                "video_url": "https://example.test/a",
                "primary_issue": "other",
                "confidence": 0.4,
            }
        ],
        raw_records=[{"video_url": "https://example.test/a", "meeting_date": "", "crawled_at": "2026-05-21T00:00:00+00:00"}],
        hotspots=[{"name": "市場周邊", "category": "垃圾 / 動線", "district": "西區"}],
    )

    assert trends
    assert {item["window_days"] for item in trends} == {7, 30, 90}
    for item in trends:
        assert REQUIRED_FIELDS <= item.keys()
        assert item["issue"] in TAXONOMY_CODES
        assert item["trend"] == "stable"
        assert item["trend"] in VALID_TRENDS
        assert item["change_percent"] == 0
        assert item["confidence"] <= 0.55
        assert item["review_status"] == "prototype"
        assert "metadata / sample" in item["summary"]


def test_analyze_issue_trends_calculates_dated_windows() -> None:
    classified = [
        {"video_url": "https://example.test/current-1", "primary_issue": "traffic", "confidence": 0.8},
        {"video_url": "https://example.test/current-2", "primary_issue": "traffic", "confidence": 0.8},
        {"video_url": "https://example.test/current-3", "primary_issue": "traffic", "confidence": 0.8},
        {"video_url": "https://example.test/previous-1", "primary_issue": "traffic", "confidence": 0.8},
    ]
    raw = [
        {"video_url": "https://example.test/current-1", "meeting_date": "2026-05-21"},
        {"video_url": "https://example.test/current-2", "meeting_date": "2026-05-20"},
        {"video_url": "https://example.test/current-3", "meeting_date": "2026-05-19"},
        {"video_url": "https://example.test/previous-1", "meeting_date": "2026-05-12"},
    ]

    trends = analyze_issue_trends(classified_records=classified, raw_records=raw)
    seven_day_traffic = next(
        item for item in trends if item["issue"] == "traffic" and item["window_days"] == 7
    )

    assert seven_day_traffic["current_count"] == 3
    assert seven_day_traffic["previous_count"] == 1
    assert seven_day_traffic["change_percent"] == 200
    assert seven_day_traffic["trend"] == "spike"
    assert seven_day_traffic["review_status"] == "uncertain"
