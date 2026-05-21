import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"


def load_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


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
    return [
        {
            "name": "文化路商圈",
            "district": "西區 / 東區交界",
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
