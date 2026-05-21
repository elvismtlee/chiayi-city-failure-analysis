# 城市故障趨勢分析規格 v1

## 目的

分析：

- 哪些議題正在增加
- 哪些問題長期存在
- 哪些區域值得優先處理

並建立「城市故障趨勢模型」。

---

## 輸入資料

來源：

- 1999 metadata
- 陳情案件
- 議員質詢 metadata
- AI issue classification
- hotspot 資料

---

## 分析時間範圍

### 短期

- 7 天
- 30 天
- 90 天

### 中期

- 半年
- 一年

### 長期

- 12 年歷史資料

---

## 輸出 JSON

```text
dashboard/data/issue_trends.json
```

---

## JSON 範例

```json
[
  {
    "issue": "停車",
    "trend": "up",
    "change_percent": 31,
    "district": "西區",
    "summary": "夜市與市場周邊停車問題增加",
    "recommended_action": "夜間停車與動線規劃"
  },
  {
    "issue": "通學安全",
    "trend": "up",
    "change_percent": 18,
    "district": "西區",
    "summary": "學校周邊接送與人行問題增加",
    "recommended_action": "通學步道盤點"
  }
]
```

---

## 趨勢分類

| trend | 說明 |
|---|---|
| up | 增加 |
| down | 減少 |
| stable | 穩定 |
| spike | 短期暴增 |

---

## 後續應用

- dashboard 趨勢區塊
- 城市週報
- AI 摘要
- 社群貼文
- 拜訪里鄰優先順序
- 政見研究

---

## 長期目標

建立：

# 嘉義城市故障指數

例如：

- 停車壓力指數
- 通學安全指數
- 道路故障指數
- 夜間照明指數
- 生活品質指數
