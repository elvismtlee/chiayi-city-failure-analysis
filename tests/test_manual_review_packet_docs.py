from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs" / "open_data_manual_review_packets"


def test_manual_review_packet_docs_exist() -> None:
    for filename in ["day_1_packet.md", "day_2_packet.md", "day_3_packet.md"]:
        assert (DOCS_DIR / filename).exists()


def test_manual_review_packet_docs_include_required_safety_and_checklist_text() -> None:
    for filename in ["day_1_packet.md", "day_2_packet.md", "day_3_packet.md"]:
        content = (DOCS_DIR / filename).read_text(encoding="utf-8")
        assert "不是 crawler" in content
        assert "不啟動 live crawler" in content
        assert "crawler_execution_allowed" in content
        assert "source_url" in content
        assert "completion checklist" in content
