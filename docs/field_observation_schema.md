# 現場觀察紀錄 Schema v1

本文件定義現場走訪、拍照、影片紀錄與地方觀察資料的標準格式。

---

## 目的

讓 dashboard 發現的城市故障熱點，可以被現場確認，並回寫成可追蹤資料。

資料流程：

```text
dashboard hotspot
→ field observation
→ privacy check
→ issue classification
→ action tracking
→ weekly report
→ dashboard update
```

---

## 建議檔案位置

### CSV

```text
data/processed/field_observations.csv
```

### JSON

```text
dashboard/data/field_observations.json
```

---

## 欄位定義

| 欄位 | 類型 | 說明 |
|---|---|---|
| observation_id | string | 現場觀察 ID |
| related_hotspot_id | string/null | 對應熱點 ID |
| observed_at | datetime/string | 觀察時間 |
| observer_role | string | volunteer / staff / public |
| location_name | string | 地點名稱 |
| district | string | 行政區 |
| location_text | string | 地點文字描述 |
| geo_precision | string | exact_address / intersection / road_segment / landmark / village / district / unknown |
| lat | number/null | 緯度，若可公開才填 |
| lng | number/null | 經度，若可公開才填 |
| primary_issue | string | 主要議題 code |
| secondary_issues | array | 次要議題 code |
| observation_summary | string | 去識別化後摘要 |
| evidence_type | array | photo / video / note / public_record |
| photo_count | number | 照片數 |
| video_count | number | 影片數 |
| privacy_checked | boolean | 是否已檢查個資 |
| publish_status | string | internal / deidentified / published |
| recommended_action | string | 建議行動 |
| created_at | datetime/string | 建立時間 |
| updated_at | datetime/string | 更新時間 |

---

## JSON 範例

```json
{
  "observation_id": "field-2026-0001",
  "related_hotspot_id": "hotspot-wenhua-road-business-district",
  "observed_at": "2026-05-21 18:30:00",
  "observer_role": "staff",
  "location_name": "文化路商圈周邊",
  "district": "西區",
  "location_text": "文化路商圈周邊路段",
  "geo_precision": "landmark",
  "lat": null,
  "lng": null,
  "primary_issue": "traffic",
  "secondary_issues": ["pedestrian", "market"],
  "observation_summary": "尖峰時段臨停與行人動線重疊，建議盤點臨停熱點與行人穿越動線。",
  "evidence_type": ["photo", "note"],
  "photo_count": 4,
  "video_count": 1,
  "privacy_checked": true,
  "publish_status": "deidentified",
  "recommended_action": "盤點臨停熱點、卸貨時段與行人穿越動線。",
  "created_at": "2026-05-21 19:00:00",
  "updated_at": "2026-05-21 19:00:00"
}
```

---

## publish_status

| 狀態 | 說明 |
|---|---|
| internal | 內部紀錄，不公開 |
| deidentified | 已去識別化，可用於統計或摘要 |
| published | 可公開展示 |
| withheld | 因隱私或授權疑慮暫不公開 |

---

## 隱私規則

不可公開：

- 可識別個人正臉
- 車牌特寫
- 完整住家地址
- 門牌號碼
- 個人電話、email、LINE ID
- 未經同意的對話內容

---

## dashboard 可呈現內容

可公開顯示：

- 去識別化摘要
- 議題分類
- 模糊地點
- 觀察月份
- 改善建議
- 是否已納入追蹤

不建議公開：

- 原始照片
- 原始影片
- 精確地址
- 原始訪談文字

---

## 與週報的關係

週報可引用：

```text
本週現場觀察顯示，文化路商圈周邊在尖峰時段仍有臨停與人行動線重疊問題，建議後續盤點卸貨區、臨停熱點與行人穿越動線。
```

---

## 驗收規則

- [ ] observation_id 不可空白
- [ ] primary_issue 必須符合 issue_taxonomy
- [ ] privacy_checked 為 false 時不可 published
- [ ] publish_status 為 published 時不可含個資
- [ ] geo_precision 若為 exact_address，公開前應降精度
- [ ] 地名應符合 `docs/local_terminology_style_guide.md`
