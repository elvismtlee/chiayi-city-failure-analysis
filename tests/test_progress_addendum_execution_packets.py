from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'docs' / 'progress_addendum_20260523_execution_packets.md'


def test_execution_packets_progress_note() -> None:
    content = DOC.read_text(encoding='utf-8')
    assert 'PR #178' in content
    assert 'open-data-manual-review-packets.html' in content
    assert 'open_data_manual_review_execution_packets.json' in content
    assert 'day_1_packet.md' in content
    assert 'day_2_packet.md' in content
    assert 'day_3_packet.md' in content
    assert 'total_tasks：10' in content
    assert 'feat/open-data-manual-review-result-patch-drafts' in content
