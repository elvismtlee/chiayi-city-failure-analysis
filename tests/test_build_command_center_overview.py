import json
from pathlib import Path

from scripts import build_command_center_overview as builder


def test_build_command_center_overview_creates_expected_fields(tmp_path: Path) -> None:
    data_dir = tmp_path / "dashboard" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "cycc_minutes_review_queue.json").write_text('[{"id": "m1"}]', encoding="utf-8")

    result = builder.build_overview(tmp_path)

    assert isinstance(result["pipeline_status"], list)
    assert "key_counts" in result
    assert isinstance(result["warnings"], list)
    assert result["public_use_status"] == "internal_command_center"
    assert "民調" not in json.dumps(result, ensure_ascii=False)
    assert "支持度調查" not in json.dumps(result, ensure_ascii=False)


def test_build_command_center_overview_missing_files_do_not_crash(tmp_path: Path) -> None:
    result = builder.build_overview(tmp_path)

    assert isinstance(result["warnings"], list)
    assert any(item["status"] == "missing" for item in result["pipeline_status"])
