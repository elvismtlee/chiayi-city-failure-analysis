import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_build_cycc_metadata_dashboard_data_script_runs() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build_cycc_metadata_dashboard_data.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "CYCC metadata OK: total=141" in result.stdout
