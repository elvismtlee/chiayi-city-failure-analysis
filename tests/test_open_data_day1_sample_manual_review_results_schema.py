from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "open_data_day1_sample_manual_review_results_schema.yml"


def load_schema() -> dict:
    data: dict[str, object] = {}
    current_list: list[str] | None = None
    for raw_line in SCHEMA.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list is None:
                raise ValueError("Unexpected list item outside of a list")
            current_list.append(line[4:].strip())
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_list = None
        if value:
            if value in {"true", "false"}:
                data[key] = value == "true"
            else:
                data[key] = value
        else:
            current_list = []
            data[key] = current_list
    return data


def test_open_data_day1_sample_manual_review_results_schema_exists_and_flags_are_safe() -> None:
    data = load_schema()
    assert SCHEMA.exists()
    assert data["public_use_status"] == "internal_day1_sample_manual_review_results_schema"
    assert data["sample_only"] is True
    assert data["not_actual_review_result"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True
    assert data["no_live_crawler"] is True
    assert data["crawler_execution_allowed"] is False
    assert data["human_approval_required"] is True


def test_open_data_day1_sample_manual_review_results_schema_contains_required_fields() -> None:
    data = load_schema()
    required_fields = set(data["required_fields"])
    assert "sample_id" in required_fields
    assert "sample_evidence_summary" in required_fields
    assert "sample_reviewer_decision" in required_fields
    assert "fields_not_changed" in required_fields
    assert "blocked_fields" in required_fields
