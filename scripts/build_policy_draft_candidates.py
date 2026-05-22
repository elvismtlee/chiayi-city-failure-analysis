from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WEEKLY_SUMMARY_PATH = ROOT / "dashboard" / "data" / "weekly_summary_draft.json"
ISSUE_CANDIDATES_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_issue_candidates.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "policy_draft_candidates.json"

SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}
PUBLIC_USE_STATUS = "internal_policy_draft"
REVIEW_STATUS = "needs_policy_review"
RECOMMENDED_NEXT_STEP = "manual_policy_review"
REQUIRED_FIELDS = [
    "draft_id",
    "source_candidate_id",
    "issue_title",
    "problem_statement",
    "possible_root_causes",
    "policy_options",
    "first_action",
    "responsible_department",
    "source_urls",
    "review_status",
    "public_use_status",
    "risk_notes",
    "recommended_next_step",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_source_records() -> list[dict[str, Any]]:
    if WEEKLY_SUMMARY_PATH.exists():
        return load_json(WEEKLY_SUMMARY_PATH).get("top_issues", [])
    return load_json(ISSUE_CANDIDATES_PATH)


def draft_id(source_candidate_id: str) -> str:
    return f"policy-draft-{source_candidate_id[-12:]}"


def problem_statement(item: dict[str, Any]) -> str:
    text = str(item.get("summary") or item.get("issue_summary") or item.get("issue_title", "")).strip()
    text = text.removeprefix("依 reviewed sample 摘要：")
    return f"依內部 sample 摘要整理：{text[:140]}"


def possible_root_causes(item: dict[str, Any]) -> list[str]:
    keywords = item.get("issue_keywords") or []
    if not keywords:
        return ["待確認：需補足會議紀錄上下文與相關局處說明。"]
    return [f"待確認：{keyword} 相關成因需回查來源與局處脈絡。" for keyword in keywords[:3]]


def policy_options(item: dict[str, Any]) -> list[str]:
    title = item.get("issue_title", "議題")
    department = item.get("department", "相關局處")
    return [
        f"整理 {title} 的公開來源、日期與局處回應脈絡。",
        f"建立一頁式內部問題脈絡表，供 {department} 相關政策審核使用。",
        "彙整可行改善方向、限制條件與後續追蹤欄位，先供人工審核。",
    ]


def build_policy_draft(item: dict[str, Any]) -> dict[str, Any]:
    source_candidate_id = item.get("source_candidate_id") or item["candidate_id"]
    source_url = item.get("source_url")
    draft = {
        "draft_id": draft_id(source_candidate_id),
        "source_candidate_id": source_candidate_id,
        "issue_title": item["issue_title"],
        "problem_statement": problem_statement(item),
        "possible_root_causes": possible_root_causes(item),
        "policy_options": policy_options(item),
        "first_action": "人工確認來源與局處脈絡",
        "responsible_department": item.get("department", ""),
        "source_urls": [source_url] if source_url else [],
        "review_status": REVIEW_STATUS,
        "public_use_status": PUBLIC_USE_STATUS,
        "risk_notes": "需人工確認來源、上下文與法遵後，才可轉為對外素材。",
        "recommended_next_step": RECOMMENDED_NEXT_STEP,
    }
    validate_policy_draft(draft)
    return draft


def validate_policy_draft(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing policy draft fields: {', '.join(missing)}")
    sensitive = {key.lower() for key in item} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")
    if item["review_status"] != REVIEW_STATUS:
        raise ValueError("Policy drafts must require policy review.")
    if item["public_use_status"] != PUBLIC_USE_STATUS:
        raise ValueError("Policy drafts must remain internal_policy_draft.")
    if item["recommended_next_step"] != RECOMMENDED_NEXT_STEP:
        raise ValueError("Policy drafts must recommend manual_policy_review.")
    if not isinstance(item["possible_root_causes"], list):
        raise ValueError("possible_root_causes must be a list.")
    if not isinstance(item["policy_options"], list) or len(item["policy_options"]) < 3:
        raise ValueError("policy_options must include at least three options.")


def build_policy_drafts(records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    return [build_policy_draft(item) for item in (records if records is not None else load_source_records())]


def write_policy_drafts(output_path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    drafts = build_policy_drafts()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(drafts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return drafts


if __name__ == "__main__":
    drafts = write_policy_drafts()
    print(f"Wrote {len(drafts)} policy draft candidates to {OUTPUT_PATH.relative_to(ROOT)}")
