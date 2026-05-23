from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
OUTPUT_PATH = DATA_DIR / "home_visible_mvp_summary.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

SOURCE_FILES = {
    "inventory": DATA_DIR / "open_data_url_inventory.json",
    "top10": DATA_DIR / "open_data_top10_review_tasks.json",
    "execution_packets": DATA_DIR / "open_data_manual_review_execution_packets.json",
    "patch_drafts": DATA_DIR / "open_data_manual_review_result_patch_drafts.json",
    "sample_results": DATA_DIR / "open_data_day1_sample_manual_review_results.json",
    "manual_review_form": DATA_DIR / "open_data_day1_manual_review_form_draft.json",
    "health_check": DATA_DIR / "dashboard_health_check.json",
}


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_home_visible_mvp_summary(
    source_files: dict[str, Path] = SOURCE_FILES,
    output_path: Path = OUTPUT_PATH,
) -> dict[str, Any]:
    inventory = load_json(source_files["inventory"])
    top10 = load_json(source_files["top10"])
    execution_packets = load_json(source_files["execution_packets"])
    patch_drafts = load_json(source_files["patch_drafts"])
    sample_results = load_json(source_files["sample_results"])
    manual_review_form = load_json(source_files["manual_review_form"])
    health_check = load_json(source_files["health_check"])

    day1_packet = next(
        packet for packet in execution_packets["packets"] if packet["review_day"] == "day_1"
    )

    visible_kpis = {
        "official_url_inventory_count": inventory["total_count"],
        "top10_review_tasks_count": top10["total_count"],
        "day1_task_count": day1_packet["task_count"],
        "day1_estimated_minutes": day1_packet["estimated_minutes_total"],
        "patch_draft_count": patch_drafts["total_count"],
        "sample_result_count": sample_results["total_count"],
        "manual_review_form_count": manual_review_form["total_count"],
        "health_status": health_check["status"],
    }

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_visible_mvp_home_summary",
        "status": "internal_review",
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": 0,
        "completed_modules": [
            "官方資料盤點",
            "Top 10 人工審核任務",
            "Crawler spec 草稿",
            "人工審核工作簿",
            "工程審查清單",
            "Evidence Pack",
            "人工審核結果輸入表",
            "人工審核 SOP",
            "人工審核工作包",
            "回填 Patch 草稿",
            "Day 1 填寫範例",
            "Day 1 審核表單草稿",
        ],
        "visible_kpis": visible_kpis,
        "next_actions": [
            "完成 Day 1 人工審核",
            "填寫 Day 1 表單",
            "產生回填 PR",
            "更新人工審核結果",
            "才能進入 engineering review",
        ],
        "safety_notes": [
            "no live crawler",
            "no personal data",
            "no private complaint full text",
            "no auto publish",
            "manual review required",
            "crawler_execution_allowed = false",
            "engineering_review_allowed = false",
        ],
    }

    assert result["visible_kpis"]["official_url_inventory_count"] == 29
    assert result["visible_kpis"]["top10_review_tasks_count"] == 10
    assert result["visible_kpis"]["day1_task_count"] == 3
    assert result["visible_kpis"]["day1_estimated_minutes"] == 90
    assert result["visible_kpis"]["patch_draft_count"] == 10
    assert result["visible_kpis"]["sample_result_count"] == 3
    assert result["visible_kpis"]["manual_review_form_count"] == 3
    assert result["visible_kpis"]["health_status"] == "ok"
    assert result["crawler_execution_allowed"] is False
    assert result["engineering_review_allowed_count"] == 0

    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict[str, Any]:
    return build_home_visible_mvp_summary()


if __name__ == "__main__":
    main()
