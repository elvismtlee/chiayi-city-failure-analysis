# 改善追蹤 Schema v1

本文件定義城市故障議題從發現、紀錄、送出建議、收到回應到改善追蹤的資料格式。

---

## 目的

讓城市故障資料不只是顯示問題，而是能追蹤後續處理與改善進度。

流程：

```text
issue identified
→ field observed
→ documented
→ submitted
→ responded
→ improved / monitoring
```

---

## 建議檔案位置

### CSV

```text
data/processed/action_tracking.csv
```

### JSON

```text
dashboard/data/action_tracking.json
```

---

## 欄位定義

| 欄位 | 類型 | 說明 |
|---|---|---|
| tracking_id | string | 改善追蹤 ID |
| issue_title | string | 議題標題 |
| related_hotspot_id | string/null | 對應熱點 ID |
| related_observation_id | string/null | 對應現場觀察 ID |
| primary_issue | string | 主要議題 code |
| district | string | 行政區 |
| location_display | string | 對外顯示地點 |
| status | string | observed / documented / submitted / responded / improved / monitoring / closed |
| current_summary | string | 目前狀態摘要 |
| recommended_action | string | 建議行動 |
| responsible_unit | string/null | 可能相關單位，若不確定填 null |
| submitted_at | date/null | 送出建議或陳情日期 |
| responded_at | date/null | 收到回應日期 |
| last_checked_at | date/string | 最近追蹤日期 |
| next_check_at | date/string/null | 下次追蹤日期 |
| public_note | string | 對外說明 |
| data_status | string | internal / deidentified / published |
| updated_at | datetime/string | 更新時間 |

---

## JSON 範例

```json
{
  "tracking_id": "track-2026-0001",
  "issue_title": "文化路夜市周邊人行安全",
  "related_hotspot_id": "hotspot-cultural-road-night-market",
  "related_observation_id": "field-2026-0001",
  "primary_issue": "traffic",
  "district": "西區",
  "location_display": "文化路夜市周邊",
  "status": "documented",
  "current_summary": "已完成現場觀察，初步整理臨停與人行動線重疊問題。",
  "recommended_action": "盤點臨停熱點、卸貨時段與行人穿越動線。",
  "responsible_unit": null,
  "submitted_at": null,
  "responded_at": null,
  "last_checked_at": "2026-05-21",
  "next_check_at": "2026-06-01",
  "public_note": "此議題已列入後續追蹤，仍需更多資料與現場觀察佐證。",
  "data_status": "deidentified",
  "updated_at": "2026-05-21 19:30:00"
}
```

---

## status 定義

| status | 說明 |
|---|---|
| observed | 已發現或現場觀察 |
| documented | 已整理資料 |
| submitted | 已送出建議或陳情 |
| responded | 已收到回應 |
| improved | 已觀察到改善 |
| monitoring | 持續觀察中 |
| closed | 結案或停止追蹤 |

---

## dashboard 呈現方式

可呈現：

- 議題名稱
- 地點
- 狀態
- 最近追蹤日期
- 下一步
- 對外說明

避免呈現：

- 個人聯絡資料
- 未公開公文細節
- 未確認責任歸屬
- 攻擊性描述

---

## 對外語氣範例

建議：

```text
此議題已列入後續追蹤，將持續蒐集現場觀察與公開資料，並整理可能改善方向。
```

避免：

```text
這證明某局處失職。
```

---

## 驗收規則

- [ ] tracking_id 不可空白
- [ ] status 必須符合定義
- [ ] primary_issue 必須符合 issue_taxonomy
- [ ] data_status 為 published 時不可含個資
- [ ] responsible_unit 不確定時填 null，不可亂填
