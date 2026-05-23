import json
from pathlib import Path

from scripts.build_open_data_top10_review_tasks import build_open_data_top10_review_tasks

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'dashboard' / 'data' / 'open_data_top10_review_tasks.json'


def test_build_open_data_top10_review_tasks() -> None:
    payload = build_open_data_top10_review_tasks()
    data = json.loads(OUTPUT.read_text(encoding='utf-8'))
    assert data['public_use_status'] == 'internal_top10_review_tasks'
    assert data['source_report_count'] == 29
    assert data['total_count'] == 10
    assert data['no_live_crawler'] is True
    assert data['manual_review_required'] is True
    assert data['no_auto_publish'] is True
    assert data['no_personal_data'] is True
    assert payload['total_count'] == data['total_count']
    for task in data['tasks']:
        assert task['review_status'] == 'not_started'
        assert task['no_live_crawler'] is True
        assert len(task['review_steps']) >= 5
        assert len(task['acceptance_criteria']) >= 5
        assert task['readiness_level'] != 'blocked'
