# Dashboard Data Contract v1

本文件定義 crawler / parser 輸出後，前端 dashboard 要讀取的資料格式。

目的：讓 crawler、資料清洗、AI 分類、dashboard 可以各自開發，但資料格式一致。

---

## 1. dashboard_summary.json

位置：

```text
dashboard/data/dashboard_summary.json
```

用途：首頁 KPI 卡片與總覽。

欄位：

| 欄位 | 說明 |
|---|---|
| total_cases | 陳情 / 1999 案件總數 |
| total_questions | 議員質詢總數 |
| total_hotspots | 熱點數 |
| top_issue | 最熱門議題 |
| updated_at | 資料更新時間 |

範例：

```json
{
  "total_cases": 12458,
  "total_questions": 386,
  "total_hotspots": 18,
  "top_issue": "交通",
  "updated_at": "2026-05-21"
}
```

---

## 2. issue_ranking.json

位置：

```text
dashboard/data/issue_ranking.json
```

用途：議題排行長條圖。

範例：

```json
[
  {"issue": "停車", "score": 88},
  {"issue": "道路", "score": 72},
  {"issue": "人行", "score": 64}
]
```

---

## 3. hotspots.json

位置：

```text
dashboard/data/hotspots.json
```

用途：熱點地圖與城市故障追蹤表。

欄位：

| 欄位 | 說明 |
|---|---|
| name | 熱點名稱 |
| district | 行政區 |
| category | 主要議題 |
| department | 對應局處 |
| score | 城市故障指數 |
| action | 建議行動 |
| x | 原型地圖 X 位置，正式版改經度 |
| y | 原型地圖 Y 位置，正式版改緯度 |

---

## 4. crawler metadata 輸出後如何接 dashboard

第一階段流程：

```text
crawler CSV
→ processed JSON
→ dashboard/data/*.json
→ GitHub Pages dashboard
```

第二階段流程：

```text
crawler CSV
→ Google Sheet / BigQuery
→ API / JSON export
→ dashboard
```

---

## 5. 注意事項

1. dashboard 不直接讀 raw CSV
2. raw data 放 data/raw
3. 清洗後資料放 data/processed
4. 前端只讀 dashboard/data JSON
5. 之後可接 Google Sheet published JSON 或 Cloud Function API
