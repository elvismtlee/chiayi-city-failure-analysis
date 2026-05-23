import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / 'dashboard' / 'data' / 'home_visible_mvp_summary.json'


def test_home_visible_mvp_summary_values() -> None:
    data = json.loads(SUMMARY.read_text(encoding='utf-8'))
    kpis = data['visible_kpis']
    assert data['public_use_status'] == 'internal_visible_mvp_home_summary'
    assert data['no_live_crawler'] is True
    assert data['manual_review_required'] is True
    assert data['no_auto_publish'] is True
    assert data['no_personal_data'] is True
    assert data['crawler_execution_allowed'] is False
    assert data['engineering_review_allowed_count'] == 0
    assert kpis['official_url_inventory_count'] == 29
    assert kpis['top10_review_tasks_count'] == 10
    assert kpis['day1_task_count'] == 3
    assert kpis['day1_estimated_minutes'] == 90
    assert kpis['patch_draft_count'] == 10
    assert kpis['sample_result_count'] == 3
    assert kpis['manual_review_form_count'] == 3
    assert kpis['health_status'] == 'ok'
