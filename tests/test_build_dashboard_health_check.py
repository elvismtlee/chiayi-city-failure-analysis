from pathlib import Path

from scripts import build_dashboard_health_check as builder


def test_build_dashboard_health_check_creates_expected_fields(tmp_path: Path) -> None:
    data_dir = tmp_path / "dashboard" / "data"
    data_dir.mkdir(parents=True)
    (data_dir / "site_map.json").write_text('{"pages": []}', encoding="utf-8")

    result = builder.build_health_check(tmp_path)

    assert isinstance(result["checked_files"], list)
    assert isinstance(result["missing_files"], list)
    assert isinstance(result["empty_files"], list)
    assert isinstance(result["invalid_json_files"], list)
    assert result["status"] in {"ok", "needs_attention"}
    assert result["public_use_status"] == "internal_health_check"


def test_build_dashboard_health_check_missing_files_do_not_crash(tmp_path: Path) -> None:
    result = builder.build_health_check(tmp_path)

    assert result["status"] == "needs_attention"
    assert result["missing_files"]
