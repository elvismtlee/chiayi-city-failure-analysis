from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config' / 'open_data_top10_review_tasks_schema.yml'


def test_top10_review_tasks_schema_is_safe() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding='utf-8'))
    assert data['public_use_status'] == 'internal_top10_review_tasks_schema'
    assert data['manual_review_required'] is True
    assert data['no_auto_publish'] is True
    assert data['no_personal_data'] is True
    assert data['no_live_crawler'] is True
    fields = set(data['required_fields'])
    assert 'task_id' in fields
    assert 'review_steps' in fields
    assert 'acceptance_criteria' in fields
    assert 'safety_checklist' in fields
    assert 'next_action' in fields
