from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from typing import Any

from src.classifiers.issue_classifier import ISSUE_DISPLAY_NAMES, TAXONOMY_CODES, classify_record


WINDOW_DAYS = (7, 30, 90)
VALID_TRENDS = {"up", "down", "stable", "spike"}
PROTOTYPE_REVIEW_STATUS = "prototype"

HOTSPOT_CATEGORY_MAP = {
    "停車": "traffic",
    "交通": "traffic",
    "人行": "pedestrian",
    "垃圾": "environment",
    "環境": "environment",
    "排水": "drainage",
    "淹水": "drainage",
    "安全": "safety",
    "市場": "market",
    "商圈": "market",
    "動線": "market",
    "公園": "park",
    "通學": "school",
    "學校": "school",
    "高齡": "senior",
    "社福": "senior",
    "文化": "culture",
    "觀光": "culture",
    "行政": "administration",
}


def parse_event_date(value: object) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None

    normalized = text.replace("/", "-")
    try:
        return date.fromisoformat(normalized[:10])
    except ValueError:
        return None


def parse_reference_datetime(value: object) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None

    normalized = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def infer_hotspot_issues(hotspots: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for hotspot in hotspots:
        text = " ".join(
            str(hotspot.get(field, ""))
            for field in ("name", "category", "department", "action")
        )
        for keyword, issue in HOTSPOT_CATEGORY_MAP.items():
            if keyword in text and issue in TAXONOMY_CODES:
                counts[issue] += 1
    return counts


def classify_raw_metadata(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [classify_record(record) for record in records]


def _issue_counts(classified_records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in classified_records:
        issue = str(record.get("primary_issue") or "other")
        counts[issue if issue in TAXONOMY_CODES else "other"] += 1
    return counts


def _average_confidence(classified_records: list[dict[str, Any]]) -> dict[str, float]:
    values: dict[str, list[float]] = defaultdict(list)
    for record in classified_records:
        issue = str(record.get("primary_issue") or "other")
        issue = issue if issue in TAXONOMY_CODES else "other"
        confidence = record.get("confidence", 0.4)
        if isinstance(confidence, (int, float)) and not isinstance(confidence, bool):
            values[issue].append(float(confidence))

    return {
        issue: round(sum(items) / len(items), 2)
        for issue, items in values.items()
        if items
    }


def _most_common_district(hotspots: list[dict[str, Any]]) -> str:
    districts = [
        str(hotspot.get("district", "")).strip()
        for hotspot in hotspots
        if str(hotspot.get("district", "")).strip()
    ]
    if not districts:
        return "待確認"
    return Counter(districts).most_common(1)[0][0]


def _recommended_action(issue: str) -> str:
    display_name = ISSUE_DISPLAY_NAMES.get(issue, ISSUE_DISPLAY_NAMES["other"])
    if issue == "other":
        return "補充逐字稿、會議日期與更完整分類後，再重新計算趨勢。"
    return f"先以「{display_name}」作為觀察題組，補足會議日期與更多樣本後再評估趨勢。"


def _change_percent(current_count: int, previous_count: int) -> int:
    if previous_count == 0:
        return 100 if current_count > 0 else 0
    return round(((current_count - previous_count) / previous_count) * 100)


def _trend(current_count: int, previous_count: int, change_percent: int) -> str:
    if previous_count > 0 and current_count >= previous_count * 3 and current_count >= 3:
        return "spike"
    if change_percent >= 15:
        return "up"
    if change_percent <= -15:
        return "down"
    return "stable"


def _dated_records(
    classified_records: list[dict[str, Any]],
    raw_records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    raw_by_url = {
        str(record.get("video_url", "")): record
        for record in raw_records
        if str(record.get("video_url", ""))
    }
    dated = []
    for record in classified_records:
        raw = raw_by_url.get(str(record.get("video_url", "")), {})
        event_date = parse_event_date(raw.get("meeting_date"))
        if event_date is None:
            continue
        dated.append({**record, "event_date": event_date})
    return dated


def _reference_date(raw_records: list[dict[str, Any]], dated_records: list[dict[str, Any]]) -> date:
    if dated_records:
        return max(record["event_date"] for record in dated_records)

    crawled_at_values = [
        parsed
        for record in raw_records
        if (parsed := parse_reference_datetime(record.get("crawled_at"))) is not None
    ]
    if crawled_at_values:
        return max(crawled_at_values).date()
    return datetime.now(timezone.utc).date()


def _prototype_summary(issue: str, window_days: int) -> str:
    display_name = ISSUE_DISPLAY_NAMES.get(issue, ISSUE_DISPLAY_NAMES["other"])
    return (
        f"{window_days} 天趨勢目前仍是 metadata / sample 階段；"
        f"「{display_name}」僅反映現有分類樣本與 hotspot 線索，"
        "尚未具備足夠會議日期或長期序列，不作正式升降判斷。"
    )


def _dated_summary(issue: str, window_days: int, trend: str) -> str:
    display_name = ISSUE_DISPLAY_NAMES.get(issue, ISSUE_DISPLAY_NAMES["other"])
    return (
        f"依已具備會議日期的 metadata 初步計算，"
        f"「{display_name}」在 {window_days} 天視窗呈現 {trend}；"
        "此結果仍需人工 review 與更多資料交叉確認。"
    )


def _build_prototype_trends(
    issue_counts: Counter[str],
    hotspot_counts: Counter[str],
    average_confidence: dict[str, float],
    district: str,
) -> list[dict[str, Any]]:
    issues = sorted((set(issue_counts) | set(hotspot_counts)) or {"other"})
    trends = []
    for window_days in WINDOW_DAYS:
        for issue in issues:
            evidence_count = int(issue_counts.get(issue, 0) + hotspot_counts.get(issue, 0))
            confidence = min(round(average_confidence.get(issue, 0.45), 2), 0.55)
            trends.append(
                {
                    "issue": issue,
                    "display_name": ISSUE_DISPLAY_NAMES.get(issue, ISSUE_DISPLAY_NAMES["other"]),
                    "current_count": evidence_count,
                    "previous_count": 0,
                    "change_percent": 0,
                    "trend": "stable",
                    "window_days": window_days,
                    "confidence": confidence,
                    "summary": _prototype_summary(issue, window_days),
                    "review_status": PROTOTYPE_REVIEW_STATUS,
                    "district": district,
                    "recommended_action": _recommended_action(issue),
                }
            )
    return trends


def _build_dated_trends(
    dated_records: list[dict[str, Any]],
    raw_records: list[dict[str, Any]],
    average_confidence: dict[str, float],
    district: str,
) -> list[dict[str, Any]]:
    reference_date = _reference_date(raw_records, dated_records)
    issues = sorted({str(record.get("primary_issue") or "other") for record in dated_records})
    trends = []
    for window_days in WINDOW_DAYS:
        current_start = reference_date - timedelta(days=window_days - 1)
        previous_start = current_start - timedelta(days=window_days)
        previous_end = current_start - timedelta(days=1)

        for issue in issues:
            current_count = sum(
                1
                for record in dated_records
                if record.get("primary_issue") == issue and current_start <= record["event_date"] <= reference_date
            )
            previous_count = sum(
                1
                for record in dated_records
                if record.get("primary_issue") == issue
                and previous_start <= record["event_date"] <= previous_end
            )
            change = _change_percent(current_count, previous_count)
            trend = _trend(current_count, previous_count, change)
            confidence = round(min(max(average_confidence.get(issue, 0.55), 0.55), 0.85), 2)
            review_status = "uncertain" if current_count + previous_count < 5 else "unreviewed"
            trends.append(
                {
                    "issue": issue,
                    "display_name": ISSUE_DISPLAY_NAMES.get(issue, ISSUE_DISPLAY_NAMES["other"]),
                    "current_count": current_count,
                    "previous_count": previous_count,
                    "change_percent": change,
                    "trend": trend,
                    "window_days": window_days,
                    "confidence": confidence,
                    "summary": _dated_summary(issue, window_days, trend),
                    "review_status": review_status,
                    "district": district,
                    "recommended_action": _recommended_action(issue),
                }
            )
    return trends


def analyze_issue_trends(
    classified_records: list[dict[str, Any]],
    raw_records: list[dict[str, Any]] | None = None,
    hotspots: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    raw_records = raw_records or []
    hotspots = hotspots or []

    normalized_records = list(classified_records)
    if not normalized_records and raw_records:
        normalized_records = classify_raw_metadata(raw_records)

    issue_counts = _issue_counts(normalized_records)
    average_confidence = _average_confidence(normalized_records)
    hotspot_counts = infer_hotspot_issues(hotspots)
    district = _most_common_district(hotspots)
    dated_records = _dated_records(normalized_records, raw_records)

    if len(dated_records) < 2:
        return _build_prototype_trends(issue_counts, hotspot_counts, average_confidence, district)

    return _build_dated_trends(dated_records, raw_records, average_confidence, district)
