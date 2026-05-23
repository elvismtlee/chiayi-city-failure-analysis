from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "open_data_readiness_score_schema.yml"


def load_schema() -> dict:
    data: dict[str, object] = {}
    current_key = ""
    current_list: list[str] | None = None
    current_dict: dict[str, object] | None = None

    for raw_line in SCHEMA.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - "):
            if current_list is None:
                raise ValueError("Unexpected list item outside of a list")
            current_list.append(line[4:].strip())
            continue
        if line.startswith("  ") and current_dict is not None:
            key, value = line.strip().split(":", 1)
            value = value.strip()
            if value in {"true", "false"}:
                current_dict[key] = value == "true"
            elif value.isdigit():
                current_dict[key] = int(value)
            else:
                current_dict[key] = value
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_list = None
        current_dict = None
        if value:
            if value in {"true", "false"}:
                data[key] = value == "true"
            else:
                data[key] = value
        else:
            if key in {"score_dimensions", "readiness_level", "crawler_stage", "scoring_formula", "readiness_level_rules", "public_use_gate"}:
                current_key = key
                current_list = []
                data[current_key] = current_list
            else:
                current_key = key
                current_dict = {}
                data[current_key] = current_dict
    return data


def test_open_data_readiness_score_schema_exists_and_flags_are_safe() -> None:
    data = load_schema()
    assert SCHEMA.exists()
    assert data["public_use_status"] == "internal_readiness_score_schema"
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True
    assert data["no_live_crawler"] is True


def test_open_data_readiness_score_schema_contains_dimensions_and_levels() -> None:
    data = load_schema()
    dimensions = set(data["score_dimensions"])
    expected_dimensions = {
        "official_source_score",
        "data_format_score",
        "license_clarity_score",
        "update_cadence_score",
        "west_district_relevance_score",
        "dashboard_value_score",
        "crawler_risk_score",
    }
    assert dimensions == expected_dimensions
    readiness_levels = set(data["readiness_level"])
    assert readiness_levels == {"high", "medium", "low", "blocked"}
