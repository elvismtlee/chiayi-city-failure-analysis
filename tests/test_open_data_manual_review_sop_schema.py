from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "config" / "open_data_manual_review_sop_schema.yml"


def test_open_data_manual_review_sop_schema_exists_and_flags_are_safe() -> None:
    assert SCHEMA_PATH.exists()
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["public_use_status"] == "internal_manual_review_sop_schema"
    assert schema["manual_review_required"] is True
    assert schema["no_auto_publish"] is True
    assert schema["no_personal_data"] is True
    assert schema["no_live_crawler"] is True
    assert schema["crawler_execution_allowed"] is False
    assert schema["human_approval_required"] is True


def test_open_data_manual_review_sop_schema_required_fields() -> None:
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    required_fields = set(schema["required_fields"])
    for field in [
        "sop_id",
        "daily_batches",
        "safety_checklist",
        "result_template_fill_steps",
        "handoff_next_actions",
    ]:
        assert field in required_fields
