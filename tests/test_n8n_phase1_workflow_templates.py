import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "automation" / "n8n" / "phase1_workflow_templates.json"

FORBIDDEN_SECRET_TERMS = [
    "ghp_",
    "github_pat_",
    "sk-",
    "token_value",
    "secret_value",
    "password",
    "private_key",
]


def load_template():
    return json.loads(TEMPLATE.read_text(encoding="utf-8"))


def test_n8n_phase1_workflow_template_exists_and_parses() -> None:
    assert TEMPLATE.exists()
    data = load_template()
    assert data["version"] == "1.0"
    assert isinstance(data["workflows"], list)
    assert data["workflows"]


def test_n8n_phase1_template_contains_required_workflows() -> None:
    workflows = {item["id"] for item in load_template()["workflows"]}
    assert "CYFA-WF-001-Weekly-Data-Update" in workflows
    assert "CYFA-WF-003-Weekly-Report-Draft" in workflows
    assert "CYFA-WF-005-Update-Failure-Alert" in workflows


def test_n8n_phase1_template_keeps_safety_boundaries() -> None:
    data = load_template()
    safety_text = "\n".join(data["safety_boundaries"])
    for phrase in [
        "不自動發文",
        "不公開個人表單資料",
        "不把 GitHub token 寫入 repo",
        "不自動寄出對外 email",
        "需要人工確認",
    ]:
        assert phrase in safety_text


def test_n8n_phase1_template_has_no_obvious_secrets() -> None:
    raw = TEMPLATE.read_text(encoding="utf-8").lower()
    for term in FORBIDDEN_SECRET_TERMS:
        assert term.lower() not in raw


def test_weekly_data_update_lists_required_dashboard_outputs() -> None:
    data = load_template()
    workflow = next(
        item for item in data["workflows"] if item["id"] == "CYFA-WF-001-Weekly-Data-Update"
    )
    for path in [
        "dashboard/data/dashboard_summary.json",
        "dashboard/data/issue_ranking.json",
        "dashboard/data/hotspots.json",
        "dashboard/data/data_sources.json",
    ]:
        assert path in workflow["required_outputs"]
