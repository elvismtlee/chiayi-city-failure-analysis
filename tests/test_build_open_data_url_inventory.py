import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_open_data_builder_runs() -> None:
    result = subprocess.run(
        [sys.executable, 'scripts/build_open_data_url_inventory.py'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    data = json.loads((ROOT / 'dashboard' / 'data' / 'open_data_url_inventory.json').read_text(encoding='utf-8'))
    assert data['public_use_status'] == 'internal_url_inventory'
    assert data['total_count'] >= 20
    assert 'traffic_parking' in data['topic_groups']
    assert 'complaints_service' in data['topic_groups']
