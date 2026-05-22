from __future__ import annotations

import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures"
HTML_FIXTURE = FIXTURE_DIR / "cycc_minutes_sample.html"
TEXT_FIXTURE = FIXTURE_DIR / "cycc_minutes_sample_text.txt"

REQUIRED_FIELDS = [
    "source_id",
    "meeting_name",
    "meeting_date",
    "councilor_name",
    "department",
    "agenda_item",
    "issue_keywords",
    "source_url",
    "raw_text",
    "raw_hash",
    "parser_status",
    "review_status",
]

SENSITIVE_FIELDS = {
    "phone",
    "email",
    "address",
    "national_id",
    "id_number",
    "full_address",
}

HASH_FIELDS = [
    "source_id",
    "meeting_name",
    "meeting_date",
    "councilor_name",
    "department",
    "agenda_item",
    "issue_keywords",
    "source_url",
    "raw_text",
]

STRUCTURED_HTML_FIELDS = {"meeting_date", "source_url"}


class MinutesFixtureHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.source_id = "CYCC_MINUTES_FIXTURE_HTML"
        self.field_stack: list[tuple[str, str]] = []
        self.text_chunks: dict[str, list[str]] = {}
        self.current_keyword_chunks: list[str] | None = None
        self.issue_keywords: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value for key, value in attrs}
        if attr_map.get("data-source-id"):
            self.source_id = attr_map["data-source-id"] or self.source_id

        field = attr_map.get("data-field")
        if field:
            self.field_stack.append((field, tag))
            self.text_chunks.setdefault(field, [])
            if field == "source_url" and attr_map.get("href"):
                self.text_chunks[field].append(attr_map["href"] or "")
            if field == "meeting_date" and attr_map.get("datetime"):
                self.text_chunks[field].append(attr_map["datetime"] or "")

        if tag == "li" and self.current_field == "issue_keywords":
            self.current_keyword_chunks = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "li" and self.current_keyword_chunks is not None:
            keyword = normalize_text(" ".join(self.current_keyword_chunks))
            if keyword:
                self.issue_keywords.append(keyword)
            self.current_keyword_chunks = None

        if self.field_stack and self.field_stack[-1][1] == tag:
            self.field_stack.pop()

    def handle_data(self, data: str) -> None:
        text = normalize_text(data)
        if not text or not self.field_stack:
            return

        current_field = self.current_field
        if current_field in STRUCTURED_HTML_FIELDS and self.text_chunks.get(current_field):
            return

        self.text_chunks.setdefault(current_field, []).append(text)
        if self.current_keyword_chunks is not None:
            self.current_keyword_chunks.append(text)

    @property
    def current_field(self) -> str:
        return self.field_stack[-1][0] if self.field_stack else ""

    def to_record(self) -> dict[str, Any]:
        fields = {
            field: normalize_text(" ".join(chunks))
            for field, chunks in self.text_chunks.items()
            if field != "issue_keywords"
        }
        fields["source_id"] = self.source_id
        fields["issue_keywords"] = self.issue_keywords or split_keywords(
            " ".join(self.text_chunks.get("issue_keywords", []))
        )
        return build_record(fields)


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def split_keywords(value: str) -> list[str]:
    separators = [",", "，", "、", "\n"]
    normalized = value
    for separator in separators:
        normalized = normalized.replace(separator, ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def stable_raw_hash(record: dict[str, Any]) -> str:
    payload = {field: record.get(field, "") for field in HASH_FIELDS}
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def build_record(fields: dict[str, Any]) -> dict[str, Any]:
    record = {
        "source_id": normalize_text(str(fields.get("source_id", ""))),
        "meeting_name": normalize_text(str(fields.get("meeting_name", ""))),
        "meeting_date": normalize_text(str(fields.get("meeting_date", ""))),
        "councilor_name": normalize_text(str(fields.get("councilor_name", ""))),
        "department": normalize_text(str(fields.get("department", ""))),
        "agenda_item": normalize_text(str(fields.get("agenda_item", ""))),
        "issue_keywords": list(fields.get("issue_keywords") or []),
        "source_url": normalize_text(str(fields.get("source_url", ""))),
        "raw_text": normalize_text(str(fields.get("raw_text", ""))),
        "parser_status": "parsed_from_fixture",
        "review_status": "unreviewed",
    }
    record["raw_hash"] = stable_raw_hash(record)
    return record


def parse_html_fixture(path: Path = HTML_FIXTURE) -> dict[str, Any]:
    parser = MinutesFixtureHTMLParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.to_record()


def parse_text_fixture(path: Path = TEXT_FIXTURE) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    raw_text_lines: list[str] = []
    in_raw_text = False

    for line in path.read_text(encoding="utf-8").splitlines():
        if in_raw_text:
            raw_text_lines.append(line)
            continue
        if line.startswith("raw_text:"):
            in_raw_text = True
            maybe_text = line.split(":", 1)[1].strip()
            if maybe_text:
                raw_text_lines.append(maybe_text)
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "issue_keywords":
            fields[key] = split_keywords(value)
        else:
            fields[key] = value

    fields["raw_text"] = normalize_text("\n".join(raw_text_lines))
    return build_record(fields)


def parse_all_fixtures() -> list[dict[str, Any]]:
    return [parse_html_fixture(), parse_text_fixture()]


def validate_no_sensitive_fields(record: dict[str, Any]) -> None:
    leaked_fields = SENSITIVE_FIELDS.intersection(record.keys())
    if leaked_fields:
        raise ValueError(f"Sensitive fields are not allowed: {sorted(leaked_fields)}")


def main() -> None:
    records = parse_all_fixtures()
    for record in records:
        validate_no_sensitive_fields(record)
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
