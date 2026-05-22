from pathlib import Path

from scripts import build_weekly_system_report as builder


def test_build_weekly_system_report_creates_expected_fields(tmp_path: Path) -> None:
    data_dir = tmp_path / "dashboard" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "command_center_overview.json").write_text(
        '{"pipeline_status": [{"status": "available"}], "review_backlog": {"public_review": 1}}',
        encoding="utf-8",
    )
    (data_dir / "dashboard_health_check.json").write_text('{"status": "ok"}', encoding="utf-8")

    result = builder.build_weekly_report(tmp_path)

    assert isinstance(result["recommended_next_actions"], list)
    assert isinstance(result["warnings"], list)
    assert result["system_status"] in {"ok", "needs_attention", "incomplete"}
    assert result["public_use_status"] == "internal_weekly_system_report"


def test_build_weekly_system_report_missing_files_do_not_crash(tmp_path: Path) -> None:
    result = builder.build_weekly_report(tmp_path)

    assert result["system_status"] == "incomplete"
    assert result["warnings"]
