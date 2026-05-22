from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "config" / "real_data_sources.yml"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "real_data_ingestion_plan.json"


@dataclass(frozen=True)
class SourcePlan:
    source_id: str
    name: str
    category: str
    status: str
    crawl_enabled: bool
    base_url_count: int
    output_raw_dir: str
    output_processed_dir: str
    ready_for_crawl: bool
    blocking_reasons: list[str]


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing manifest: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest must be a YAML mapping.")
    return data


def validate_source(source: dict[str, Any]) -> SourcePlan:
    required = ["id", "name", "category", "status", "crawl_enabled", "output_raw_dir", "output_processed_dir"]
    missing = [key for key in required if key not in source]
    blocking: list[str] = []
    if missing:
        blocking.append(f"missing required fields: {', '.join(missing)}")

    crawl_enabled = bool(source.get("crawl_enabled", False))
    base_urls = source.get("base_urls") or []
    if not isinstance(base_urls, list):
        blocking.append("base_urls must be a list")
        base_urls = []

    if not crawl_enabled:
        blocking.append("crawl_enabled is false; manual review required before crawling")
    if not base_urls:
        blocking.append("base_urls is empty; no reviewed public source URL configured")
    if source.get("status") not in {"ready_for_crawl", "reviewed_public_source"}:
        blocking.append("source status is not ready_for_crawl or reviewed_public_source")

    return SourcePlan(
        source_id=str(source.get("id", "unknown")),
        name=str(source.get("name", "unknown")),
        category=str(source.get("category", "unknown")),
        status=str(source.get("status", "unknown")),
        crawl_enabled=crawl_enabled,
        base_url_count=len(base_urls),
        output_raw_dir=str(source.get("output_raw_dir", "")),
        output_processed_dir=str(source.get("output_processed_dir", "")),
        ready_for_crawl=not blocking,
        blocking_reasons=blocking,
    )


def build_plan(manifest: dict[str, Any]) -> dict[str, Any]:
    sources = manifest.get("sources") or []
    if not isinstance(sources, list):
        raise ValueError("manifest.sources must be a list")

    plans = [validate_source(source) for source in sources]
    ready = [plan for plan in plans if plan.ready_for_crawl]
    blocked = [plan for plan in plans if not plan.ready_for_crawl]

    return {
        "plan_id": "real-data-ingestion-plan",
        "public_use_status": "internal_ingestion_plan",
        "manual_review_required": True,
        "no_auto_publish": True,
        "source_count": len(plans),
        "ready_source_count": len(ready),
        "blocked_source_count": len(blocked),
        "sources": [plan.__dict__ for plan in plans],
        "next_actions": [
            "Review official source URLs and terms before enabling any crawler.",
            "Set crawl_enabled to true only after human review.",
            "Keep raw crawled data internal until privacy and license review is complete.",
            "Build source-specific fetchers only after the manifest entry is ready_for_crawl.",
        ],
    }


def write_plan(plan: dict[str, Any], output: Path = DEFAULT_OUTPUT) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    manifest = load_manifest()
    plan = build_plan(manifest)
    write_plan(plan)
    print(f"Wrote {DEFAULT_OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
