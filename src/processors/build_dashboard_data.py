import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from src.classifiers.issue_classifier import classify
except ImportError:  # pragma: no cover - keeps direct script execution usable
    classify = lambda text: "其他"  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"

MINUTES_FILE = "cycc_minutes_metadata.csv"
QUESTION_VIDEO_FILE = "cycc_question_video_metadata.csv"

FALLBACK_ISSUE_RANKING = [
    {"issue": "停車", "score": 88},
    {"issue": "道路", "score": 72},
    {"issue": "人行", "score": 64},
    {"issue": "環境", "score": 51},
    {"issue": "路燈", "score": 39},
]

FALLBACK_HOTSPOTS = [
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

ISSUE_KEYWORDS = {
    "交通": ["停車", "違停", "號誌", "交通", "機車", "汽車"],
    "道路": ["道路", "坑洞", "柏油", "路面", "施工", "公共工程", "建管", "發照"],
    "環境": ["垃圾", "髒亂", "異味", "清潔", "環境"],
    "人行": ["人行道", "斑馬線", "無障礙", "通學"],
    "公共安全": ["路燈", "照明", "危險", "安全"],
    "文化體育": ["體育", "運動", "場館", "文化"],
    "土地管理": ["土地", "市有土地"],
    "議事": ["議會", "程序委員會", "定期會", "臨時會", "會議"],
}

HOTSPOT_PROFILES = {
    "交通": ("交通與停車熱點", "交通處", "停車與交通動線改善"),
    "道路": ("公共工程與道路品質", "工務處", "公共工程品質與路平追蹤"),
    "環境": ("市場周邊生活環境", "環保局", "環境清潔與市場周邊改善"),
    "人行": ("通學與人行安全", "交通處 / 教育處", "通學步道與人行安全盤點"),
    "公共安全": ("公共安全設施", "工務處 / 警察局", "照明與危險點位巡檢"),
    "文化體育": ("運動場館與文化設施", "教育處 / 文化局", "場館設施管理與使用需求盤點"),
    "土地管理": ("市有土地管理", "財政稅務局", "市有土地處分與管理追蹤"),
    "議事": ("議會議事追蹤", "議事組", "會議紀錄與議事進度整理"),
    "其他": ("公共議題追蹤", "市府相關局處", "持續補齊分類規則與資料來源"),
}

HOTSPOT_POSITIONS = [(22, 38), (60, 55), (42, 72), (76, 34), (30, 62)]


def load_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path, encoding="utf-8-sig").fillna("")
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_taipei() -> str:
    return pd.Timestamp.now(tz="Asia/Taipei").strftime("%Y-%m-%d %H:%M:%S")


def guess_issue(*parts: object) -> str:
    text = " ".join(str(part or "") for part in parts)
    for issue, keywords in ISSUE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return issue

    classified = classify(text)
    return classified if classified != "其他" else "其他"


def collect_issue_counts(minutes: pd.DataFrame, videos: pd.DataFrame) -> Counter:
    counts: Counter = Counter()

    for _, row in minutes.iterrows():
        issue = guess_issue(row.get("title", ""), row.get("department", ""))
        counts[issue] += 1

    for _, row in videos.iterrows():
        topic_guess = str(row.get("topic_guess", "")).strip()
        if topic_guess and topic_guess != "其他":
            issue = topic_guess
        else:
            issue = guess_issue(
                row.get("video_title", ""),
                row.get("session_name", ""),
                row.get("councilor_name", ""),
            )
        counts[issue] += 1

    return counts


def build_issue_ranking(minutes: pd.DataFrame, videos: pd.DataFrame) -> list[dict[str, int | str]]:
    counts = collect_issue_counts(minutes, videos)
    if not counts:
        return FALLBACK_ISSUE_RANKING

    max_count = max(counts.values())
    ranking = []
    for issue, count in counts.most_common(5):
        ranking.append(
            {
                "issue": issue,
                "score": max(35, round(count / max_count * 100)),
                "count": int(count),
            }
        )
    return ranking


def build_hotspots(issue_ranking: list[dict[str, Any]], has_raw_data: bool) -> list[dict[str, Any]]:
    if not has_raw_data:
        return FALLBACK_HOTSPOTS

    hotspots = []
    for index, item in enumerate(issue_ranking[:5]):
        issue = str(item["issue"])
        name, department, action = HOTSPOT_PROFILES.get(issue, HOTSPOT_PROFILES["其他"])
        x, y = HOTSPOT_POSITIONS[index]
        hotspots.append(
            {
                "name": name,
                "district": "嘉義市",
                "category": issue,
                "department": department,
                "score": int(item["score"]),
                "action": action,
                "x": x,
                "y": y,
            }
        )
    return hotspots


