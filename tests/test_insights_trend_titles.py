from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSIGHTS_JS = ROOT / "dashboard" / "insights.js"


def test_insights_trend_cards_use_display_name_for_title() -> None:
    content = INSIGHTS_JS.read_text(encoding="utf-8")
    assert "function issueTrendTitle" in content
    assert "item.display_name" in content
    assert "issueTrendTitle(item)" in content


def test_insights_trend_cards_keep_issue_fallback() -> None:
    content = INSIGHTS_JS.read_text(encoding="utf-8")
    assert "item.issue" in content
    assert "未分類議題" in content
