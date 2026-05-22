from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "policy-drafts.html"
SCRIPT = DASHBOARD_DIR / "policy-drafts.js"


def test_policy_drafts_page_has_dashboard_layout() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "政策草稿候選清單" in content
    assert "data-render=\"breadcrumb\"" in content
    assert "kpi-grid" in content
    assert "draft-grid" in content
    assert "正式政見" in content
    assert "人工審核" in content


def test_policy_drafts_renderer_builds_cards() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/policy_draft_candidates.json" in content
    assert "makeDraftCard" in content
    assert "problem_statement" in content
    assert "policy_options" in content
    assert "possible_root_causes" in content
