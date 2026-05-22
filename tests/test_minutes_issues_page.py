from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"
HTML = DASHBOARD_DIR / "minutes-issues.html"
SCRIPT = DASHBOARD_DIR / "minutes-issues.js"
SITE_MAP = DASHBOARD_DIR / "data" / "site_map.json"
SHARED_NAV = DASHBOARD_DIR / "shared-nav.js"


def test_minutes_issues_page_files_exist() -> None:
    assert HTML.exists()
    assert SCRIPT.exists()


def test_minutes_issues_page_discloses_sample_safety_scope() -> None:
    content = HTML.read_text(encoding="utf-8")
    assert "會議紀錄議題候選清單" in content
    assert "不是正式結論" in content
    assert "不代表完整 CYCC 正式資料庫" in content
    assert "人工政策審核" in content


def test_minutes_issues_page_has_required_render_targets() -> None:
    content = HTML.read_text(encoding="utf-8")
    for target in [
        'data-stat="total"',
        'data-stat="departments"',
        'data-stat="keywords"',
        'data-stat="sample-only"',
        'data-render="minutes-issue-candidates"',
    ]:
        assert target in content


def test_minutes_issues_page_does_not_use_polling_terms() -> None:
    content = HTML.read_text(encoding="utf-8") + SCRIPT.read_text(encoding="utf-8")
    assert "民調" not in content
    assert "支持度調查" not in content


def test_minutes_issues_renderer_reads_issue_candidates_json() -> None:
    content = SCRIPT.read_text(encoding="utf-8")
    assert "./data/cycc_minutes_issue_candidates.json" in content
    assert "bootMinutesIssues" in content
    assert "renderStats" in content
    assert "renderCandidates" in content


def test_minutes_issues_page_is_in_site_map() -> None:
    content = SITE_MAP.read_text(encoding="utf-8")
    assert "會議紀錄議題" in content
    assert "./minutes-issues.html" in content


def test_minutes_issues_page_is_in_shared_nav() -> None:
    content = SHARED_NAV.read_text(encoding="utf-8")
    assert "會議紀錄議題" in content
    assert "./minutes-issues.html" in content
