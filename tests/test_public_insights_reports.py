from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / 'dashboard'


def read_page(name: str) -> str:
    return (DASHBOARD / name).read_text(encoding='utf-8')


def test_insights_page_is_public_readable() -> None:
    content = read_page('insights.html')
    assert '城市洞察分析' in content
    assert '這頁怎麼看' in content
    assert '本週城市觀察摘要' in content
    assert '議題趨勢原型' in content
    assert '優先補資料清單' in content
    assert '交通停車' in content
    assert '文化路商圈' in content
    assert 'prototype dashboard' in content
    assert './index.html' in content
    assert './map.html' in content
    assert './reports.html' in content


def test_reports_page_is_public_readable() -> None:
    content = read_page('reports.html')
    assert '城市週報' in content
    assert '本週城市觀察' in content
    assert '週報會包含什麼' in content
    assert '正式週報上線前的準備' in content
    assert '週報列表' in content
    assert '交通停車仍是第一優先' in content
    assert 'prototype dashboard' in content
    assert './index.html' in content
    assert './map.html' in content
    assert './sources.html' in content
