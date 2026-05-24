from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "project-landing.html"


def test_project_landing_page_exists() -> None:
    assert PAGE.exists()


def test_project_landing_page_shows_public_facing_progress() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "公開展示頁" in content or "專案說明" in content
    assert "嘉義市城市問題儀表板專案總覽" in content
    assert "現在已經能看什麼" in content
    assert "現在怎麼開始" in content
    assert "主要功能" in content
    assert "下一步會補什麼" in content
    assert "no live crawler" in content
    assert "approved_for_crawling" in content
    assert "./shared-nav.js?v=20260523-navux" in content
