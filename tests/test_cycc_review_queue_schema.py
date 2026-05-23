from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "cycc_review_queue_schema.yml"
SOP = ROOT / "docs" / "cycc_review_queue_sop.md"


def test_cycc_review_queue_schema_is_internal_and_safe() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    assert data["public_use_status"] == "internal_review_queue_schema"
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_cycc_review_queue_required_fields() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    required = set(data["required_fields"])
    for field in [
        "record_id",
        "source_type",
        "title",
        "source_url",
        "detail_url",
        "review_status",
        "reviewer",
        "reviewed_at",
        "source_verified",
        "original_content_reviewed",
        "citation_ready",
        "public_summary_allowed",
        "caution_notes",
    ]:
        assert field in required


def test_cycc_review_queue_public_gate() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    gate = data["public_use_gate"]
    assert gate["allowed_public_status"] == ["citation_ready"]
    assert "needs_review" in gate["forbidden_public_status"]
    assert "source_verified" in gate["forbidden_public_status"]
    assert "do_not_use_publicly" in gate["forbidden_public_status"]
    assert gate["require_source_link"] is True
    assert gate["require_neutral_summary"] is True
    assert gate["require_no_personal_data"] is True
    assert gate["require_no_auto_publish"] is True


def test_cycc_review_queue_sop_exists_and_sets_limits() -> None:
    content = SOP.read_text(encoding="utf-8")
    assert "CYCC metadata 人工審核佇列 SOP" in content
    assert "review_status: needs_review" in content
    assert "review_status: citation_ready" in content
    assert "不可只看 metadata 就下結論" in content
    assert "不可自動發布" in content
    assert "每天可處理 5 到 10 筆" in content
