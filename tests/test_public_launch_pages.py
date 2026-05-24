from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard"


def test_public_launch_pages_exist() -> None:
    for page in [
        "index.html",
        "map.html",
        "command-center.html",
        "sources.html",
        "methodology.html",
        "health-check.html",
        "shared-nav.js",
    ]:
        assert (DASHBOARD / page).exists(), f"Missing public page asset: {page}"


def test_shared_nav_prioritizes_public_pages() -> None:
    content = (DASHBOARD / "shared-nav.js").read_text(encoding="utf-8")
    for label in [
        "儀表板首頁",
        "城市熱點地圖",
        "城市資料總控台",
        "資料來源",
        "方法論",
        "健康檢查",
    ]:
        assert label in content


def test_homepage_keeps_public_dashboard_sections() -> None:
    content = (DASHBOARD / "index.html").read_text(encoding="utf-8")
    assert "嘉義市城市問題儀表板" in content
    assert "原型案件數" in content
    assert "議題排行" in content
    assert "Top 3 熱點行動建議" in content
    assert "prototype dashboard" in content


def test_map_page_reads_like_public_hotspot_dashboard() -> None:
    content = (DASHBOARD / "map.html").read_text(encoding="utf-8")
    assert "城市熱點地圖" in content
    assert "熱點排行" in content
    assert "Top 3 熱點行動建議" in content


def test_command_center_reads_like_public_control_room() -> None:
    content = (DASHBOARD / "command-center.html").read_text(encoding="utf-8")
    assert "嘉義市城市資料總控台" in content
    assert "目前可用資料" in content
    assert "目前可用頁面" in content
    assert "資料接入狀態" in content


def test_sources_page_uses_public_readable_language() -> None:
    content = (DASHBOARD / "sources.html").read_text(encoding="utf-8")
    assert "資料來源" in content
    assert "prototype" in content
    assert "官方資料來源" in content
    assert "no live crawler" in content


def test_methodology_page_explains_prototype_and_formal_data() -> None:
    content = (DASHBOARD / "methodology.html").read_text(encoding="utf-8")
    assert "城市故障分析方法論" in content
    assert "prototype data" in content
    assert "正式資料" in content
