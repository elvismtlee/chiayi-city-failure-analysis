from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "automation" / "n8n" / "README.md"


def test_n8n_readme_exists() -> None:
    assert README.exists()


def test_n8n_readme_lists_phase1_workflows() -> None:
    content = README.read_text(encoding="utf-8")
    for workflow in [
        "CYFA-WF-001-Weekly-Data-Update",
        "CYFA-WF-003-Weekly-Report-Draft",
        "CYFA-WF-005-Update-Failure-Alert",
    ]:
        assert workflow in content


def test_n8n_readme_keeps_safety_boundaries() -> None:
    content = README.read_text(encoding="utf-8")
    for phrase in [
        "不自動發文",
        "不公開 Google Drive",
        "不自動寄出對外 email",
        "不公開個人表單資料",
        "不把 GitHub token 寫入 repo",
    ]:
        assert phrase in content


def test_n8n_readme_rejects_polling_language() -> None:
    content = README.read_text(encoding="utf-8")
    assert "不可稱為" in content
    assert "民調" in content
    assert "支持度調查" in content
