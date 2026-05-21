import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.processors.build_dashboard_data import build_dashboard_data


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_build_dashboard_data_keeps_fallback_without_raw_csv(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "dashboard-data"

    build_dashboard_data(raw_dir=raw_dir, dashboard_data_dir=output_dir)

    summary = read_json(output_dir / "dashboard_summary.json")
    issue_ranking = read_json(output_dir / "issue_ranking.json")
    hotspots = read_json(output_dir / "hotspots.json")
    ai_summary = read_json(output_dir / "ai_issue_summary.json")

    assert summary["data_status"] == "fallback_mock"
    assert summary["total_questions"] == 386
    assert issue_ranking[0]["issue"] == "停車"
    assert hotspots[0]["name"] == "文化路商圈"
    assert hotspots[0]["district"] == "西區 / 東區交界"
    assert hotspots[0]["action"] == "商圈動線與停車熱點專案"
    assert "raw CSV" in ai_summary["summary"]


def test_fallback_output_uses_local_terminology(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "dashboard-data"

    build_dashboard_data(raw_dir=raw_dir, dashboard_data_dir=output_dir)

    hotspots = read_json(output_dir / "hotspots.json")
    combined_output = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(output_dir.glob("*.json"))
    )

    assert "文化路夜市" not in combined_output
    assert hotspots[0]["name"] == "文化路商圈"


def test_build_dashboard_data_uses_cycc_raw_metadata(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    output_dir = tmp_path / "dashboard-data"

    pd.DataFrame(
        [
            {
                "source_id": "CYCC_MINUTES",
                "title": "嘉義市公共工程品質督導專案小組第13次會議",
                "department": "議事組",
                "views": 81,
                "updated_at": "",
                "detail_url": "https://example.com/minutes/1",
                "file_url": "https://example.com/minutes/1.pdf",
                "crawled_at": "2026-05-21T00:00:00+00:00",
                "raw_hash": "a",
            },
            {
                "source_id": "CYCC_MINUTES",
                "title": "嘉義市議會為了解市府處分市有土地及管理情形專案小組第5次會議",
                "department": "議事組",
                "views": 63,
                "updated_at": "",
                "detail_url": "https://example.com/minutes/2",
                "file_url": "https://example.com/minutes/2.pdf",
                "crawled_at": "2026-05-21T00:00:00+00:00",
                "raw_hash": "b",
            },
        ]
    ).to_csv(raw_dir / "cycc_minutes_metadata.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(
        [
            {
                "source_id": "CYCC_QUESTION_VIDEO",
                "councilor_name": "王議員",
                "council_term": "第十屆",
                "session_name": "第七次定期會",
                "video_title": "停車與交通動線質詢",
                "video_url": "https://www.youtube.com/embed/test1",
                "meeting_date": "",
                "topic_guess": "交通",
                "crawled_at": "2026-05-21T00:00:00+00:00",
                "raw_hash": "c",
            },
            {
                "source_id": "CYCC_QUESTION_VIDEO",
                "councilor_name": "李議員",
                "council_term": "第十屆",
                "session_name": "第七次定期會",
                "video_title": "市場周邊垃圾清潔質詢",
                "video_url": "https://www.youtube.com/embed/test2",
                "meeting_date": "",
                "topic_guess": "",
                "crawled_at": "2026-05-21T00:00:00+00:00",
                "raw_hash": "d",
            },
        ]
    ).to_csv(raw_dir / "cycc_question_video_metadata.csv", index=False, encoding="utf-8-sig")

    build_dashboard_data(raw_dir=raw_dir, dashboard_data_dir=output_dir)

    summary = read_json(output_dir / "dashboard_summary.json")
    issue_ranking = read_json(output_dir / "issue_ranking.json")
    hotspots = read_json(output_dir / "hotspots.json")
    ai_summary = read_json(output_dir / "ai_issue_summary.json")

    assert summary["data_status"] == "raw_csv"
    assert summary["minutes_metadata_count"] == 2
    assert summary["question_video_metadata_count"] == 2
    assert summary["total_questions"] == 2
    assert {item["issue"] for item in issue_ranking} >= {"道路", "土地管理", "交通", "環境"}
    assert hotspots[0]["district"] == "嘉義市"
    assert "2 筆會議紀錄 metadata" in ai_summary["summary"]


def test_dashboard_pages_reference_expected_scripts_and_json_paths() -> None:
    index_html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
    insights_html = (ROOT / "dashboard" / "insights.html").read_text(encoding="utf-8")
    app_js = (ROOT / "dashboard" / "app.js").read_text(encoding="utf-8")
    insights_js = (ROOT / "dashboard" / "insights.js").read_text(encoding="utf-8")

    assert '<script src="./app.js"></script>' in index_html
    assert '<script src="./insights.js"></script>' in insights_html
    assert "./data/dashboard_summary.json" in app_js
    assert "./data/issue_ranking.json" in app_js
    assert "./data/hotspots.json" in app_js
    assert "./data/ai_issue_summary.json" in insights_js
    assert "./data/issue_trends.json" in insights_js
    assert "./data/urban_failure_scores.json" in insights_js
    assert "./data/department_performance.json" in insights_js
    assert "./data/councilor_issue_analysis.json" in insights_js
