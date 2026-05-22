from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "dashboard" / "data" / "social_post_drafts.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "short_video_script_drafts.json"

SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}
REVIEW_STATUS = "needs_video_review"
PUBLIC_USE_STATUS = "internal_video_draft"
RECOMMENDED_NEXT_STEP = "manual_video_review"
REQUIRED_FIELDS = [
    "script_id",
    "source_post_id",
    "issue_title",
    "hook",
    "opening_line",
    "scene_plan",
    "voiceover",
    "subtitle_lines",
    "call_to_action",
    "source_urls",
    "review_status",
    "public_use_status",
    "risk_notes",
    "recommended_next_step",
]


def load_social_posts(input_path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    return json.loads(input_path.read_text(encoding="utf-8"))


def script_id(source_post_id: str) -> str:
    return f"video-script-{source_post_id[-12:]}"


def first_post_per_policy(posts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for item in posts:
        selected.setdefault(item["source_draft_id"], item)
    return list(selected.values())


def build_script(post: dict[str, Any]) -> dict[str, Any]:
    title = post["issue_title"]
    item = {
        "script_id": script_id(post["post_id"]),
        "source_post_id": post["post_id"],
        "issue_title": title,
        "hook": f"一個地方議題，先從公開來源與現場脈絡看起。",
        "opening_line": f"今天先用 60 秒，整理「{title}」的內部草稿重點。",
        "scene_plan": [
            "一人可拍攝：面向鏡頭口播，說明這是內部草稿與待審核資料。",
            "一人可拍攝：拍攝公開場域空景或桌面資料整理畫面。",
            "一人可拍攝：收尾提醒需要人工 review 後才可對外使用。",
        ],
        "voiceover": f"目前這份內容仍是 internal draft，依政策草稿候選整理 {title} 的問題脈絡。內容不代表正式結論，後續需確認來源、上下文與政策可行性。",
        "subtitle_lines": [
            "內部短影音腳本草稿",
            "來源與上下文仍需人工 review",
            "不自動發布，對外使用前需審核",
        ],
        "call_to_action": post["call_to_action"],
        "source_urls": list(post.get("source_urls") or []),
        "review_status": REVIEW_STATUS,
        "public_use_status": PUBLIC_USE_STATUS,
        "risk_notes": "需人工確認來源、語氣、畫面權利與法遵；避免未經同意或造成誤解的素材使用。",
        "recommended_next_step": RECOMMENDED_NEXT_STEP,
    }
    validate_script(item)
    return item


def validate_script(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing video script fields: {', '.join(missing)}")
    sensitive = {key.lower() for key in item} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")
    if not isinstance(item["scene_plan"], list) or not item["scene_plan"]:
        raise ValueError("scene_plan must be a non-empty list.")
    if not isinstance(item["subtitle_lines"], list) or not item["subtitle_lines"]:
        raise ValueError("subtitle_lines must be a non-empty list.")
    if item["review_status"] != REVIEW_STATUS:
        raise ValueError("Video scripts must require video review.")
    if item["public_use_status"] != PUBLIC_USE_STATUS:
        raise ValueError("Video scripts must remain internal_video_draft.")
    if item["recommended_next_step"] != RECOMMENDED_NEXT_STEP:
        raise ValueError("Video scripts must recommend manual_video_review.")


def build_short_video_script_drafts(records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    posts = records if records is not None else load_social_posts()
    return [build_script(post) for post in first_post_per_policy(posts)]


def write_short_video_script_drafts(output_path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    drafts = build_short_video_script_drafts()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(drafts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return drafts


if __name__ == "__main__":
    drafts = write_short_video_script_drafts()
    print(f"Wrote {len(drafts)} short video script drafts to {OUTPUT_PATH.relative_to(ROOT)}")
