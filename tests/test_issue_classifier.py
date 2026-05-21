from src.classifiers.issue_classifier import (
    REQUIRED_OUTPUT_FIELDS,
    TAXONOMY_CODES,
    classify,
    classify_record,
)


def test_classify_record_outputs_required_fields() -> None:
    record = {
        "source_id": "CYCC_QUESTION_VIDEO",
        "video_title": "市場周邊停車與人行動線質詢",
        "video_url": "https://www.youtube.com/embed/test",
        "council_term": "第十屆",
        "session_name": "第七次定期會",
        "topic_guess": "交通",
    }

    result = classify_record(record)

    assert list(result) == REQUIRED_OUTPUT_FIELDS
    assert result["primary_issue"] in TAXONOMY_CODES
    assert result["primary_issue"] == "traffic"
    assert "market" in result["secondary_issues"]
    assert "parking" in result["secondary_tags"]
    assert result["confidence"] >= 0.65
    assert result["review_status"] == "unreviewed"


def test_classify_record_marks_low_confidence_as_uncertain() -> None:
    record = {
        "source_id": "CYCC_QUESTION_VIDEO",
        "video_title": "第十屆 第七次定期會 質詢影音 jM3_3wA9dH0",
        "video_url": "https://www.youtube.com/embed/jM3_3wA9dH0",
        "council_term": "第十屆",
        "session_name": "第七次定期會",
        "topic_guess": "其他",
    }

    result = classify_record(record)

    assert result["primary_issue"] == "other"
    assert result["confidence"] < 0.65
    assert result["review_status"] == "uncertain"
    assert result["secondary_issues"] == []
    assert result["secondary_tags"] == []


def test_classify_record_uses_taxonomy_codes_and_neutral_language() -> None:
    result = classify_record({"video_title": "公園照明與公共設施安全質詢"})

    assert result["primary_issue"] in TAXONOMY_CODES
    assert result["summary"]
    assert result["recommended_action"]
    assert "責任" not in result["summary"]
    assert "指控" not in result["summary"]


def test_classify_keeps_legacy_text_interface() -> None:
    assert classify("市場周邊停車問題") == "交通"
    assert classify("沒有足夠分類線索") == "其他"
