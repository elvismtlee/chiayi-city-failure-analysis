from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DIR = ROOT / "dashboard"


def read_dashboard_file(filename: str) -> str:
    return (DASHBOARD_DIR / filename).read_text(encoding="utf-8")


def test_insights_loads_issue_trends_json() -> None:
    html = read_dashboard_file("insights.html")
    script = read_dashboard_file("insights.js")

    assert './insights.js' in html
    assert "./data/issue_trends.json" in script
    assert 'data-render="trends"' in html


def test_issue_trends_ui_groups_by_window_days() -> None:
    script = read_dashboard_file("insights.js")

    assert "groupTrendsByWindow" in script
    assert "[7, 30, 90]" in script
    assert 'data-window-days="${group.days}"' in script
    assert "${group.days} 天" in script


def test_issue_trends_ui_renders_required_fields() -> None:
    script = read_dashboard_file("insights.js")

    for field in [
        "display_name",
        "current_count",
        "previous_count",
        "change_percent",
        "trend",
        "confidence",
        "review_status",
        "summary",
        "recommended_action",
    ]:
        assert field in script

    for label in ["上升", "下降", "穩定", "快速升高", "原型資料"]:
        assert label in script


def test_issue_trends_ui_uses_chinese_title_helper() -> None:
    script = read_dashboard_file("insights.js")
    assert "function issueTrendTitle" in script
    assert "item.display_name" in script
    assert "issueTrendTitle(item)" in script
    assert "未分類議題" in script


def test_issue_trends_ui_discloses_prototype_data_limits() -> None:
    html = read_dashboard_file("insights.html")

    for phrase in [
        "metadata / sample 階段",
        "不代表正式調查結果",
        "不代表完整民意結論",
        "持續補充資料與人工 review",
    ]:
        assert phrase in html


def test_issue_trends_ui_avoids_support_polling_language() -> None:
    content = read_dashboard_file("insights.html") + read_dashboard_file("insights.js")

    assert "支持度調查" not in content
    assert "民調" not in content


def test_insights_keeps_existing_json_rendering() -> None:
    script = read_dashboard_file("insights.js")

    for path in [
        "./data/ai_issue_summary.json",
        "./data/urban_failure_scores.json",
        "./data/department_performance.json",
        "./data/councilor_issue_analysis.json",
    ]:
        assert path in script

    for renderer in [
        "renderScoreTable(scores)",
        "renderDepartmentCards(departments)",
        "renderCouncilorCards(councilors)",
        "renderList('[data-ai=\"findings\"]'",
        "renderList('[data-ai=\"actions\"]'",
    ]:
        assert renderer in script
