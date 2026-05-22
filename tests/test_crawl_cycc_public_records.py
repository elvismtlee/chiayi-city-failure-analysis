import json
import subprocess
import sys
from pathlib import Path

from scripts.crawl_cycc_public_records import (
    build_report,
    load_config,
    run_crawl,
    validate_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "cycc_public_records.yml"


def test_cycc_public_record_config_is_safe_and_scoped() -> None:
    config = load_config(CONFIG)

    assert config["public_use_status"] == "internal_cycc_public_records_config"
    assert config["manual_review_required"] is True
    assert config["no_auto_publish"] is True
    assert config["no_personal_data"] is True
    assert config["crawl_scope"] == "metadata_only"
    assert set(config["sources"].keys()) == {"cycc"}

    source = config["sources"]["cycc"]
    assert set(source["targets"].keys()) == {"minutes", "question_videos"}
    for target in source["targets"].values():
        assert "cycc.gov.tw" in target["url"]


def test_validate_config_accepts_reviewed_public_cycc_source() -> None:
    source = validate_config(load_config(CONFIG))

    assert source["source_id"] == "CYCC_PUBLIC_RECORDS"
    assert source["review_status"] == "reviewed_public_source"
    assert source["crawl_enabled"] is True
    assert source["base_urls"]
    assert set(source["targets"].keys()) == {"minutes", "question_videos"}


def test_build_report_keeps_internal_manual_review_flags() -> None:
    source = validate_config(load_config(CONFIG))
    report = build_report(
        {"cycc_minutes_metadata.csv": 2, "cycc_question_video_metadata.csv": 3},
        source,
        CONFIG,
        ROOT / "data" / "raw",
    )

    assert report["public_use_status"] == "internal_crawl_report"
    assert report["manual_review_required"] is True
    assert report["no_auto_publish"] is True
    assert report["no_personal_data"] is True
    assert report["crawl_scope"] == "metadata_only"
    assert len(report["output_files"]) == 2


def test_run_crawl_writes_report_without_live_network(tmp_path: Path) -> None:
    config_path = tmp_path / "cycc_public_records.yml"
    config_path.write_text(CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    output_dir = tmp_path / "raw"
    report_path = tmp_path / "processed" / "cycc_public_records_crawl_report.json"

    class FakeCrawler:
        def __init__(self, config_path: Path, output_dir: Path) -> None:
            self.config_path = config_path
            self.output_dir = output_dir

        def run(self) -> dict[str, int]:
            return {
                "cycc_minutes_metadata.csv": 1,
                "cycc_question_video_metadata.csv": 2,
            }

    report = run_crawl(
        config_path=config_path,
        output_dir=output_dir,
        report_path=report_path,
        crawler_cls=FakeCrawler,
    )

    assert report_path.exists()
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["source_name"] == "嘉義市議會公開資料"
    assert payload["manual_review_required"] is True
    assert payload["no_auto_publish"] is True
    assert payload["output_dir"].endswith("/raw")
    assert {item["record_count"] for item in payload["output_files"]} == {1, 2}


def test_script_can_be_invoked_directly_for_help() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/crawl_cycc_public_records.py", "--help"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "Run CYCC public records metadata crawler" in result.stdout
