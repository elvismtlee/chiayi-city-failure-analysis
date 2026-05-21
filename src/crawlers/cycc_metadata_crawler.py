from __future__ import annotations

import argparse
import csv
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup

try:
    from src.classifiers.issue_classifier import classify
except ImportError:  # pragma: no cover - keeps direct script execution usable
    classify = lambda text: "其他"  # type: ignore[assignment]


MINUTES_COLUMNS = [
    "source_id",
    "title",
    "department",
    "views",
    "updated_at",
    "detail_url",
    "file_url",
    "crawled_at",
    "raw_hash",
]

QUESTION_VIDEO_COLUMNS = [
    "source_id",
    "councilor_name",
    "council_term",
    "session_name",
    "video_title",
    "video_url",
    "meeting_date",
    "topic_guess",
    "crawled_at",
    "raw_hash",
]

DATE_PATTERN = re.compile(r"\d{4}[/-]\d{1,2}[/-]\d{1,2}")
VIEWS_PATTERN = re.compile(r"(?:點閱|瀏覽|人氣|views?)\D*(\d+)", re.IGNORECASE)
SESSION_HEADING_PATTERN = re.compile(r"【([^:：】]+)[:：]([^】]+)】")
FILE_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".odt", ".ods")


@dataclass(frozen=True)
class MetadataTarget:
    source_id: str
    url: str
    output_filename: str


def read_config(config_path: str | Path) -> dict[str, Any]:
    with Path(config_path).open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    if not isinstance(data, dict) or "sources" not in data:
        raise ValueError("config/sources.yml must contain a top-level sources mapping")
    return data


def get_cycc_targets(config: dict[str, Any]) -> dict[str, MetadataTarget]:
    targets = config["sources"]["cycc"]["targets"]
    return {
        "minutes": MetadataTarget(
            source_id="CYCC_MINUTES",
            url=targets["minutes"]["url"],
            output_filename="cycc_minutes_metadata.csv",
        ),
        "question_videos": MetadataTarget(
            source_id="CYCC_QUESTION_VIDEO",
            url=targets["question_videos"]["url"],
            output_filename="cycc_question_video_metadata.csv",
        ),
    }


