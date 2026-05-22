from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "dashboard" / "data" / "policy_draft_candidates.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "social_post_drafts.json"

CHANNELS = ["facebook", "threads", "line"]
SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}
BANNED_TERMS = ["民調", "支持度調查"]
REVIEW_STATUS = "needs_communication_review"
PUBLIC_USE_STATUS = "internal_social_draft"
RECOMMENDED_NEXT_STEP = "manual_communication_review"
REQUIRED_FIELDS = [
    "post_id",
    "source_draft_id",
    "issue_title",
    "channel",
    "headline",
    "body",
    "short_version",
    "call_to_action",
    "source_urls",
    "review_status",
    "public_use_status",
    "risk_notes",
    "recommended_next_step",
]


def load_policy_drafts(input_path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    return json.loads(input_path.read_text(encoding="utf-8"))


def post_id(channel: str, source_draft_id: str) -> str:
    return f"social-{channel}-{source_draft_id[-12:]}"


def channel_hint(channel: str) -> str:
    return {
        "facebook": "適合較完整說明來源脈絡與初步觀察。",
        "threads": "適合短句呈現議題重點，保留人工審核提醒。",
        "line": "適合地方群組內部討論草稿，語氣清楚溫和。",
    }[channel]


def build_post(draft: dict[str, Any], channel: str) -> dict[str, Any]:
    title = draft["issue_title"]
    department = draft.get("responsible_department") or "相關局處"
    headline = f"{title}：先整理問題脈絡，再做政策審核"
    body = (
        f"這是 internal draft，內容依政策草稿候選整理，尚未作為正式對外聲明。"
        f"目前先把「{title}」的來源、局處脈絡與可能改善方向整理給人工審核。"
        f"相關局處暫列為 {department}，後續仍需確認上下文、法遵與表述。"
    )
    short_version = f"{title} 先作為內部草稿整理，需人工確認來源與政策脈絡後才可對外使用。"
    item = {
        "post_id": post_id(channel, draft["draft_id"]),
        "source_draft_id": draft["draft_id"],
        "issue_title": title,
        "channel": channel,
        "headline": headline,
        "body": f"{body} {channel_hint(channel)}",
        "short_version": short_version,
        "call_to_action": "歡迎提供你觀察到的地方問題，作為後續人工整理參考。",
        "source_urls": list(draft.get("source_urls") or []),
        "review_status": REVIEW_STATUS,
        "public_use_status": PUBLIC_USE_STATUS,
        "risk_notes": "需人工確認來源、語氣與法遵；internal draft, needs human review.",
        "recommended_next_step": RECOMMENDED_NEXT_STEP,
    }
    validate_post(item)
    return item


def validate_post(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing social post fields: {', '.join(missing)}")
    sensitive = {key.lower() for key in item} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")
    if item["channel"] not in CHANNELS:
        raise ValueError("Unsupported social channel.")
    if item["review_status"] != REVIEW_STATUS:
        raise ValueError("Social drafts must require communication review.")
    if item["public_use_status"] != PUBLIC_USE_STATUS:
        raise ValueError("Social drafts must remain internal_social_draft.")
    if item["recommended_next_step"] != RECOMMENDED_NEXT_STEP:
        raise ValueError("Social drafts must recommend manual_communication_review.")
    serialized = json.dumps(item, ensure_ascii=False)
    for term in BANNED_TERMS:
        if term in serialized:
            raise ValueError(f"Banned term found in social draft: {term}")


def build_social_post_drafts(records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    source_records = records if records is not None else load_policy_drafts()
    return [build_post(draft, channel) for draft in source_records for channel in CHANNELS]


def write_social_post_drafts(output_path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    drafts = build_social_post_drafts()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(drafts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return drafts


if __name__ == "__main__":
    drafts = write_social_post_drafts()
    print(f"Wrote {len(drafts)} social post drafts to {OUTPUT_PATH.relative_to(ROOT)}")
