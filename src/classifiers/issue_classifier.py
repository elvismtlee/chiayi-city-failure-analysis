from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


TAXONOMY_CODES = {
    "traffic",
    "road",
    "pedestrian",
    "environment",
    "drainage",
    "safety",
    "market",
    "park",
    "school",
    "senior",
    "culture",
    "administration",
    "other",
}

ISSUE_DISPLAY_NAMES = {
    "traffic": "交通停車",
    "road": "道路路平",
    "pedestrian": "人行安全",
    "environment": "環境衛生",
    "drainage": "排水防汛",
    "safety": "公共安全",
    "market": "市場商圈",
    "park": "公園休憩",
    "school": "通學安全",
    "senior": "社福高齡",
    "culture": "文化觀光",
    "administration": "行政服務",
    "other": "其他議題",
}

TOPIC_GUESS_MAP = {
    "交通": "traffic",
    "停車": "traffic",
    "道路": "road",
    "人行": "pedestrian",
    "環境": "environment",
    "水利": "drainage",
    "排水": "drainage",
    "公共安全": "safety",
    "市場": "market",
    "商圈": "market",
    "公園": "park",
    "教育": "school",
    "學校": "school",
    "通學": "school",
    "社福": "senior",
    "高齡": "senior",
    "文化": "culture",
    "觀光": "culture",
    "行政": "administration",
}

ISSUE_RULES: dict[str, dict[str, list[str]]] = {
    "traffic": {
        "停車": ["parking"],
        "違停": ["illegal_parking", "parking"],
        "號誌": ["traffic_light"],
        "交通": ["congestion"],
        "車流": ["congestion"],
        "壅塞": ["congestion"],
        "機車": ["motorcycle"],
        "公車": ["bus"],
        "卸貨": ["loading_zone"],
    },
    "road": {
        "道路": ["road_surface"],
        "路平": ["road_surface"],
        "坑洞": ["pothole"],
        "路面": ["road_surface"],
        "施工": ["construction"],
        "標線": ["road_marking"],
    },
    "pedestrian": {
        "人行道": ["sidewalk"],
        "行人": ["pedestrian_crossing"],
        "斑馬線": ["pedestrian_crossing"],
        "無障礙": ["barrier_free"],
        "騎樓": ["arcade"],
        "通學步道": ["school_route"],
    },
    "environment": {
        "垃圾": ["garbage"],
        "噪音": ["noise"],
        "異味": ["odor"],
        "髒亂": ["dirty"],
        "空污": ["air_pollution"],
        "回收": ["recycling"],
    },
    "drainage": {
        "淹水": ["flooding"],
        "側溝": ["ditch"],
        "下水道": ["sewer"],
        "雨水": ["rainwater"],
        "排水": ["drainage_blocked"],
    },
    "safety": {
        "路燈": ["lighting"],
        "照明": ["lighting"],
        "危險路口": ["dangerous_intersection"],
        "治安": ["night_safety"],
        "公共設施": ["public_facility"],
        "安全": ["traffic_safety"],
    },
    "market": {
        "市場": ["market_traffic"],
        "商圈": ["crowd_flow"],
        "攤商": ["vendor"],
        "攤販": ["vendor"],
        "卸貨": ["unloading"],
        "人潮": ["crowd_flow"],
    },
    "park": {
        "公園": ["public_facility"],
        "綠地": ["public_facility"],
        "遊具": ["public_facility"],
    },
    "school": {
        "通學": ["school_commute"],
        "校園": ["school_zone"],
        "學校": ["school_zone"],
        "接送": ["parent_pickup"],
        "學生": ["student_safety"],
        "導護": ["crossing_guard"],
    },
    "senior": {
        "長照": ["senior_care"],
        "高齡": ["age_friendly"],
        "社福": ["social_welfare"],
        "弱勢": ["social_support"],
    },
    "culture": {
        "文化": ["culture_event"],
        "觀光": ["tourism_flow"],
        "歷史": ["historic_district"],
        "藝文": ["arts_venue"],
    },
    "administration": {
        "陳情": ["petition_handling"],
        "行政": ["administrative_efficiency"],
        "資訊公開": ["open_data"],
        "服務": ["public_service"],
    },
}

REQUIRED_OUTPUT_FIELDS = [
    "source_id",
    "video_title",
    "video_url",
    "council_term",
    "session_name",
    "primary_issue",
    "secondary_issues",
    "secondary_tags",
    "confidence",
    "summary",
    "recommended_action",
    "review_status",
]

