from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard" / "data" / "open_data_readiness_report.json"
OUTPUT = ROOT / "dashboard" / "data" / "open_data_top10_review_tasks.json"
TOPIC_PRIORITY = {
    "traffic_parking": 0,
    "social_welfare": 1,
    "public_works_environment": 2,
    "culture_events": 3,
    "complaints_service": 4,
}


def load_candidates() -> list[dict]:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    items = data.get("items") or data.get("top_candidates", []) + data.get("blocked_or_high_risk", [])
    candidates = [item for item in items if item.get("readiness_level") != "blocked"]
    return sorted(
        candidates,
        key=lambda item: (
            -int(item.get("readiness_score", 0)),
            TOPIC_PRIORITY.get(item.get("topic_group"), 99),
            item.get("title", ""),
        ),
    )[:10]


def priority_for(index: int, score: int) -> str:
    if index <= 3 or score >= 25:
        return "P1"
    if index <= 7 or score >= 20:
        return "P2"
    return "P3"


def task_for(item: dict, index: int) -> dict:
    topic = item.get("topic_group", "")
    is_complaint = topic == "complaints_service"
    review_steps = [
        "開啟 source_url",
        "確認是否為官方來源",
        "確認資料格式是否可下載或可讀",
        "確認授權或開放資料條款",
        "記錄更新頻率",
        "判斷是否適合後續建立 crawler spec",
    ]
    safety_checklist = [
        "不啟動 live crawler",
        "不抓個資",
        "不抓私人陳情全文",
        "不自動發布",
        "不產生競選文案",
    ]
    if is_complaint:
        review_steps.append("確認不含私人陳情全文與個資")
        safety_checklist.append("complaints_service 必須額外確認只可使用公開統計或入口說明")
    acceptance_criteria = [
        "source_url 可開啟",
        "official source verified",
        "license reviewed",
        "expected format checked",
        "no personal data",
        "no private complaint full text",
        "no auto publish",
        "reviewer notes completed",
    ]
    score = int(item.get("readiness_score", 0))
    return {
        "task_id": f"top10_{index:02d}_{item.get('inventory_id')}",
        "inventory_id": item.get("inventory_id"),
        "title": item.get("title"),
        "topic_group": topic,
        "source_owner": item.get("source_owner"),
        "source_url": item.get("source_url"),
        "expected_format": item.get("expected_format"),
        "license_status": item.get("license_status"),
        "update_cadence": item.get("update_cadence"),
        "readiness_score": score,
        "readiness_level": item.get("readiness_level"),
        "crawler_stage": item.get("crawler_stage"),
        "review_priority": priority_for(index, score),
        "estimated_review_minutes": 20 if not is_complaint else 30,
        "review_steps": review_steps,
        "acceptance_criteria": acceptance_criteria,
        "safety_checklist": safety_checklist,
        "review_status": "not_started",
        "assigned_to": "",
        "reviewed_at": "",
        "reviewer_notes": "",
        "next_action": "verify_source_url",
        "no_live_crawler": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }


def build_open_data_top10_review_tasks() -> dict:
    tasks = [task_for(item, index) for index, item in enumerate(load_candidates(), start=1)]
    if len(tasks) != 10:
        raise ValueError(f"Expected 10 tasks, got {len(tasks)}")
    topic_counts = Counter(task["topic_group"] for task in tasks)
    priority_counts = Counter(task["review_priority"] for task in tasks)
    level_counts = Counter(task["readiness_level"] for task in tasks)
    payload = {
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "public_use_status": "internal_top10_review_tasks",
        "source_report_count": 29,
        "total_count": 10,
        "topic_groups": dict(topic_counts),
        "review_priorities": dict(priority_counts),
        "readiness_levels": dict(level_counts),
        "tasks": tasks,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    build_open_data_top10_review_tasks()
