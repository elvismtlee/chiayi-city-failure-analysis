from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"


def read_dashboard_file(filename: str) -> str:
    return (DASHBOARD_DIR / filename).read_text(encoding="utf-8")


def test_insights_has_trend_window_jump_links() -> None:
    html = read_dashboard_file("insights.html")

    assert "城市洞察分析" in html
    assert "議題趨勢原型" in html
    assert "優先補資料清單" in html
    assert "相關頁面" in html


def test_insights_renders_three_window_sections() -> None:
    script = read_dashboard_file("insights.js")

    assert "TREND_WINDOWS" in script
    assert "groupTrendsByWindow" in script
    assert "days: 7" in script
    assert "days: 30" in script
    assert "days: 90" in script
    assert "id: 'trend-7'" in script
    assert "id: 'trend-30'" in script
    assert "id: 'trend-90'" in script
    assert 'class="trend-group trend-group-${group.days}"' in script
    assert "Number(item.window_days) === window.days" in script


def test_trend_window_titles_notes_and_empty_state_are_present() -> None:
    script = read_dashboard_file("insights.js")

    for phrase in [
        "最近 7 天｜短期熱點",
        "最近 30 天｜中期變化",
        "最近 90 天｜長期趨勢",
        "適合觀察最近快速升高、需要立即注意的議題",
        "適合觀察一個月內逐漸累積的地方議題",
        "適合觀察較長時間持續存在的結構性問題",
        "目前沒有可顯示的趨勢資料",
    ]:
        assert phrase in script


def test_trend_window_css_classes_are_present() -> None:
    script = read_dashboard_file("insights.js")

    for class_name in [
        "trend-group",
        "trend-group-header",
        "trend-group-7",
        "trend-group-30",
        "trend-group-90",
        "trend-group-note",
        "trend-empty",
    ]:
        assert class_name in script


def test_trend_labels_review_status_and_title_helper_are_preserved() -> None:
    script = read_dashboard_file("insights.js")

    assert "function issueTrendTitle" in script
    assert "issueTrendTitle(item)" in script
    assert "item.display_name" in script
    assert "item.issue" in script

    for label in ["上升", "下降", "穩定", "快速升高", "原型資料"]:
        assert label in script


def test_insights_avoids_support_polling_terms() -> None:
    content = read_dashboard_file("insights.html") + read_dashboard_file("insights.js")

    assert "民調" not in content
    assert "支持度調查" not in content