LEGACY_ISSUE_KEYWORDS = {
    "交通": ["停車", "違停", "號誌", "交通", "機車", "汽車"],
    "道路": ["坑洞", "柏油", "路面", "施工"],
    "環境": ["垃圾", "髒亂", "異味", "清潔"],
    "人行": ["人行道", "斑馬線", "無障礙"],
    "公共安全": ["路燈", "照明", "危險"],
}


def _normalize_text(*parts: object) -> str:
    return " ".join(str(part or "").strip() for part in parts if str(part or "").strip())


def _topic_guess_issue(topic_guess: str) -> str | None:
    normalized = topic_guess.strip()
    if not normalized or normalized == "其他":
        return None
    if normalized in TAXONOMY_CODES:
        return normalized
    return TOPIC_GUESS_MAP.get(normalized)


def _score_record(record: dict[str, Any]) -> tuple[Counter[str], dict[str, set[str]]]:
    text = _normalize_text(
        record.get("video_title", ""),
        record.get("session_name", ""),
        record.get("council_term", ""),
        record.get("topic_guess", ""),
    )
    scores: Counter[str] = Counter()
    tags: dict[str, set[str]] = defaultdict(set)

    topic_issue = _topic_guess_issue(str(record.get("topic_guess", "")))
    if topic_issue:
        scores[topic_issue] += 2

    for issue, keyword_map in ISSUE_RULES.items():
        for keyword, keyword_tags in keyword_map.items():
            if keyword in text:
                scores[issue] += 1
                tags[issue].update(keyword_tags)

    return scores, tags


def _confidence_for_scores(scores: Counter[str]) -> float:
    if not scores:
        return 0.4

    ranked = scores.most_common()
    top_score = ranked[0][1]
    second_score = ranked[1][1] if len(ranked) > 1 else 0
    margin = max(top_score - second_score, 0)
    confidence = 0.58 + (top_score * 0.1) + (margin * 0.04)
    return round(min(confidence, 0.95), 2)


def _make_summary(primary_issue: str, confidence: float) -> str:
    display_name = ISSUE_DISPLAY_NAMES[primary_issue]
    if primary_issue == "other":
        return "目前 metadata 僅提供質詢影音標題與基本資訊，暫列為其他議題，建議人工檢視影音內容後再補充分類。"
    if confidence < 0.65:
        return f"依 metadata 可見線索，這筆質詢可能與「{display_name}」相關，但分類信心偏低，需人工複核。"
    return f"依 metadata 標題與來源欄位判斷，這筆質詢暫歸為「{display_name}」。分類僅反映資料中的議題線索，需人工 review 後再對外使用。"


def _make_recommended_action(primary_issue: str) -> str:
    display_name = ISSUE_DISPLAY_NAMES[primary_issue]
    if primary_issue == "other":
        return "建議補充逐字稿、議員姓名或更完整標題後重新分類。"
    return f"建議人工檢視影音內容，確認是否與「{display_name}」相關，並補上逐字稿或摘要依據。"


def classify_record(record: dict[str, Any]) -> dict[str, Any]:
    scores, tags = _score_record(record)
    if scores:
        ranked_issues = [issue for issue, _ in scores.most_common()]
        primary_issue = ranked_issues[0]
        secondary_issues = [issue for issue in ranked_issues[1:] if issue in TAXONOMY_CODES]
    else:
        primary_issue = "other"
        secondary_issues = []

    confidence = _confidence_for_scores(scores)
    if primary_issue == "other":
        confidence = min(confidence, 0.5)

    secondary_tags = sorted(
        tag
        for issue_tags in tags.values()
        for tag in issue_tags
    )
    review_status = "uncertain" if confidence < 0.65 else "unreviewed"

    return {
        "source_id": str(record.get("source_id", "")),
        "video_title": str(record.get("video_title", "")),
        "video_url": str(record.get("video_url", "")),
        "council_term": str(record.get("council_term", "")),
        "session_name": str(record.get("session_name", "")),
        "primary_issue": primary_issue,
        "secondary_issues": secondary_issues,
        "secondary_tags": secondary_tags,
        "confidence": confidence,
        "summary": _make_summary(primary_issue, confidence),
        "recommended_action": _make_recommended_action(primary_issue),
        "review_status": review_status,
    }


def classify(text: str) -> str:
    for category, keywords in LEGACY_ISSUE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "其他"


if __name__ == "__main__":
    sample = {"source_id": "sample", "video_title": "市場周邊停車與人行動線質詢"}
    print(classify_record(sample))
