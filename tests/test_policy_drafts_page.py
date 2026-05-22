from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "policy-drafts.html"
SCRIPT = DASHBOARD_DIR / "policy-drafts.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_policy_drafts_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_policy_drafts_page_discloses_internal_draft_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "政策草稿候選清單" in content
    assert "不是正式政見" in content
    assert "人工審核" in content


def test_policy_drafts_renderer_reads_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/policy_draft_candidates.json" in content
    assert "bootPolicyDrafts" in content
    assert "renderDrafts" in content


def test_policy_drafts_page_has_render_targets() -> None:
    content = HTML.read_text(encoding="utf-8")
    for target in [
        'data-stat="total"',
        'data-stat="needs-review"',
        'data-stat="departments"',
        'data-render="policy-drafts"',
    ]:
        assert target in content


def test_policy_drafts_page_is_in_site_map_and_nav() -> None:
    assert "./policy-drafts.html" in SITE_MAP.read_text(encoding="utf-8")
    assert "./policy-drafts.html" in SHARED_NAV.read_text(encoding="utf-8")
