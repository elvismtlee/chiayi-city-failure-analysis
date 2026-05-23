from __future__ import annotations

import json
from pathlib import Path

from scripts.build_open_data_manual_review_sop import build_open_data_manual_review_sop


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_sop.json"


def test_build_open_data_manual_review_sop(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_sop.json"
    result = build_open_data_manual_review_sop(output_path=output_path)

    assert output_path.exists()
    parsed = json.loads(output_path.read_text(encoding="utf-8"))
    assert parsed["public_use_status"] == "internal_manual_review_sop"
    assert parsed["total_tasks"] == 10
    assert parsed["source_result_template_count"] == 10
    assert parsed["review_days"]["day_1"] == 3
    assert parsed["review_days"]["day_2"] == 4
    assert parsed["review_days"]["day_3"] == 3
    assert parsed["engineering_review_allowed_count"] == 0
    assert parsed["crawler_execution_allowed"] is False
    assert parsed["no_live_crawler"] is True
    assert parsed["manual_review_required"] is True
    assert parsed["no_auto_publish"] is True
    assert parsed["no_personal_data"] is True
    assert len(parsed["sop"]["safety_checklist"]) >= 8
    assert len(parsed["sop"]["per_source_review_steps"]) >= 10
    assert len(parsed["sop"]["result_template_fill_steps"]) >= 10
    assert "approved_for_crawling" not in json.dumps(parsed, ensure_ascii=False)
    assert '"live_crawler"' not in json.dumps(parsed, ensure_ascii=False)
    assert result["estimated_total_minutes"] == 285


def test_open_data_manual_review_sop_output_matches_expected_shape() -> None:
    parsed = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    assert parsed["public_use_status"] == "internal_manual_review_sop"
    assert parsed["total_tasks"] == 10
    assert parsed["source_result_template_count"] == 10
    assert parsed["review_days"] == {"day_1": 3, "day_2": 4, "day_3": 3}
    assert parsed["engineering_review_allowed_count"] == 0
    assert parsed["crawler_execution_allowed"] is False
    assert len(parsed["sop"]["safety_checklist"]) >= 8
    assert len(parsed["sop"]["per_source_review_steps"]) >= 10
    assert len(parsed["sop"]["result_template_fill_steps"]) >= 10
