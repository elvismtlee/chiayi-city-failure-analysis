from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_daily_execution_builder_exists() -> None:
    assert (ROOT / "scripts" / "build_daily_execution_list.py").exists()


def test_daily_execution_data_exists() -> None:
    assert (ROOT / "dashboard" / "data" / "daily_execution_list.json").exists()
