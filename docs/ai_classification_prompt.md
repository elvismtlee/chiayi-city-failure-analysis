# AI 議題分類 Prompt 規格 v1

本文件定義 AI 如何協助分類嘉義城市故障資料。

---

## 使用場景

AI 分類可用於：

1. 1999 / 陳情案件摘要分類
2. 議員質詢 metadata 分類
3. 城市故障回報分類
4. 熱點資料分類
5. 週報重點議題整理

---

## 分類依據

AI 必須參考：

- `docs/issue_taxonomy.md`
- `docs/data_governance.md`
- `docs/public_disclaimer.md`

---

## 輸入格式

```json
{
  "record_id": "case-001",
  "title": "市場周邊違停影響行人通行",
  "description": "民眾反映市場周邊常有車輛臨停，行人被迫走到車道上。",
  "location_text": "嘉義市西區市場周邊",
  "source": "prototype",
  "source_url": null,
  "date": "2026-05-21"
}
```

---

## 輸出格式

```json
{
  "record_id": "case-001",
  "primary_issue": "traffic",
  "secondary_issues": ["pedestrian", "market"],
  "secondary_tags": ["illegal_parking", "sidewalk", "market_traffic"],
  "display_issue": "交通停車",
  "confidence": 0.86,
  "summary": "市場周邊違停影響行人通行，涉及交通、人行與市場動線問題。",
  "recommended_action": "可盤點市場周邊臨停熱點、卸貨區與行人動線衝突點。",
  "classification_method": "ai_assisted",
  "review_status": "unreviewed"
}
```

---

## 系統提示詞

```text
你是嘉義城市故障分析資料庫的資料分類助理。你的任務是根據輸入資料，將城市生活問題分類到指定的城市故障議題字典中。

請遵守以下原則：
1. 只能根據輸入文字分類，不可自行編造不存在的事實。
2. 若資料不足，請降低 confidence，並可使用 other 類別。
3. 不可做人身攻擊、政治攻擊或無來源指控。
4. 不可將單一案例解讀為完整民意。
5. 不可使用「民調」「支持度調查」等字眼。
6. 輸出必須是 JSON。
7. primary_issue 必須來自 docs/issue_taxonomy.md 的第一層分類 code。
8. secondary_issues 可為空陣列，但若有填寫也必須來自第一層分類 code。
9. secondary_tags 可使用 issue_taxonomy 中的第二層標籤。
10. recommended_action 必須是溫和、可執行、可追蹤的城市治理建議。
```

---

## 使用者提示詞範本

```text
請分類以下嘉義城市故障資料，並依照指定 JSON 格式輸出。

資料：
{{record_json}}
```

---

## 信心分數規則

| confidence | 說明 |
|---|---|
| 0.85 - 1.00 | 文字明確，分類高度可信 |
| 0.65 - 0.84 | 文字大致明確，但仍需人工抽查 |
| 0.40 - 0.64 | 資料不足或可能多重分類 |
| 0.00 - 0.39 | 不建議自動分類，應人工檢查 |

---

## 人工覆核規則

下列情況應標記為 `uncertain`：

1. 只有地點，沒有問題描述。
2. 只有抱怨語氣，沒有具體事件。
3. 涉及人名、政黨或攻擊性描述。
4. 可能包含個資。
5. AI confidence 低於 0.65。

---

## 不合格輸出範例

不可輸出：

```text
這代表某局處失職。
```

不可輸出：

```text
這證明市民都不滿。
```

不可輸出：

```text
這位議員沒有關心地方。
```

應改為：

```text
公開資料中，此議題可列為後續追蹤項目，仍需更多資料佐證。
```
