import json
from pathlib import Path

from scripts import build_cycc_metadata_dashboard_data


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_build_cycc_metadata_dashboard_data_writes_expected_files(tmp_path: Path, monkeypatch) -> None:
    output_dir = tmp_path / "dashboard-data"
    minutes_output = output_dir / "cycc_minutes_metadata.json"
    videos_output = output_dir / "cycc_question_video_metadata.json"

    monkeypatch.setattr(build_cycc_metadata_dashboard_data, "DASHBOARD_DATA_DIR", output_dir)
    monkeypatch.setattr(build_cycc_metadata_dashboard_data, "MINUTES_OUTPUT", minutes_output)
    monkeypatch.setattr(build_cycc_metadata_dashboard_data, "VIDEOS_OUTPUT", videos_output)

    build_cycc_metadata_dashboard_data.write_dashboard_metadata()

    assert minutes_output.exists()
    assert videos_output.exists()

    minutes = read_json(minutes_output)
    videos = read_json(videos_output)
    assert minutes["total_count"] == 10
    assert videos["total_count"] == 131
    assert minutes["total_count"] + videos["total_count"] == 141


def test_build_cycc_metadata_dashboard_data_keeps_internal_review_flags() -> None:
    minutes, videos = build_cycc_metadata_dashboard_data.build_dashboard_metadata()

    for payload in (minutes, videos):
        assert payload["public_use_status"] == "internal_metadata_table"
        assert payload["manual_review_required"] is True
        assert payload["no_auto_publish"] is True
        assert payload["metadata_only"] is True
        assert payload["generated_at"].endswith("+08:00")
        assert all("\\" not in item["source_url"] for item in payload["items"] if item["source_url"])
