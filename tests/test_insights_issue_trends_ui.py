from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"


def read_dashboard_file(filename: str) -> str:
    return (DASHBOARD_DIR / filename).read_text(encoding="utf-8")


def test_insights_page_is_public_readable() -> None:
    html = read_dashboard_file("insights.html")
    assert "城市洞察分析" in html
    assert "本週城市觀察摘要" in html
    assert "議題趨勢原型" in html
    assert "優先補資料清單" in html
    assert "prototype dashboard" in html
    assert "./index.html" in html
    assert "./map.html" in html
    assert "./reports.html" in html


def test_insights_page_mentions_key_issue_groups() -> None:
    html = read_dashboard_file("insights.html")
    for text in ["交通停車", "文化路商圈", "市場周邊", "通學安全", "正式資料"]:
        assert text in html


def test_insights_avoids_support_polling_terms() -> None:
    content = read_dashboard_file("insights.html")
    assert "支持度調查" not in content
    assert "民調" not in content


def test_insights_script_still_exists_for_legacy_data_renderers() -> None:
    script = read_dashboard_file("insights.js")
    for path in [
        "./data/ai_issue_summary.json",
        "./data/urban_failure_scores.json",
        "./data/department_performance.json",
        "./data/councilor_issue_analysis.json",
        "./data/issue_trends.json",
    ]:
        assert path in script
