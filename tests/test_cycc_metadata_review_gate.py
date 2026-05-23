from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "cycc_metadata_review_gate.yml"
DOC = ROOT / "docs" / "cycc_metadata_review_workflow.md"


def test_cycc_review_gate_config_is_internal_and_safe() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    assert data["public_use_status"] == "internal_review_gate"
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True
    assert data["metadata_only_default"] is True


def test_cycc_review_gate_statuses_and_public_rules() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    allowed = set(data["review_statuses"]["allowed"])
    assert "needs_review" in allowed
    assert "source_verified" in allowed
    assert "content_reviewed" in allowed
    assert "citation_ready" in allowed
    assert "do_not_use_publicly" in allowed
    assert data["public_use_rules"]["may_use_for_public_citation"] == ["citation_ready"]
    assert data["public_use_rules"]["never_auto_publish"] is True
    assert data["public_use_rules"]["require_human_approval_before_public_use"] is True


def test_cycc_review_gate_requires_original_source_checks() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    checks = set(data["review_statuses"]["citation_ready_required_checks"])
    assert "source_url_verified" in checks
    assert "detail_url_verified" in checks
    assert "official_source_confirmed" in checks
    assert "original_content_reviewed" in checks
    assert "source_link_retained" in checks


def test_cycc_review_gate_blocks_sensitive_uses() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    prohibited = set(data["prohibited_uses"])
    assert "auto_social_posting" in prohibited
    assert "personal_data_collection" in prohibited
    assert "private_complaint_text_collection" in prohibited
    assert "unverified_accusation" in prohibited
    assert "fundraising_or_payment_action" in prohibited


def test_cycc_review_workflow_document_exists() -> None:
    content = DOC.read_text(encoding="utf-8")
    assert "CYCC 公開 metadata 人工審核流程" in content
    assert "review_status: needs_review" in content
    assert "citation_ready" in content
    assert "不得把 metadata 直接改寫成指控" in content
    assert "不自動發布" in content
