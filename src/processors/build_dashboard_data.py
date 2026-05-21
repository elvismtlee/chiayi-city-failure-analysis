import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"
LOCAL_PLACE_DICTIONARY_PATH = DASHBOARD_DATA_DIR / "local_place_dictionary.json"
WENHUA_PLACE_ID = "place-wenhua-road-business-district"

DEFAULT_PLACE_ENTRY = {
    "place_id": WENHUA_PLACE_ID,
    "display_name": "文化路商圈",
    "local_name": "文化路",
    "formal_name": "文化路商圈",
    "aliases": ["文化路周邊", "文化路商圈周邊"],
    "avoid_terms": [],
    "district": "西區 / 東區交界",
}


def load_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def load_local_place_dictionary(path: Path = LOCAL_PLACE_DICTIONARY_PATH) -> list[dict]:
    if not path.exists():
        return [DEFAULT_PLACE_ENTRY]
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else [DEFAULT_PLACE_ENTRY]


def get_place_entry(place_id: str, dictionary: list[dict] | None = None) -> dict:
    place_dictionary = dictionary if dictionary is not None else load_local_place_dictionary()
    for item in place_dictionary:
        if item.get("place_id") == place_id:
            return item
    return DEFAULT_PLACE_ENTRY


def get_place_display_name(place_id: str, dictionary: list[dict] | None = None) -> str:
    return str(get_place_entry(place_id, dictionary).get("display_name") or DEFAULT_PLACE_ENTRY["display_name"])


def normalize_place_name(text: str, dictionary: list[dict] | None = None) -> str:
    place_dictionary = dictionary if dictionary is not None else load_local_place_dictionary()
    normalized = text
    for item in place_dictionary:
        display_name = str(item.get("display_name") or "")
        if not display_name:
            continue
        terms = [
            *item.get("avoid_terms", []),
            *item.get("aliases", []),
            item.get("formal_name", ""),
        ]
        for term in terms:
            if term and term != display_name:
                normalized = normalized.replace(str(term), display_name)
    return normalized


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_summary():
    minutes = load_csv_if_exists(RAW_DIR / "cycc_minutes_metadata.csv")
    videos = load_csv_if_exists(RAW_DIR / "cycc_question_video_metadata.csv")

    summary = {
        "total_cases": 12458,
        "total_questions": int(len(videos)) if not videos.empty else 386,
        "total_hotspots": 18,
        "top_issue": "交通",
        "updated_at": pd.Timestamp.now(tz="Asia/Taipei").strftime("%Y-%m-%d %H:%M:%S"),
        "minutes_metadata_count": int(len(minutes)) if not minutes.empty else 0,
        "question_video_metadata_count": int(len(videos)) if not videos.empty else 0,
    }
    return summary


def build_issue_ranking():
    default_data = [
        {"issue": "停車", "score": 88},
        {"issue": "道路", "score": 72},
        {"issue": "人行", "score": 64},
        {"issue": "環境", "score": 51},
        {"issue": "路燈", "score": 39},
    ]
    return default_data


def build_hotspots():
    place_dictionary = load_local_place_dictionary()
    wenhua_entry = get_place_entry(WENHUA_PLACE_ID, place_dictionary)
    return [
        {
            "place_id": WENHUA_PLACE_ID,
            "name": get_place_display_name(WENHUA_PLACE_ID, place_dictionary),
            "district": wenhua_entry.get("district", DEFAULT_PLACE_ENTRY["district"]),
            "category": "停車 / 人行",
            "department": "交通處",
            "score": 92,
            "action": "商圈動線與停車熱點專案",
            "x": 22,
            "y": 38,
        },
        {
            "name": "市場周邊",
            "district": "西區",
            "category": "垃圾 / 動線",
            "department": "環保局 / 建設處",
            "score": 78,
            "action": "市場周邊環境改善與卸貨規劃",
            "x": 60,
            "y": 55,
        },
        {
            "name": "學校周邊",
            "district": "西區",
            "category": "通學安全",
            "department": "交通處 / 教育處",
            "score": 71,
            "action": "通學步道與接送區改善",
            "x": 42,
            "y": 72,
        },
    ]


def main():
    write_json(DASHBOARD_DATA_DIR / "dashboard_summary.json", build_summary())
    write_json(DASHBOARD_DATA_DIR / "issue_ranking.json", build_issue_ranking())
    write_json(DASHBOARD_DATA_DIR / "hotspots.json", build_hotspots())
    print("Dashboard data built successfully.")


if __name__ == "__main__":
    main()