def make_raw_hash(*parts: object) -> str:
    normalized = "||".join(str(part or "").strip() for part in parts)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def dedupe_by_raw_hash(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique_records: list[dict[str, Any]] = []
    for record in records:
        raw_hash = str(record.get("raw_hash", ""))
        if not raw_hash or raw_hash in seen:
            continue
        seen.add(raw_hash)
        unique_records.append(record)
    return unique_records


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _row_texts(row: Any) -> list[str]:
    return [_clean_text(cell.get_text(" ", strip=True)) for cell in row.find_all(["td", "th"])]


def _find_date(text: str) -> str:
    match = DATE_PATTERN.search(text)
    return match.group(0).replace("/", "-") if match else ""


def _find_views(text: str) -> str:
    labeled = VIEWS_PATTERN.search(text)
    if labeled:
        return labeled.group(1)
    numbers = re.findall(r"\b\d+\b", text)
    return numbers[-1] if numbers else ""


def _looks_like_file_url(url: str) -> bool:
    clean_url = url.split("?", 1)[0].lower()
    return clean_url.endswith(FILE_EXTENSIONS) or "download" in clean_url.lower()


def _first_useful_link(container: Any, base_url: str) -> tuple[str, str, str]:
    detail_url = ""
    file_url = ""
    title = ""
    for link in container.find_all("a", href=True):
        link_text = _clean_text(link.get_text(" ", strip=True))
        href = urljoin(base_url, link["href"])
        if not title and link_text:
            title = link_text
            detail_url = href
        if _looks_like_file_url(href):
            file_url = href
    return title, detail_url, file_url


def _content_scope(soup: BeautifulSoup) -> Any:
    return (
        soup.select_one("#ContentPlaceHolder1_UpdatePanel1")
        or soup.select_one("main")
        or soup.select_one(".contentsA01")
        or soup
    )


def parse_minutes_metadata(html: str, list_url: str, crawled_at: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    records: list[dict[str, Any]] = []
    containers = soup.select("tr")
    if not containers:
        containers = soup.select("li, .list, .item")

    for container in containers:
        title, detail_url, file_url = _first_useful_link(container, list_url)
        if not title:
            continue
        if detail_url.lower().startswith("javascript:") or title.isdigit():
            continue

        texts = [text for text in _row_texts(container) if text and text != title]
        full_text = _clean_text(container.get_text(" ", strip=True))
        updated_at = _find_date(full_text)
        views = _find_views(full_text)
        department = ""
        for text in texts:
            if text != updated_at and text != views and not DATE_PATTERN.search(text):
                department = text
                break

        records.append(
            {
                "source_id": "CYCC_MINUTES",
                "title": title,
                "department": department,
                "views": views,
                "updated_at": updated_at,
                "detail_url": detail_url,
                "file_url": file_url,
                "crawled_at": crawled_at,
                "raw_hash": make_raw_hash(title, detail_url, updated_at),
            }
        )
    return dedupe_by_raw_hash(records)


def parse_question_video_metadata(html: str, list_url: str, crawled_at: str) -> list[dict[str, Any]]:
    soup = BeautifulSoup(html, "html.parser")
    scope = _content_scope(soup)
    records: list[dict[str, Any]] = []
    containers = scope.select("tr")
    if not containers:
        containers = scope.select("li, .list, .item")

    for container in containers:
        title, video_url, _file_url = _first_useful_link(container, list_url)
        if not title:
            continue

        texts = [text for text in _row_texts(container) if text and text != title]
        full_text = _clean_text(container.get_text(" ", strip=True))
        meeting_date = _find_date(full_text)
        councilor_name = texts[0] if len(texts) > 0 else ""
        council_term = texts[1] if len(texts) > 1 else ""
        session_name = texts[2] if len(texts) > 2 else ""

        records.append(
            {
                "source_id": "CYCC_QUESTION_VIDEO",
                "councilor_name": councilor_name,
                "council_term": council_term,
                "session_name": session_name,
                "video_title": title,
                "video_url": video_url,
                "meeting_date": meeting_date,
                "topic_guess": classify(title),
                "crawled_at": crawled_at,
                "raw_hash": make_raw_hash(title, video_url, councilor_name),
            }
        )

    deduped_records = dedupe_by_raw_hash(records)
    if deduped_records:
        return deduped_records

    iframe_records = _parse_question_video_iframes(scope, list_url, crawled_at)
    if iframe_records:
        return iframe_records

    return _parse_question_video_form_metadata(scope, list_url, crawled_at)


def _parse_session_heading(text: str) -> tuple[str, str]:
    match = SESSION_HEADING_PATTERN.search(text)
    if not match:
        return "", text.strip()
    return match.group(1).strip(), match.group(2).strip()


def _parse_question_video_iframes(scope: Any, list_url: str, crawled_at: str) -> list[dict[str, Any]]:
    result_container = scope.select_one(".resume_cost_03") or scope
    records: list[dict[str, Any]] = []
    council_term = ""
    session_name = ""

    for child in result_container.find_all(recursive=False):
        classes = child.get("class", [])
        if "resume_cost_07" in classes:
            council_term, session_name = _parse_session_heading(child.get_text(" ", strip=True))
            continue

        iframe = child.find("iframe", src=True)
        if iframe is None:
            continue

        video_url = urljoin(list_url, iframe["src"])
        video_id = video_url.rstrip("/").split("/")[-1]
        video_title = _clean_text(f"{council_term} {session_name} 質詢影音 {video_id}")
        records.append(
            {
                "source_id": "CYCC_QUESTION_VIDEO",
                "councilor_name": "",
                "council_term": council_term,
                "session_name": session_name,
                "video_title": video_title,
                "video_url": video_url,
                "meeting_date": "",
                "topic_guess": classify(video_title),
                "crawled_at": crawled_at,
                "raw_hash": make_raw_hash(video_title, video_url, ""),
            }
        )

    return dedupe_by_raw_hash(records)


def _select_options(scope: Any, selector: str) -> list[str]:
    select = scope.select_one(selector)
    if select is None:
        return []
    values: list[str] = []
    for option in select.find_all("option"):
        value = _clean_text(option.get_text(" ", strip=True))
        option_value = _clean_text(option.get("value", ""))
        if not value or value == "請選擇" or option_value == "0":
            continue
        values.append(value)
    return values


def _parse_question_video_form_metadata(scope: Any, list_url: str, crawled_at: str) -> list[dict[str, Any]]:
    councilors = _select_options(scope, "select[id$='peoeple_list']")
    terms = _select_options(scope, "select[id$='DropDownList1']") or [""]
    sessions = _select_options(scope, "select[id$='DropDownList2']") or [""]
    records: list[dict[str, Any]] = []

    for councilor_name in councilors:
        for council_term in terms:
            for session_name in sessions:
                video_title = _clean_text(f"{councilor_name} {council_term} {session_name} 質詢影音 metadata")
                records.append(
                    {
                        "source_id": "CYCC_QUESTION_VIDEO",
                        "councilor_name": councilor_name,
                        "council_term": council_term,
                        "session_name": session_name,
                        "video_title": video_title,
                        "video_url": list_url,
                        "meeting_date": "",
                        "topic_guess": classify(video_title),
                        "crawled_at": crawled_at,
                        "raw_hash": make_raw_hash(video_title, list_url, councilor_name),
                    }
                )

    return dedupe_by_raw_hash(records)


def write_csv_deduped(records: list[dict[str, Any]], output_path: str | Path, columns: list[str]) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_records: list[dict[str, Any]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as file:
            existing_records = list(csv.DictReader(file))

    deduped = dedupe_by_raw_hash([*existing_records, *records])
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(deduped)


class CYCCMetadataCrawler:
    def __init__(self, config_path: str | Path = "config/sources.yml", output_dir: str | Path = "data/raw") -> None:
        self.config = read_config(config_path)
        self.targets = get_cycc_targets(self.config)
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "chiayi-city-failure-analysis/metadata-crawler-v1"})

    def fetch(self, url: str) -> str:
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or response.encoding
        return response.text

    def fetch_question_video_results(self, url: str) -> str:
        initial_response = self.session.get(url, timeout=30)
        initial_response.raise_for_status()
        initial_response.encoding = initial_response.apparent_encoding or initial_response.encoding
        soup = BeautifulSoup(initial_response.text, "html.parser")

        payload: dict[str, str] = {}
        for input_element in soup.find_all("input"):
            name = input_element.get("name")
            input_type = input_element.get("type")
            if name and input_type not in {"submit", "image"}:
                payload[name] = input_element.get("value", "")

        payload.update(
            {
                "ctl00$ContentPlaceHolder1$peoeple_list": "請選擇",
                "ctl00$ContentPlaceHolder1$DropDownList1": "0",
                "ctl00$ContentPlaceHolder1$DropDownList2": "0",
                "ctl00$ContentPlaceHolder1$kySearch.x": "10",
                "ctl00$ContentPlaceHolder1$kySearch.y": "10",
            }
        )

        response = self.session.post(url, data=payload, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or response.encoding
        return response.text

    def crawl_minutes(self, crawled_at: str | None = None) -> list[dict[str, Any]]:
        target = self.targets["minutes"]
        timestamp = crawled_at or datetime.now(timezone.utc).isoformat()
        return parse_minutes_metadata(self.fetch(target.url), target.url, timestamp)

    def crawl_question_videos(self, crawled_at: str | None = None) -> list[dict[str, Any]]:
        target = self.targets["question_videos"]
        timestamp = crawled_at or datetime.now(timezone.utc).isoformat()
        return parse_question_video_metadata(self.fetch_question_video_results(target.url), target.url, timestamp)

    def run(self) -> dict[str, int]:
        minutes_target = self.targets["minutes"]
        videos_target = self.targets["question_videos"]
        minutes_records = self.crawl_minutes()
        video_records = self.crawl_question_videos()

        write_csv_deduped(minutes_records, self.output_dir / minutes_target.output_filename, MINUTES_COLUMNS)
        write_csv_deduped(video_records, self.output_dir / videos_target.output_filename, QUESTION_VIDEO_COLUMNS)
        return {
            minutes_target.output_filename: len(minutes_records),
            videos_target.output_filename: len(video_records),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl CYCC metadata into data/raw CSV files.")
    parser.add_argument("--config", default="config/sources.yml")
    parser.add_argument("--output-dir", default="data/raw")
    args = parser.parse_args()

    result = CYCCMetadataCrawler(config_path=args.config, output_dir=args.output_dir).run()
    print(result)


if __name__ == "__main__":
    main()
