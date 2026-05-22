from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "dashboard" / "data" / "short_video_script_drafts.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "filming_checklists.json"

SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}
REVIEW_STATUS = "needs_filming_review"
PUBLIC_USE_STATUS = "internal_filming_plan"
RECOMMENDED_NEXT_STEP = "manual_filming_review"
LOCATION_TYPES = {"office", "street", "market", "school_area", "park", "other"}
REQUIRED_FIELDS = [
    "checklist_id",
    "source_script_id",
    "issue_title",
    "shooting_goal",
    "location_type",
    "scene_tasks",
    "a_roll_notes",
    "b_roll_notes",
    "props_needed",
    "audio_notes",
    "estimated_minutes",
    "review_status",
    "public_use_status",
    "risk_notes",
    "recommended_next_step",
]


def load_video_scripts(input_path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    return json.loads(input_path.read_text(encoding="utf-8"))


def checklist_id(source_script_id: str) -> str:
    return f"filming-{source_script_id[-12:]}"


def location_type_for(title: str) -> str:
    if any(keyword in title for keyword in ["道路", "停車", "行人", "騎樓"]):
        return "street"
    if "市場" in title or "商圈" in title:
        return "market"
    if "學校" in title:
        return "school_area"
    if "公園" in title:
        return "park"
    return "other"


def build_checklist(script: dict[str, Any]) -> dict[str, Any]:
    title = script["issue_title"]
    item = {
        "checklist_id": checklist_id(script["script_id"]),
        "source_script_id": script["script_id"],
        "issue_title": title,
        "shooting_goal": f"拍出「{title}」的內部草稿說明素材，供人工審核後使用。",
        "location_type": location_type_for(title),
        "scene_tasks": [
            "確認拍攝地點是公開可拍攝場域，先做現場安全判斷。",
            "錄製 30 到 60 秒口播，開頭說明是內部草稿素材。",
            "補拍環境空景、資料整理畫面與不含私人資訊的細節畫面。",
        ],
        "a_roll_notes": "人物口播以清楚、溫和、可查證語氣說明，避免把草稿說成正式結論。",
        "b_roll_notes": "補充畫面以公開場域空景與資料整理畫面為主，避開可識別私人資訊與未同意近距離人物。",
        "props_needed": ["手機或相機", "簡短提詞稿", "收音設備", "來源與審核提示卡"],
        "audio_notes": "拍攝前測試收音，避開車流與施工高噪音時段。",
        "estimated_minutes": 30,
        "review_status": REVIEW_STATUS,
        "public_use_status": PUBLIC_USE_STATUS,
        "risk_notes": "需人工確認地點、影像權與安全；needs human review before public use.",
        "recommended_next_step": RECOMMENDED_NEXT_STEP,
    }
    validate_checklist(item)
    return item


def validate_checklist(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing filming checklist fields: {', '.join(missing)}")
    sensitive = {key.lower() for key in item} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")
    if item["location_type"] not in LOCATION_TYPES:
        raise ValueError("Unsupported location_type.")
    if not isinstance(item["scene_tasks"], list) or not item["scene_tasks"]:
        raise ValueError("scene_tasks must be a non-empty list.")
    if not isinstance(item["props_needed"], list):
        raise ValueError("props_needed must be a list.")
    if not isinstance(item["estimated_minutes"], int):
        raise ValueError("estimated_minutes must be an int.")
    if item["review_status"] != REVIEW_STATUS:
        raise ValueError("Filming checklists must require filming review.")
    if item["public_use_status"] != PUBLIC_USE_STATUS:
        raise ValueError("Filming checklists must remain internal_filming_plan.")
    if item["recommended_next_step"] != RECOMMENDED_NEXT_STEP:
        raise ValueError("Filming checklists must recommend manual_filming_review.")


def build_filming_checklists(records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    scripts = records if records is not None else load_video_scripts()
    return [build_checklist(script) for script in scripts]


def write_filming_checklists(output_path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    checklists = build_filming_checklists()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(checklists, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return checklists


if __name__ == "__main__":
    checklists = write_filming_checklists()
    print(f"Wrote {len(checklists)} filming checklists to {OUTPUT_PATH.relative_to(ROOT)}")
