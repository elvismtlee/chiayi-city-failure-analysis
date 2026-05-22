from __future__ import annotations

import socket

from scripts.parse_cycc_minutes_sample import (
    REQUIRED_FIELDS,
    SENSITIVE_FIELDS,
    parse_all_fixtures,
    parse_html_fixture,
    parse_text_fixture,
    stable_raw_hash,
)


EXPECTED_STATUS = "parsed_from_fixture"
EXPECTED_REVIEW_STATUS = "unreviewed"


def assert_minutes_record(record: dict) -> None:
    for field in REQUIRED_FIELDS:
        assert field in record, f"missing required field: {field}"

    assert record["parser_status"] == EXPECTED_STATUS
    assert record["review_status"] == EXPECTED_REVIEW_STATUS
    assert isinstance(record["issue_keywords"], list)
    assert record["issue_keywords"]
    assert isinstance(record["raw_hash"], str)
    assert len(record["raw_hash"]) == 64

    leaked_fields = SENSITIVE_FIELDS.intersection(record.keys())
    assert not leaked_fields, f"sensitive fields leaked: {sorted(leaked_fields)}"


def test_parse_html_fixture() -> None:
    record = parse_html_fixture()

    assert_minutes_record(record)
    assert record["source_id"] == "CYCC_MINUTES_FIXTURE_HTML"
    assert record["meeting_name"] == "嘉義市議會第 11 屆第 3 次定期會模擬紀錄"
    assert record["meeting_date"] == "2026-05-01"
    assert record["councilor_name"] == "測試議員甲"
    assert record["department"] == "交通處"
    assert "道路安全" in record["issue_keywords"]
    assert record["source_url"].endswith("sample.html")
    assert "公開會議紀錄內容" in record["raw_text"]
    assert "交通處說明" in record["raw_text"]


def test_parse_text_fixture() -> None:
    record = parse_text_fixture()

    assert_minutes_record(record)
    assert record["source_id"] == "CYCC_MINUTES_FIXTURE_TEXT"
    assert record["meeting_name"] == "嘉義市議會第 11 屆第 4 次定期會模擬紀錄"
    assert record["meeting_date"] == "2026-05-02"
    assert record["councilor_name"] == "測試議員乙"
    assert record["department"] == "建設處"
    assert "排水改善" in record["issue_keywords"]
    assert record["source_url"].endswith("sample.pdf")
    assert "騎樓整平" in record["raw_text"]


def test_required_fields_exist_for_all_fixture_records() -> None:
    records = parse_all_fixtures()

    assert len(records) == 2
    for record in records:
        assert_minutes_record(record)


def test_raw_hash_is_stable() -> None:
    first = parse_html_fixture()
    second = parse_html_fixture()

    assert first["raw_hash"] == second["raw_hash"]
    assert first["raw_hash"] == stable_raw_hash(first)


def test_parser_does_not_output_sensitive_fields() -> None:
    records = parse_all_fixtures()

    for record in records:
        assert not SENSITIVE_FIELDS.intersection(record.keys())


def test_parser_status_and_review_status_are_initial_fixture_values() -> None:
    records = parse_all_fixtures()

    assert {record["parser_status"] for record in records} == {EXPECTED_STATUS}
    assert {record["review_status"] for record in records} == {EXPECTED_REVIEW_STATUS}


def test_issue_keywords_are_lists() -> None:
    records = parse_all_fixtures()

    for record in records:
        assert isinstance(record["issue_keywords"], list)
        assert all(isinstance(keyword, str) for keyword in record["issue_keywords"])


def test_parser_does_not_require_network(monkeypatch) -> None:
    def fail_socket(*args, **kwargs):
        raise AssertionError("network access is not allowed for fixture parser")

    monkeypatch.setattr(socket, "socket", fail_socket)

    records = parse_all_fixtures()
    assert len(records) == 2
