from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
READINESS_REPORT_PATH = ROOT / "dashboard" / "data" / "open_data_readiness_report.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_top10_review_tasks.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
TOPIC_PRIORITY = {
    "traffic_parking": 0,
    "social_welfare": 1,
    "public_works_environment": 2,
    "culture_events": 3,
    "complaints_service": 4,
}
BASE_REVIEW_STEPS = [
    "開啟 source_url",
    "確認是否為官方來源",
    "確認資料格式是否可下載或可讀",
    "確認授權或開放資料條款",
    "記錄更新頻率",
    "判斷是否適合後續建立 crawler spec",
]
BASE_ACCEPTANCE = [
    "source_url 可開啟",
    "official source verified",
    "license reviewed",
    "expected format checked",
    "no personal data",
    "no private complaint full text",
    "no auto publish",
    "reviewer notes completed",
]
BASE_SAFETY = [
    "不啟動 live crawler",
    "不抓個資",
    "不抓私人陳情全文",
    "不自動發布",
    "crawler_candidate 或 readiness_score 不代表批准爬取",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_readiness_report(path: Path = READINESS_REPORT_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_report(report: dict) -> list[dict]:
    items = report.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Readiness report items must be a list")
    if int(report.get("total_count", 0)) != len(items):
        raise ValueError("Readiness report total_count does not match items length")
    if len(items) != 29:
        raise ValueError("Readiness report should currently contain 29 items")
    return items


def selection_key(item: dict) -> tuple[int, int, int, str]:
    readiness_rank = 0 if item.get("readiness_level") == "high" else 1
    score_rank = -int(item.get("readiness_score", 0))
    topic_rank = TOPIC_PRIORITY.get(str(item.get("topic_group", "")), 99)
    title = str(item.get("title", ""))
    return (readiness_rank, score_rank, topic_rank, title)


def estimated_review_minutes(item: dict) -> int:
    score = int(item.get("readiness_score", 0))
    topic_group = str(item.get("topic_group", ""))
    base = 20 if score >= 24 else 25 if score >= 20 else 30
    if topic_group == "complaints_service":
        return base + 15
    if "html" in str(item.get("expected_format", "")).lower():
        return base + 10
    return base


def review_priority(index: int, item: dict) -> str:
    if str(item.get("topic_group")) == "complaints_service":
        return "P3"
    if index < 4:
        return "P1"
    if index < 7:
        return "P2"
    return "P3"


def next_action(item: dict) -> str:
    topic_group = str(item.get("topic_group", ""))
    license_status = str(item.get("license_status", "")).lower()
    expected_format = str(item.get("expected_format", "")).lower()
    if topic_group == "complaints_service":
        return "mark_not_suitable"
    if "review_needed" in license_status:
        return "check_license"
    if any(token in expected_format for token in ("csv", "json", "api", "xml")):
        return "prepare_crawler_spec_later"
    if "html" in expected_format:
        return "inspect_download_format"
    return "verify_source_url"


def build_review_steps(item: dict) -> list[str]:
    steps = list(BASE_REVIEW_STEPS)
    if str(item.get("topic_group")) == "complaints_service":
        steps.append("若涉及 complaints_service，確認不含私人陳情全文與個資")
    return steps


def build_acceptance_criteria(item: dict) -> list[str]:
    criteria = list(BASE_ACCEPTANCE)
    if str(item.get("topic_group")) == "complaints_service":
        criteria.append("complaints_service 僅保留公開入口或統計資訊")
    return criteria


def build_safety_checklist(item: dict) -> list[str]:
    checklist = list(BASE_SAFETY)
    if str(item.get("topic_group")) == "complaints_service":
        checklist.extend(
            [
                "只檢查公開入口或統計頁，不碰私人陳情全文",
                "若頁面要求登入、驗證或填表，直接停止並標記 blocked",
            ]
        )
    return checklist


def build_task(index: int, item: dict) -> dict:
    return {
        "task_id": f"open-data-top10-{index + 1:02d}",
        "inventory_id": item["inventory_id"],
        "title": item["title"],
        "topic_group": item["topic_group"],
        "source_owner": item["source_owner"],
        "source_url": item["source_url"],
        "expected_format": item["expected_format"],
        "license_status": item["license_status"],
        "update_cadence": item["update_cadence"],
        "readiness_score": item["readiness_score"],
        "readiness_level": item["readiness_level"],
        "crawler_stage": item["crawler_stage"],
        "review_priority": review_priority(index, item),
        "estimated_review_minutes": estimated_review_minutes(item),
        "review_steps": build_review_steps(item),
        "acceptance_criteria": build_acceptance_criteria(item),
        "safety_checklist": build_safety_checklist(item),
        "review_status": "not_started",
        "assigned_to": "",
        "reviewed_at": "",
        "reviewer_notes": "",
        "next_action": next_action(item),
        "no_live_crawler": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }


def build_open_data_top10_review_tasks(
    readiness_report_path: Path = READINESS_REPORT_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    report = load_readiness_report(readiness_report_path)
    items = validate_report(report)
    candidates = [
        item for item in items
        if item.get("readiness_level") != "blocked"
        and item.get("crawler_stage") != "live_crawler"
    ]
    selected = sorted(candidates, key=selection_key)[:10]
    if len(selected) != 10:
        raise ValueError("Top 10 review tasks builder must select exactly 10 items")

    tasks = [build_task(index, item) for index, item in enumerate(selected)]
    topic_groups = Counter(task["topic_group"] for task in tasks)
    readiness_levels = Counter(task["readiness_level"] for task in tasks)
    review_priorities = Counter(task["review_priority"] for task in tasks)

    payload = {
        "generated_at": now_iso(),
        "public_use_status": "internal_top10_review_tasks",
        "source_report_count": len(items),
        "total_count": len(tasks),
        "topic_groups": dict(sorted(topic_groups.items())),
        "readiness_levels": {
            "high": readiness_levels.get("high", 0),
            "medium": readiness_levels.get("medium", 0),
            "low": readiness_levels.get("low", 0),
            "blocked": readiness_levels.get("blocked", 0),
        },
        "review_priority_counts": {
            "P1": review_priorities.get("P1", 0),
            "P2": review_priorities.get("P2", 0),
            "P3": review_priorities.get("P3", 0),
        },
        "tasks": tasks,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> dict:
    return build_open_data_top10_review_tasks()


if __name__ == "__main__":
    main()
