import pytest

from scripts.build_transcript_review_queue import (
    build_queue,
    detect_video_platform,
    extract_video_id,
    queue_id,
    transcript_priority,
)


SAMPLE_ROW = {
    "source_id": "CYCC_QUESTION_VIDEO",
    "councilor_name": "",
    "council_term": "第十屆",
    "session_name": "第七次定期會",
    "video_title": "第十屆 第七次定期會 質詢影音 jM3_3wA9dH0",
    "video_url": "https://www.youtube.com/embed/jM3_3wA9dH0",
    "meeting_date": "",
    "topic_guess": "其他",
    "crawled_at": "2026-05-21T07:26:08+00:00",
    "raw_hash": "b7658588fe7656a8e4703408d75b4bd8489e25608352a0c4e6d7017c72d9e942",
}

REQUIRED_FIELDS = [
    "queue_id",
    "source_id",
    "councilor_name",
    "council_term",
    "session_name",
    "video_title",
    "video_url",
    "video_platform",
    "video_id",
    "meeting_date",
    "topic_guess",
    "raw_hash",
    "transcript_status",
    "review_status",
    "priority",
    "needs_metadata_review",
    "recommended_action",
    "notes",
]

SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id"}


def test_extract_video_id_from_youtube_embed_url() -> None:
    assert extract_video_id("https://www.youtube.com/embed/jM3_3wA9dH0") == "jM3_3wA9dH0"


def test_detect_video_platform() -> None:
    assert detect_video_platform("https://www.youtube.com/embed/jM3_3wA9dH0") == "youtube"
    assert detect_video_platform("") == "missing_url"
    assert detect_video_platform("https://example.com/video") == "unknown_video_url"


def test_transcript_priority_flags_missing_metadata() -> None:
    assert transcript_priority(SAMPLE_ROW) == "medium"
    missing_url = {**SAMPLE_ROW, "video_url": ""}
    assert transcript_priority(missing_url) == "needs_metadata_review"
    complete = {**SAMPLE_ROW, "councilor_name": "王小明", "meeting_date": "2026-05-21"}
    assert transcript_priority(complete) == "normal"


def test_queue_id_uses_raw_hash_prefix() -> None:
    assert queue_id(SAMPLE_ROW, 0) == "cycc-transcript-b7658588fe76"


def test_build_queue_creates_required_fields() -> None:
    queue = build_queue([SAMPLE_ROW])
    assert len(queue) == 1
    item = queue[0]
    for field in REQUIRED_FIELDS:
        assert field in item, f"missing field: {field}"
    assert item["video_platform"] == "youtube"
    assert item["video_id"] == "jM3_3wA9dH0"
    assert item["transcript_status"] == "not_started"
    assert item["review_status"] == "unreviewed"
    assert item["recommended_action"] == "manual_transcript_or_asr_review"
    assert item["needs_metadata_review"] is True


def test_build_queue_does_not_add_sensitive_fields() -> None:
    item = build_queue([SAMPLE_ROW])[0]
    lowered = {str(key).lower() for key in item.keys()}
    assert not lowered & SENSITIVE_FIELDS


def test_build_queue_notes_do_not_claim_transcription_started() -> None:
    item = build_queue([SAMPLE_ROW])[0]
    assert "不下載影音" in item["notes"]
    assert "不呼叫 Whisper" in item["notes"]
    assert item["transcript_status"] == "not_started"


def test_build_queue_rejects_sensitive_output_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    from scripts import build_transcript_review_queue as module

    original_keys = module.SENSITIVE_KEYS
    monkeypatch.setattr(module, "SENSITIVE_KEYS", original_keys | {"queue_id"})
    with pytest.raises(ValueError):
        module.build_queue([SAMPLE_ROW])
