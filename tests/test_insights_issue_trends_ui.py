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
    assert "TREND_WINDOWS" in script
    assert "days: 7" in script
    assert "days: 30" in script
    assert "days: 90" in script
    assert 'data-window-days="${group.days}"' in script


def test_issue_trends_ui_has_named_time_window_sections() -> None:
    script = read_dashboard_file("insights.js")
    for text in [
        "最近 7 天｜短期熱點",
        "最近 30 天｜中期變化",
        "最近 90 天｜長期趨勢",
        "適合觀察最近快速升高、需要立即注意的議題",
        "適合觀察一個月內逐漸累積的地方議題",
        "適合觀察較長時間持續存在的結構性問題",
    ]:
        assert text in script


def test_issue_trends_ui_has_jump_links_and_anchors() -> None:
    html = read_dashboard_file("insights.html")
    script = read_dashboard_file("insights.js")

    for anchor in ["trend-7", "trend-30", "trend-90"]:
        assert f'href="#{anchor}"' in html
        assert anchor in script

    for css_class in [
        "trend-jump-nav",
        "trend-jump-link",
        "trend-group",
        "trend-group-header",
        "trend-group-7",
        "trend-group-30",
        "trend-group-90",
        "trend-group-note",
        "trend-empty",
    ]:
        assert css_class in html


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


def test_issue_trends_ui_keeps_chinese_title_helper() -> None:
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
