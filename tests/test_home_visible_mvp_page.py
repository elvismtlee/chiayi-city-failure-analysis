from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "dashboard" / "index.html"


def test_home_visible_mvp_page_exists() -> None:
    assert INDEX_PATH.exists()


def test_home_visible_mvp_page_contains_visible_mvp_sections() -> None:
    content = INDEX_PATH.read_text(encoding="utf-8")

    assert "嘉義城市故障分析資料庫" in content
    assert "Day 1" in content
    assert "人工審核工作包" in content
    assert "審核表單草稿" in content
    assert "回填 Patch 草稿" in content
    assert "目前狀態：內部人工審核階段" in content
    assert "尚未啟動 live crawler" in content
    assert './shared-nav.js?v=20260523-navux' in content