def build_summary(
    minutes: pd.DataFrame,
    videos: pd.DataFrame,
    issue_ranking: list[dict[str, Any]],
    hotspots: list[dict[str, Any]],
) -> dict[str, Any]:
    has_raw_data = not minutes.empty or not videos.empty
    return {
        "total_cases": 12458,
        "total_questions": int(len(videos)) if not videos.empty else 386,
        "total_hotspots": int(len(hotspots)),
        "top_issue": str(issue_ranking[0]["issue"]) if issue_ranking else "交通",
        "updated_at": now_taipei(),
        "minutes_metadata_count": int(len(minutes)),
        "question_video_metadata_count": int(len(videos)),
        "data_status": "raw_csv" if has_raw_data else "fallback_mock",
        "source_files": {
            MINUTES_FILE: bool(not minutes.empty),
            QUESTION_VIDEO_FILE: bool(not videos.empty),
        },
    }


def build_ai_issue_summary(
    summary: dict[str, Any],
    issue_ranking: list[dict[str, Any]],
    has_raw_data: bool,
) -> dict[str, Any]:
    if not has_raw_data:
        return {
            "updated_at": summary["updated_at"],
            "summary_title": "本週嘉義城市故障觀察",
            "summary": "目前尚未偵測到 CYCC raw CSV，dashboard 保留原型資料，待 crawler 輸出後會自動改用真實 metadata 更新摘要。",
            "top_findings": [
                "交通、停車與道路仍作為原型優先觀察議題",
                "raw CSV 不存在時，資料管線會保留 mock data，避免 GitHub Pages 顯示失敗",
                "crawler 輸出後，dashboard JSON 會改由 metadata 統計產生",
            ],
            "recommended_actions": [
                "持續接入 CYCC 會議紀錄與議員質詢影音 metadata",
                "補齊 1999 與陳情資料來源",
                "將熱點資料轉為 GeoJSON 並接入正式地圖",
            ],
        }

    top_issues = [str(item["issue"]) for item in issue_ranking[:3]]
    return {
        "updated_at": summary["updated_at"],
        "summary_title": "CYCC metadata 城市議題摘要",
        "summary": (
            f"本次資料管線讀取 {summary['minutes_metadata_count']} 筆會議紀錄 metadata "
            f"與 {summary['question_video_metadata_count']} 筆議員質詢影音 metadata，"
            f"目前最高關注議題為「{summary['top_issue']}」。"
        ),
        "top_findings": [
            f"目前前 3 名議題為：{'、'.join(top_issues)}",
            "會議紀錄與質詢影音已整合為 dashboard 可讀取的 JSON",
            "raw_hash 去重後的 metadata 可作為後續議題趨勢與熱點分析基礎",
        ],
        "recommended_actions": [
            "持續累積 CYCC metadata 歷史資料",
            "把質詢影音進一步補上議員姓名與逐字稿摘要",
            "將 raw CSV 與 1999 / 陳情資料合併，建立更完整的城市議題排行",
        ],
    }


def build_dashboard_data(raw_dir: Path = RAW_DIR, dashboard_data_dir: Path = DASHBOARD_DATA_DIR) -> dict[str, Any]:
    minutes = load_csv_if_exists(raw_dir / MINUTES_FILE)
    videos = load_csv_if_exists(raw_dir / QUESTION_VIDEO_FILE)
    has_raw_data = not minutes.empty or not videos.empty

    issue_ranking = build_issue_ranking(minutes, videos)
    hotspots = build_hotspots(issue_ranking, has_raw_data)
    summary = build_summary(minutes, videos, issue_ranking, hotspots)
    ai_summary = build_ai_issue_summary(summary, issue_ranking, has_raw_data)

    outputs = {
        "dashboard_summary.json": summary,
        "issue_ranking.json": issue_ranking,
        "hotspots.json": hotspots,
        "ai_issue_summary.json": ai_summary,
    }

    for filename, data in outputs.items():
        write_json(dashboard_data_dir / filename, data)

    return outputs


def main() -> None:
    outputs = build_dashboard_data()
    print(f"Dashboard data built successfully: {', '.join(outputs)}")


if __name__ == "__main__":
    main()
