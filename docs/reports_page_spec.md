# 城市週報頁規格 v1

本文件定義 `dashboard/reports.html` 的頁面內容與資料結構。

---

## 頁面定位

```text
嘉義城市故障週報列表頁
```

用途是保存每週產出的城市故障觀察報告。

---

## 建議網址

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/reports.html
```

---

## 頁面主要區塊

### 1. 最新週報

顯示最新一期：

- 週報標題
- 日期
- 本週摘要
- 三大重點
- 進入完整週報按鈕

---

### 2. 歷史週報列表

欄位：

| 欄位 | 說明 |
|---|---|
| report_id | 週報 ID |
| title | 週報標題 |
| week_start | 週期開始 |
| week_end | 週期結束 |
| top_issue | 本週主要議題 |
| summary | 摘要 |
| report_url | 報告連結 |

---

## JSON 資料

建議建立：

```text
dashboard/data/reports_index.json
```

範例：

```json
[
  {
    "report_id": "2026-W21",
    "title": "嘉義城市故障週報｜2026 第 21 週",
    "week_start": "2026-05-18",
    "week_end": "2026-05-24",
    "top_issue": "交通",
    "summary": "交通、停車與道路議題仍是本週主要觀察重點。",
    "report_url": "./reports/2026-W21.html"
  }
]
```

---

## 報告輸出位置

### HTML

```text
dashboard/reports/*.html
```

### Markdown

```text
reports/markdown/*.md
```

### JSON

```text
reports/json/*.json
```

---

## 每週報告基本結構

1. 本週摘要
2. 熱門議題排行
3. 熱點地圖
4. 議員質詢摘要
5. 局處負荷觀察
6. 城市故障分數
7. 建議行動
8. 資料來源與限制

---

## 導覽關係

`reports.html` 應與下列頁面互相連結：

- index.html
- insights.html
- sources.html
- methodology.html
