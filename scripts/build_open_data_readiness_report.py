from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "dashboard" / "data" / "open_data_url_review_queue.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_readiness_report.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
REQUIRED_GROUPS = {
    "traffic_parking",
    "social_welfare",
    "culture_events",
    "public_works_environment",
    "complaints_service",
}
HIGH_OFFICIAL_DOMAINS = {"chiayi.gov.tw", "data.gov.tw"}
GOOD_FORMAT_KEYWORDS = ("csv", "json", "api", "xml")
CLEAR_LICENSE_KEYWORDS = ("ogdl", "official_open_data_terms", "cc-by", "open_data")


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_review_queue(path: Path = QUEUE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _score_official_source(item: dict) -> int:
    domain = str(item.get("official_domain", "")).lower()
    if domain in HIGH_OFFICIAL_DOMAINS:
        return 5
    if domain.endswith(".chiayi.gov.tw") or domain.endswith(".gov.tw"):
        return 4
    if domain.endswith("youbike.com.tw"):
        return 3
    return 2


def _score_data_format(item: dict) -> int:
    expected_format = str(item.get("expected_format", "")).lower()
    if any(keyword in expected_format for keyword in GOOD_FORMAT_KEYWORDS):
        return 5
    if "metadata" in expected_format or "preview" in expected_format:
        return 4
    if "html" in expected_format:
        return 2
    return 1


def _score_license(item: dict) -> int:
    license_status = str(item.get("license_status", "")).lower()
    if any(keyword in license_status for keyword in CLEAR_LICENSE_KEYWORDS):
        return 5
    if "review_needed" in license_status:
        return 2
    if license_status:
        return 3
    return 1


def _score_update_cadence(item: dict) -> int:
    cadence = str(item.get("update_cadence", "")).lower()
    if any(keyword in cadence for keyword in ("hour", "daily", "每日", "每小時", "weekly", "每週")):
        return 5
    if any(keyword in cadence for keyword in ("monthly", "每月")):
        return 4
    if any(keyword in cadence for keyword in ("quarter", "每季")):
        return 3
    if any(keyword in cadence for keyword in ("year", "每年")):
        return 2
    if cadence:
        return 1
    return 0


def _score_relevance(item: dict) -> int:
    relevance = str(item.get("west_district_relevance", "")).lower()
    if relevance == "high":
        return 5
    if relevance == "medium":
        return 3
    if relevance == "low":
        return 1
    return 0


def _score_dashboard_value(item: dict) -> int:
    dashboard_use = str(item.get("dashboard_use", "")).strip()
    if not dashboard_use:
        return 0
    if len(dashboard_use) >= 8:
        return 5
    return 3


def _score_risk(item: dict) -> int:
    topic_group = str(item.get("topic_group", ""))
    expected_format = str(item.get("expected_format", "")).lower()
    source_type = str(item.get("source_type", "")).lower()
    if str(item.get("url_review_status")) == "do_not_crawl":
        return 5
    if topic_group == "complaints_service":
        return 5
    if "login" in expected_format or "blocked" in expected_format:
        return 4
    if "html" in expected_format and "service" in source_type:
        return 3
    if "html" in expected_format:
        return 2
    return 1


def build_score_breakdown(item: dict) -> dict:
    return {
        "official_source_score": _score_official_source(item),
        "data_format_score": _score_data_format(item),
        "license_clarity_score": _score_license(item),
        "update_cadence_score": _score_update_cadence(item),
        "west_district_relevance_score": _score_relevance(item),
        "dashboard_value_score": _score_dashboard_value(item),
        "crawler_risk_score": _score_risk(item),
    }


def compute_readiness_score(score_breakdown: dict) -> int:
    raw_score = (
        score_breakdown["official_source_score"]
        + score_breakdown["data_format_score"]
        + score_breakdown["license_clarity_score"]
        + score_breakdown["update_cadence_score"]
        + score_breakdown["west_district_relevance_score"]
        + score_breakdown["dashboard_value_score"]
        - score_breakdown["crawler_risk_score"]
    )
    return max(0, min(30, raw_score))


def get_readiness_level(item: dict, readiness_score: int) -> str:
    if str(item.get("url_review_status")) == "do_not_crawl" or readiness_score == 0:
        return "blocked"
    if readiness_score >= 22:
        return "high"
    if readiness_score >= 14:
        return "medium"
    return "low"


def get_crawler_stage(item: dict, readiness_level: str, score_breakdown: dict) -> str:
    if str(item.get("url_review_status")) == "do_not_crawl" or readiness_level == "blocked":
        return "not_recommended"
    if item.get("topic_group") == "complaints_service":
        return "manual_review_only"
    if bool(item.get("official_source_verified")) is False:
        return "candidate_after_source_verification"
    if bool(item.get("license_reviewed")) is False:
        return "candidate_after_license_review"
    if score_breakdown["data_format_score"] < 4:
        return "candidate_after_format_check"
    return "manual_review_only"


def build_readiness_notes(item: dict, readiness_level: str, crawler_stage: str, score_breakdown: dict) -> str:
    notes = []
    if readiness_level == "high":
        notes.append("官方來源與資料格式條件較完整，可優先安排人工審核。")
    elif readiness_level == "medium":
        notes.append("具備初步 dashboard 價值，但仍需補來源或授權審核。")
    elif readiness_level == "low":
        notes.append("仍需補更多來源驗證或格式確認，再考慮進下一階段。")
    else:
        notes.append("目前不建議進入 crawler 規劃。")

    if crawler_stage == "candidate_after_source_verification":
        notes.append("先確認官方來源可穩定存取。")
    elif crawler_stage == "candidate_after_license_review":
        notes.append("先完成授權條款人工審核。")
    elif crawler_stage == "candidate_after_format_check":
        notes.append("先確認公開格式是否適合穩定擷取。")
    elif crawler_stage == "manual_review_only":
        notes.append("目前只可做人工審核排序，不啟動 live crawler。")
    elif crawler_stage == "not_recommended":
        notes.append("暫不建議納入 crawler 候選。")

    if score_breakdown["crawler_risk_score"] >= 5:
        notes.append("風險較高，必須特別避免個資與私人陳情內容。")
    return " ".join(notes)


def build_item(item: dict) -> dict:
    score_breakdown = build_score_breakdown(item)
    readiness_score = compute_readiness_score(score_breakdown)
    readiness_level = get_readiness_level(item, readiness_score)
    crawler_stage = get_crawler_stage(item, readiness_level, score_breakdown)
    return {
        "inventory_id": item["inventory_id"],
        "title": item["title"],
        "topic_group": item["topic_group"],
        "source_owner": item["source_owner"],
        "source_url": item["source_url"],
        "expected_format": item["expected_format"],
        "license_status": item["license_status"],
        "update_cadence": item["update_cadence"],
        "dashboard_use": item["dashboard_use"],
        "url_review_status": item["url_review_status"],
        "crawler_candidate": item["crawler_candidate"],
        "crawler_priority": item["crawler_priority"],
        "readiness_score": readiness_score,
        "readiness_level": readiness_level,
        "crawler_stage": crawler_stage,
        "score_breakdown": score_breakdown,
        "readiness_notes": build_readiness_notes(item, readiness_level, crawler_stage, score_breakdown),
        "safety_notes": item.get("safety_notes", "no personal data / no auto publish / no live crawler"),
    }


def validate_queue(queue: dict) -> list[dict]:
    items = queue.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Review queue items must be a list")
    if len(items) < 20:
        raise ValueError("Review queue must contain at least 20 items")
    if len(items) != 29:
        raise ValueError("Review queue should currently contain 29 items")
    if int(queue.get("total_count", 0)) != len(items):
        raise ValueError("Queue total_count does not match items length")
    topic_groups = {item.get("topic_group") for item in items}
    missing_groups = REQUIRED_GROUPS - topic_groups
    if missing_groups:
        raise ValueError(f"Missing required topic groups: {', '.join(sorted(missing_groups))}")
    return items


def build_open_data_readiness_report(
    queue_path: Path = QUEUE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    queue = load_review_queue(queue_path)
    queue_items = validate_queue(queue)
    items = [build_item(item) for item in queue_items]
    topic_groups = Counter(item["topic_group"] for item in items)
    readiness_levels = Counter(item["readiness_level"] for item in items)
    sorted_items = sorted(
        items,
        key=lambda item: (item["readiness_score"], item["topic_group"], item["title"]),
        reverse=True,
    )
    payload = {
        "generated_at": now_iso(),
        "public_use_status": "internal_readiness_report",
        "source_queue_count": len(queue_items),
        "total_count": len(items),
        "topic_groups": {group: topic_groups.get(group, 0) for group in sorted(REQUIRED_GROUPS)},
        "readiness_levels": {
            "high": readiness_levels.get("high", 0),
            "medium": readiness_levels.get("medium", 0),
            "low": readiness_levels.get("low", 0),
            "blocked": readiness_levels.get("blocked", 0),
        },
        "top_candidates": sorted_items[:5],
        "blocked_or_high_risk": [
            item for item in items
            if item["readiness_level"] == "blocked"
            or item["score_breakdown"]["crawler_risk_score"] >= 5
        ],
        "items": items,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> dict:
    return build_open_data_readiness_report()


if __name__ == "__main__":
    main()
