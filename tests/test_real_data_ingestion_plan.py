from pathlib import Path

from scripts.plan_real_data_ingestion import build_plan, load_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "real_data_sources.yml"


def test_manifest_requires_manual_review() -> None:
    manifest = load_manifest(MANIFEST)
    assert manifest["public_use_status"] == "internal_source_manifest"
    assert manifest["manual_review_required"] is True
    assert manifest["no_auto_publish"] is True
    assert manifest["timezone"] == "Asia/Taipei"


def test_sources_start_disabled() -> None:
    manifest = load_manifest(MANIFEST)
    sources = manifest["sources"]
    assert sources
    for source in sources:
        assert source["crawl_enabled"] is False
        assert source["base_urls"] == []
        assert source["output_raw_dir"].startswith("data/raw/")
        assert source["output_processed_dir"].startswith("data/processed/")


def test_plan_blocks_sources_without_reviewed_urls() -> None:
    plan = build_plan(load_manifest(MANIFEST))
    assert plan["public_use_status"] == "internal_ingestion_plan"
    assert plan["manual_review_required"] is True
    assert plan["source_count"] >= 3
    assert plan["ready_source_count"] == 0
    assert plan["blocked_source_count"] == plan["source_count"]
