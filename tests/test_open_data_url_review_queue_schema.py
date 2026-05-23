from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "config" / "open_data_url_review_queue_schema.yml"


def load_schema() -> dict:
    data: dict[str, object] = {}
    current_list_key = ""
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
        if value:
            if value in {"true", "false"}:
                data[key] = value == "true"
            else:
                data[key] = value
            current_list = None
            current_list_key = ""
            continue
        current_list_key = key
        current_list = []
        data[current_list_key] = current_list
    return data


def test_open_data_url_review_queue_schema_exists_and_flags_are_safe() -> None:
    data = load_schema()
    assert SCHEMA.exists()
    assert data["public_use_status"] == "internal_url_review_queue_schema"
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True
    assert data["no_live_crawler"] is True


def test_open_data_url_review_queue_schema_required_fields_cover_review_controls() -> None:
    data = load_schema()
    required_fields = set(data["required_fields"])
    for field in [
        "inventory_id",
        "url_review_status",
        "crawler_candidate",
        "crawler_priority",
        "crawler_blockers",
    ]:
        assert field in required_fields
