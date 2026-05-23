from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "project-landing.html"


def test_project_landing_page_exists() -> None:
    assert PAGE.exists()


def test_project_landing_page_shows_public_facing_progress() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "嘉義市 12 年城市故障分析資料庫" in content
    assert "公開展示版" in content
    assert "現在怎麼開始" in content
    assert "打開資料源人工檢查工作台" in content
    assert "Day 1 操作看板" in content
    assert "29 筆官方 URL" in content
    assert "10 筆高優先審核任務" in content
    assert "3 筆任務" in content
    assert "no live crawler" in content
    assert "crawler_execution_allowed = false" in content
    assert "./shared-nav.js?v=20260523-navux" in content
