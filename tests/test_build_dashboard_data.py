import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.processors import build_dashboard_data


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_build_dashboard_data_writes_required_json_files(tmp_path: Path, monkeypatch) -> None:
    output_dir = tmp_path / "dashboard-data"
    monkeypatch.setattr(build_dashboard_data, "DASHBOARD_DATA_DIR", output_dir)

    build_dashboard_data.main()

    required_files = [
        "dashboard_summary.json",
        "issue_ranking.json",
        "hotspots.json",
    ]
    for filename in required_files:
        path = output_dir / filename
        assert path.exists()
        data = read_json(path)
        assert data


def test_build_dashboard_data_summary_has_expected_keys(tmp_path: Path, monkeypatch) -> None:
    output_dir = tmp_path / "dashboard-data"
    monkeypatch.setattr(build_dashboard_data, "DASHBOARD_DATA_DIR", output_dir)

    build_dashboard_data.main()

    summary = read_json(output_dir / "dashboard_summary.json")
    for key in ["total_cases", "total_questions", "total_hotspots", "top_issue", "updated_at"]:
        assert key in summary
