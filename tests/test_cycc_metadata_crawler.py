import csv
from pathlib import Path

from src.crawlers.cycc_metadata_crawler import (
    MINUTES_COLUMNS,
    QUESTION_VIDEO_COLUMNS,
    CYCCMetadataCrawler,
    dedupe_by_raw_hash,
    make_raw_hash,
    parse_minutes_metadata,
    parse_question_video_metadata,
    read_config,
    write_csv_deduped,
)


SOURCES_YML = """
sources:
  cycc:
    name: 嘉義市議會
    base_url: https://www.cycc.gov.tw/
    targets:
      minutes:
        name: 會議紀錄檢索
        url: https://www.cycc.gov.tw/web/Download_file/listDownload_file.aspx?c0=3682
        type: html_list
      question_videos:
        name: 議員質詢影音專區
        url: https://www.cycc.gov.tw/web/UnitStaff_New/List.aspx?c0=4758
        type: html_form_metadata
"""


def test_read_config_loads_cycc_targets(tmp_path: Path) -> None:
    config_path = tmp_path / "sources.yml"
    config_path.write_text(SOURCES_YML, encoding="utf-8")

    config = read_config(config_path)

    assert config["sources"]["cycc"]["targets"]["minutes"]["type"] == "html_list"


def test_parse_minutes_metadata_extracts_required_fields() -> None:
    html = """
    <table>
      <tr>
        <td>議事組</td>
        <td><a href="/web/Download_file/content.aspx?id=1">第 11 屆第 3 次定期會會議紀錄</a></td>
        <td><a href="/files/minutes.pdf">PDF</a></td>
        <td>2026/05/21</td>
        <td>點閱 42</td>
      </tr>
    </table>
    """

    records = parse_minutes_metadata(html, "https://www.cycc.gov.tw/list.aspx", "2026-05-21T00:00:00+00:00")

    assert records[0]["source_id"] == "CYCC_MINUTES"
    assert records[0]["title"] == "第 11 屆第 3 次定期會會議紀錄"
    assert records[0]["department"] == "議事組"
    assert records[0]["updated_at"] == "2026-05-21"
    assert records[0]["views"] == "42"
    assert records[0]["detail_url"] == "https://www.cycc.gov.tw/web/Download_file/content.aspx?id=1"
    assert records[0]["file_url"] == "https://www.cycc.gov.tw/files/minutes.pdf"
    assert records[0]["raw_hash"]


def test_parse_question_video_metadata_extracts_required_fields() -> None:
    html = """
    <table>
      <tr>
        <td>王議員</td>
        <td>第 11 屆</td>
        <td>第 3 次定期會</td>
        <td><a href="/video/123">道路坑洞與交通安全質詢</a></td>
        <td>2026-05-21</td>
      </tr>
    </table>
    """

    records = parse_question_video_metadata(html, "https://www.cycc.gov.tw/videos.aspx", "2026-05-21T00:00:00+00:00")

    assert records[0]["source_id"] == "CYCC_QUESTION_VIDEO"
    assert records[0]["councilor_name"] == "王議員"
    assert records[0]["council_term"] == "第 11 屆"
    assert records[0]["session_name"] == "第 3 次定期會"
    assert records[0]["video_title"] == "道路坑洞與交通安全質詢"
    assert records[0]["video_url"] == "https://www.cycc.gov.tw/video/123"
    assert records[0]["meeting_date"] == "2026-05-21"
    assert records[0]["topic_guess"] == "交通"


def test_parse_question_video_metadata_falls_back_to_form_options() -> None:
    html = """
    <main>
      <div id="ContentPlaceHolder1_UpdatePanel1">
        <select id="ContentPlaceHolder1_peoeple_list">
          <option value="請選擇">請選擇</option>
          <option value="王議員浩">王議員浩</option>
        </select>
        <select id="ContentPlaceHolder1_DropDownList1">
          <option value="0">請選擇</option>
          <option value="40737">第十屆</option>
        </select>
        <select id="ContentPlaceHolder1_DropDownList2">
          <option value="0">請選擇</option>
          <option value="40738">第二次定期會</option>
        </select>
      </div>
    </main>
    """

    records = parse_question_video_metadata(html, "https://www.cycc.gov.tw/videos.aspx", "2026-05-21T00:00:00+00:00")

    assert records == [
        {
            "source_id": "CYCC_QUESTION_VIDEO",
            "councilor_name": "王議員浩",
            "council_term": "第十屆",
            "session_name": "第二次定期會",
            "video_title": "王議員浩 第十屆 第二次定期會 質詢影音 metadata",
            "video_url": "https://www.cycc.gov.tw/videos.aspx",
            "meeting_date": "",
            "topic_guess": "其他",
            "crawled_at": "2026-05-21T00:00:00+00:00",
            "raw_hash": make_raw_hash(
                "王議員浩 第十屆 第二次定期會 質詢影音 metadata",
                "https://www.cycc.gov.tw/videos.aspx",
                "王議員浩",
            ),
        }
    ]


