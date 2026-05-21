# 議員議題分析 Schema v1

本文件定義如何分析議員質詢與城市議題之間的關係。

## 目的

把議員質詢 metadata、會議紀錄與影音資料轉成可比較的議題關注度資料。

---

## 輸入資料

```text
data/raw/cycc_question_video_metadata.csv
data/raw/cycc_minutes_metadata.csv
data/processed/question_issue_classified.csv
```

---

## 輸出資料

```text
dashboard/data/councilor_issue_analysis.json
```

---

## 欄位定義

| 欄位 | 說明 |
|---|---|
| councilor_name | 議員姓名 |
| council_term | 屆次 |
| district | 選區 |
| total_questions | 質詢總數 |
| top_issues | 最常質詢議題 |
| issue_distribution | 各議題比例 |
| latest_question_date | 最近質詢日期 |
| source_count | 原始資料筆數 |

---

## JSON 範例

```json
[
  {
    "councilor_name": "範例議員",
    "council_term": "第十一屆",
    "district": "西區",
    "total_questions": 25,
    "top_issues": ["交通", "道路", "教育"],
    "issue_distribution": {
      "交通": 10,
      "道路": 6,
      "教育": 4,
      "環境": 3,
      "其他": 2
    },
    "latest_question_date": "2026-05-01",
    "source_count": 25
  }
]
```

---

## Dashboard 用途

可建立：

1. 議員議題關注度排行
2. 議員 × 議題矩陣
3. 市民陳情 vs 議員質詢落差
4. 特定議題關注議員清單
5. 西區議題代表性分析

---

## 注意事項

1. 本分析只根據公開資料整理，不做個人攻擊。
2. 若資料不足，應標示 sample / incomplete。
3. 議員姓名與屆次需標準化。
4. 不應把資料不足解讀為不關心，只能標示「公開資料中較少出現」。
