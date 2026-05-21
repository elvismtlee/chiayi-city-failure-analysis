from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPRINT_STATUS = ROOT / "docs" / "sprint_status_2026-05-21.md"


def test_sprint_status_exists() -> None:
    assert SPRINT_STATUS.exists()


def test_sprint_status_mentions_completed_key_issues() -> None:
    content = SPRINT_STATUS.read_text(encoding="utf-8")
    for issue in ["#6", "#11", "#12", "#13", "#18", "#20"]:
        assert issue in content


def test_sprint_status_mentions_next_issue_trend_work() -> None:
    content = SPRINT_STATUS.read_text(encoding="utf-8")
    for phrase in [
        "#7｜建立 issue trend analyzer",
        "scripts/build_issue_trends.py",
        "dashboard/data/issue_trends.json",
    ]:
        assert phrase in content


def test_sprint_status_keeps_safety_principles() -> None:
    content = SPRINT_STATUS.read_text(encoding="utf-8")
    for phrase in [
        "沒有 token / secret / credential",
        "沒有敏感個資欄位",
        "不要只看 Actions 綠燈",
        "不使用民調、支持度調查",
    ]:
        assert phrase in content