def test_parse_question_video_metadata_extracts_iframe_results() -> None:
    html = """
    <main>
      <div id="ContentPlaceHolder1_UpdatePanel1">
        <div class="resume_cost_03">
          <div class="resume_cost_07">【第十屆:第二次定期會】</div>
          <div class="resume_cost_08">
            <iframe src="https://www.youtube.com/embed/abc123"></iframe>
          </div>
          <div class="resume_cost_08">
            <iframe src="https://www.youtube.com/embed/abc123"></iframe>
          </div>
          <div class="resume_cost_07">【第十屆:第三次定期會】</div>
          <div class="resume_cost_08">
            <iframe src="https://www.youtube.com/embed/def456"></iframe>
          </div>
        </div>
      </div>
    </main>
    """

    records = parse_question_video_metadata(html, "https://www.cycc.gov.tw/videos.aspx", "2026-05-21T00:00:00+00:00")

    assert len(records) == 2
    assert records[0]["council_term"] == "第十屆"
    assert records[0]["session_name"] == "第二次定期會"
    assert records[0]["video_title"] == "第十屆 第二次定期會 質詢影音 abc123"
    assert records[0]["video_url"] == "https://www.youtube.com/embed/abc123"
    assert records[1]["session_name"] == "第三次定期會"


def test_raw_hash_dedupes_records() -> None:
    raw_hash = make_raw_hash("title", "url", "date")
    records = [{"raw_hash": raw_hash, "title": "A"}, {"raw_hash": raw_hash, "title": "B"}]

    assert dedupe_by_raw_hash(records) == [{"raw_hash": raw_hash, "title": "A"}]


def test_write_csv_deduped_keeps_rerun_unique(tmp_path: Path) -> None:
    output = tmp_path / "cycc_minutes_metadata.csv"
    record = {
        "source_id": "CYCC_MINUTES",
        "title": "會議紀錄",
        "department": "議事組",
        "views": "1",
        "updated_at": "2026-05-21",
        "detail_url": "https://example.com/1",
        "file_url": "",
        "crawled_at": "2026-05-21T00:00:00+00:00",
        "raw_hash": make_raw_hash("會議紀錄", "https://example.com/1", "2026-05-21"),
    }

    write_csv_deduped([record], output, MINUTES_COLUMNS)
    write_csv_deduped([record], output, MINUTES_COLUMNS)

    assert output.read_text(encoding="utf-8-sig").count("CYCC_MINUTES") == 1


def test_crawler_reads_config_fetches_and_writes_csv(tmp_path: Path) -> None:
    config_path = tmp_path / "sources.yml"
    config_path.write_text(SOURCES_YML, encoding="utf-8")
    output_dir = tmp_path / "raw"
    crawler = CYCCMetadataCrawler(config_path=config_path, output_dir=output_dir)

    def fake_fetch(url: str) -> str:
        if "Download_file" in url:
            return """
            <table><tr><td>議事組</td><td><a href="/m/1">會議紀錄</a></td><td>2026/05/21</td></tr></table>
            """
        return """
        <table><tr><td>王議員</td><td>第 11 屆</td><td>第 3 次定期會</td><td><a href="/v/1">停車問題質詢</a></td></tr></table>
        """

    crawler.fetch = fake_fetch  # type: ignore[method-assign]
    crawler.fetch_question_video_results = fake_fetch  # type: ignore[method-assign]

    result = crawler.run()

    assert result["cycc_minutes_metadata.csv"] == 1
    assert result["cycc_question_video_metadata.csv"] == 1
    assert (output_dir / "cycc_minutes_metadata.csv").exists()
    assert (output_dir / "cycc_question_video_metadata.csv").exists()
    with (output_dir / "cycc_question_video_metadata.csv").open("r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows[0].keys() >= set(QUESTION_VIDEO_COLUMNS)
