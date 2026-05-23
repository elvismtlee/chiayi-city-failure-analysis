from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "open-data-review-evidence.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_open_data_review_evidence_page_exists_with_filters_and_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "官方資料人工審核證據包" in content
    assert 'id="openDataReviewEvidenceSearch"' in content
    assert 'id="openDataReviewEvidenceDay"' in content
    assert 'id="openDataReviewEvidenceBatch"' in content
    assert 'id="openDataReviewEvidenceStatus"' in content
    assert 'id="openDataReviewEvidenceTopicGroup"' in content
    assert "manual review" in content
    assert "no auto publish" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "engineering_review_allowed" in content
    assert './shared-nav.js?v=20260523-navux' in content


def test_site_pages_renders_open_data_review_evidence_pack() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "./data/open_data_review_evidence_pack.json" in content
    assert "setupOpenDataReviewEvidence" in content
    assert "openDataReviewEvidenceSearch" in content
    assert "openDataReviewEvidenceDay" in content
    assert "openDataReviewEvidenceBatch" in content


def test_open_data_review_evidence_page_links_to_manual_review_result_template() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-manual-review-results.html" in content
    assert "建立審核結果輸入表" in content


def test_open_data_review_evidence_page_links_to_manual_review_sop() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "./open-data-manual-review-sop.html" in content
    assert "查看人工審核 SOP" in content
