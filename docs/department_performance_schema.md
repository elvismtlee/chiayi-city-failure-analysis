# 局處處理與回應分析 Schema v1

本文件定義如何分析局處與城市議題之間的關係。

## 目的

建立局處回應、處理效率與議題負荷的資料模型。

---

## 輸入資料

```text
data/raw/1999_cases.csv
data/raw/cycc_minutes_metadata.csv
data/processed/department_normalized.csv
```

---

## 輸出資料

```text
dashboard/data/department_performance.json
```

---

## 欄位定義

| 欄位 | 說明 |
|---|---|
| department | 局處名稱 |
| total_cases | 相關案件數 |
| avg_processing_days | 平均處理天數 |
| top_issues | 主要議題 |
| repeated_cases | 重複案件數 |
| council_question_count | 被質詢次數 |
| response_score | 回應指標分數 |
| notes | 備註 |

---

## JSON 範例

```json
[
  {
    "department": "交通處",
    "total_cases": 320,
    "avg_processing_days": 12.5,
    "top_issues": ["停車", "號誌", "通學安全"],
    "repeated_cases": 42,
    "council_question_count": 18,
    "response_score": 78,
    "notes": "交通與停車為高負荷議題"
  }
]
```

---

## 分析方式

### 1. 案件負荷

```text
total_cases
```

### 2. 處理速度

```text
avg_processing_days
```

### 3. 重複問題

```text
repeated_cases
```

### 4. 議會關注度

```text
council_question_count
```

---

## Dashboard 用途

- 局處案件負荷排行
- 平均處理天數
- 被質詢最多局處
- 議題與局處對照
- 行政效率觀察

---

## 注意事項

1. 資料不足時不可做過度結論。
2. 應區分案件量高與效率低是不同概念。
3. 局處名稱必須先使用字典標準化。
