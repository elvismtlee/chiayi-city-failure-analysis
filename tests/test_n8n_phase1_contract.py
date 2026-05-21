from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "n8n_phase1_implementation_contract.md"


def test_n8n_phase1_contract_exists() -> None:
    assert CONTRACT.exists()


def test_n8n_phase1_contract_includes_required_workflows() -> None:
    content = CONTRACT.read_text(encoding="utf-8")
    for workflow in ["WF-001", "WF-003", "WF-005"]:
        assert workflow in content


def test_n8n_phase1_contract_defines_safety_boundaries() -> None:
    content = CONTRACT.read_text(encoding="utf-8")
    for phrase in [
        "不自動發文",
        "不公開個人表單資料",
        "不把 GitHub token 寫入 repo",
        "不自動寄出對外 email",
        "需要人工確認",
    ]:
        assert phrase in content


def test_n8n_phase1_contract_lists_required_dashboard_json() -> None:
    content = CONTRACT.read_text(encoding="utf-8")
    for path in [
        "dashboard/data/dashboard_summary.json",
        "dashboard/data/issue_ranking.json",
        "dashboard/data/hotspots.json",
        "dashboard/data/data_sources.json",
    ]:
        assert path in content
