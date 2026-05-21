import csv
import json
from pathlib import Path

from scripts.build_issue_classified_sample import build_issue_classified_sample
from src.classifiers.issue_classifier import REQUIRED_OUTPUT_FIELDS, TAXONOMY_CODES


def write_sample_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
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
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def make_rows(count: int) -> list[dict[str, str]]:
    rows = []
    for index in range(count):
        rows.append(
            {
                "source_id": "CYCC_QUESTION_VIDEO",
                "councilor_name": "",
                "council_term": "第十屆",
                "session_name": "第七次定期會",
                "video_title": f"市場周邊停車與人行動線質詢 {index}",
                "video_url": f"https://www.youtube.com/embed/test{index}",
                "meeting_date": "",
                "topic_guess": "交通",
                "crawled_at": "2026-05-21T00:00:00+00:00",
                "raw_hash": f"hash-{index}",
            }
        )
    return rows


def test_build_issue_classified_sample_writes_first_10_records(tmp_path: Path) -> None:
    source = tmp_path / "cycc_question_video_metadata.csv"
    output = tmp_path / "issue_classified_sample.json"
    write_sample_csv(source, make_rows(12))

    classified = build_issue_classified_sample(source=source, output=output)

    assert output.exists()
    assert len(classified) == 10
    written = json.loads(output.read_text(encoding="utf-8"))
    assert written == classified
    assert list(written[0]) == REQUIRED_OUTPUT_FIELDS
    assert written[0]["primary_issue"] in TAXONOMY_CODES
    assert written[0]["primary_issue"] == "traffic"


def test_build_issue_classified_sample_honors_limit(tmp_path: Path) -> None:
    source = tmp_path / "cycc_question_video_metadata.csv"
    output = tmp_path / "issue_classified_sample.json"
    write_sample_csv(source, make_rows(5))

    classified = build_issue_classified_sample(source=source, output=output, limit=3)

    assert len(classified) == 3
    assert all(item["source_id"] == "CYCC_QUESTION_VIDEO" for item in classified)
