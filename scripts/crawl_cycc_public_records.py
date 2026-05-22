from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

from src.crawlers.cycc_metadata_crawler import CYCCMetadataCrawler


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "cycc_public_records.yml"
DEFAULT_OUTPUT_DIR = ROOT / "data" / "raw"
DEFAULT_REPORT_PATH = ROOT / "data" / "processed" / "cycc_public_records_crawl_report.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
ALLOWED_HOST_SNIPPETS = ("cycc.gov.tw", "cycc.digital.th.gov.tw")
ALLOWED_TARGETS = {"minutes", "question_videos"}


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def to_posix_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return path.as_posix()


def load_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing config: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("CYCC public records config must be a YAML mapping.")
    return data


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    if config.get("public_use_status") != "internal_cycc_public_records_config":
        raise ValueError("public_use_status must remain internal_cycc_public_records_config.")
    if config.get("manual_review_required") is not True:
        raise ValueError("manual_review_required must remain true.")
    if config.get("no_auto_publish") is not True:
        raise ValueError("no_auto_publish must remain true.")
    if config.get("no_personal_data") is not True:
        raise ValueError("no_personal_data must remain true.")
    if config.get("crawl_scope") != "metadata_only":
        raise ValueError("crawl_scope must remain metadata_only.")

    sources = config.get("sources")
    if not isinstance(sources, dict) or set(sources.keys()) != {"cycc"}:
        raise ValueError("Only the cycc public source is allowed in this crawler config.")

    source = sources["cycc"]
    if source.get("review_status") != "reviewed_public_source":
        raise ValueError("CYCC source must remain reviewed_public_source before crawling.")
    if source.get("crawl_enabled") is not True:
        raise ValueError("CYCC source must be explicitly enabled for manual crawler runs.")

    base_urls = source.get("base_urls")
    if not isinstance(base_urls, list) or not base_urls:
        raise ValueError("CYCC source must declare reviewed public base_urls.")
    for url in base_urls:
        if not isinstance(url, str) or not any(host in url for host in ALLOWED_HOST_SNIPPETS):
            raise ValueError("CYCC base_urls must stay within reviewed public CYCC domains.")

    targets = source.get("targets")
    if not isinstance(targets, dict) or set(targets.keys()) != ALLOWED_TARGETS:
        raise ValueError("CYCC crawler may only target minutes and question_videos metadata.")
    for name, target in targets.items():
        if not isinstance(target, dict):
            raise ValueError(f"Target {name} must be a mapping.")
        url = str(target.get("url", ""))
        if not url or not any(host in url for host in ALLOWED_HOST_SNIPPETS):
            raise ValueError(f"Target {name} must use a reviewed public CYCC URL.")

    return source


def build_report(
    result: dict[str, int],
    source: dict[str, Any],
    config_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    return {
        "report_id": f"cycc-public-records-{datetime.now(TAIPEI_TZ).strftime('%Y%m%d%H%M%S')}",
        "generated_at": now_iso(),
        "public_use_status": "internal_crawl_report",
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "source_id": source["source_id"],
        "source_name": source["name"],
        "review_status": source["review_status"],
        "crawl_scope": "metadata_only",
        "config_file": to_posix_path(config_path),
        "output_dir": to_posix_path(output_dir),
        "output_files": [
            {
                "file": to_posix_path(output_dir / filename),
                "record_count": count,
            }
            for filename, count in sorted(result.items())
        ],
        "notes": [
            "internal crawler output / needs human review / manual publishing only",
            "CYCC public metadata only; no 1999 private complaint full text.",
            "Do not publish crawled outputs without human review.",
        ],
    }


def write_report(report: dict[str, Any], report_path: Path = DEFAULT_REPORT_PATH) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_crawl(
    config_path: Path = DEFAULT_CONFIG,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    report_path: Path = DEFAULT_REPORT_PATH,
    crawler_cls: type[CYCCMetadataCrawler] = CYCCMetadataCrawler,
) -> dict[str, Any]:
    config = load_config(config_path)
    source = validate_config(config)
    crawler = crawler_cls(config_path=config_path, output_dir=output_dir)
    result = crawler.run()
    report = build_report(result, source, config_path, output_dir)
    write_report(report, report_path)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl reviewed CYCC public metadata into internal raw CSV files.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--report-path", default=str(DEFAULT_REPORT_PATH))
    args = parser.parse_args()

    report = run_crawl(
        config_path=Path(args.config),
        output_dir=Path(args.output_dir),
        report_path=Path(args.report_path),
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
