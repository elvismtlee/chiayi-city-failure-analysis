import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEALTH = ROOT / 'dashboard' / 'data' / 'dashboard_health_check.json'


def test_health_check_marks_evidence_pack_valid() -> None:
    data = json.loads(HEALTH.read_text(encoding='utf-8'))
    checked = {item['file']: item for item in data['checked_files']}
    evidence = checked['dashboard/data/open_data_review_evidence_pack.json']
    assert evidence['exists'] is True
    assert evidence['empty'] is False
    assert evidence['valid_json'] is True
    assert 'dashboard/data/open_data_review_evidence_pack.json' not in data['invalid_json_files']
    assert data['warnings'] == []
    assert data['status'] == 'ok'
