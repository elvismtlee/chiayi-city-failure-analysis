from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "project-landing.html"


def test_project_landing_page_exists() -> None:
    assert PAGE.exists()


def test_project_landing_page_shows_public_facing_progress() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "專案說明" in content
    assert "城市問題儀表板" in content
    assert "原型案件數" in content
    assert "質詢紀錄數" in content
    assert "城市熱點" in content
    assert "官方資料源" in content
    assert "no live crawler" in content
    assert "approved_for_crawling" in content
    assert "./shared-nav.js?v=20260523-navux" in content
