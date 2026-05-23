from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "source-verification-workspace.html"
SITE_MAP = ROOT / "dashboard" / "data" / "site_map.json"
SHARED_NAV = ROOT / "dashboard" / "shared-nav.js"


def test_source_verification_workspace_exists() -> None:
    assert PAGE.exists()


def test_source_verification_workspace_has_plain_language_manual_checks() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "資料源人工檢查工作台" in content
    assert "打開一筆官方 URL" in content
    for field in [
        "source_title",
        "source_owner",
        "source_url",
        "is_official_source",
        "data_format",
        "visible_fields",
        "privacy_risk",
        "recommended_next_action",
    ]:
        assert field in content
    assert "no live crawler" in content
    assert "no source_url requests" in content
    assert "crawler_execution_allowed = false" in content
    assert "engineering_review_allowed = false" in content
    assert "approved_for_crawling" in content
    assert "./shared-nav.js?v=20260523-navux" in content


def test_source_verification_workspace_is_in_site_map_and_shared_nav() -> None:
    site_map = json.loads(SITE_MAP.read_text(encoding="utf-8"))
    assert any(item.get("path") == "./source-verification-workspace.html" for item in site_map)
    nav_content = SHARED_NAV.read_text(encoding="utf-8")
    assert "資料源檢查工作台" in nav_content
    assert "./source-verification-workspace.html" in nav_content
