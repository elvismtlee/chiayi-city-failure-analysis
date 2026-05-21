# 城市故障議題分類字典 v1

本文件定義「嘉義市 12 年城市故障分析資料庫」的議題分類標準。

---

## 設計目的

議題分類字典用於：

1. 1999 / 陳情案件分類
2. 議員質詢 metadata 分類
3. 城市故障回報分類
4. 熱點地圖分類
5. AI 摘要與週報生成
6. 社群文案與短影音題材整理

---

## 第一層分類

| code | 類別 | 說明 |
|---|---|---|
| traffic | 交通 | 停車、車流、號誌、違停、交通壅塞 |
| road | 道路 | 路平、坑洞、路面破損、道路施工 |
| pedestrian | 人行 | 人行道、行人動線、無障礙、騎樓通行 |
| environment | 環境 | 垃圾、噪音、髒亂、空污、異味 |
| drainage | 水利排水 | 淹水、側溝、排水不良、雨水下水道 |
| safety | 公共安全 | 治安、照明、危險路口、公共設施安全 |
| market | 市場商圈 | 市場動線、攤商、卸貨、商圈環境 |
| park | 公園休憩 | 公園設施、綠地、兒童遊具、休憩空間 |
| school | 教育學區 | 通學安全、校園周邊、學區生活議題 |
| senior | 社福高齡 | 長照、高齡友善、社福服務、弱勢協助 |
| culture | 文化觀光 | 文化活動、觀光動線、歷史街區、藝文場域 |
| administration | 行政服務 | 局處服務、陳情處理、行政效率、資訊公開 |
| other | 其他 | 無法歸入上述類別者 |

---

## 第二層標籤範例

### traffic

- parking
- illegal_parking
- traffic_light
- congestion
- motorcycle
- bus
- loading_zone

### road

- pothole
- road_surface
- construction
- road_marking
- sidewalk_edge

### pedestrian

- sidewalk
- arcade
- barrier_free
- pedestrian_crossing
- school_route

### environment

- garbage
- noise
- odor
- dirty
- air_pollution
- recycling

### drainage

- flooding
- ditch
- sewer
- rainwater
- drainage_blocked

### safety

- lighting
- dangerous_intersection
- public_facility
- night_safety
- traffic_safety

### market

- market_traffic
- unloading
- vendor
- waste_collection
- crowd_flow

### school

- school_commute
- parent_pickup
- crossing_guard
- school_zone
- student_safety

---

## 分類原則

1. 每筆資料至少應有一個第一層分類。
2. 可有多個第二層標籤。
3. 若資料不足，先標為 `other`，不可強行分類。
4. 同一案件可同時屬於多個議題，例如「市場周邊違停造成行人危險」可標為 traffic、pedestrian、market。
5. AI 自動分類結果應可人工校正。

---

## 建議輸出欄位

```json
{
  "primary_issue": "traffic",
  "secondary_tags": ["parking", "illegal_parking"],
  "confidence": 0.82,
  "classification_method": "ai_assisted",
  "review_status": "unreviewed"
}
```

---

## review_status

| status | 說明 |
|---|---|
| unreviewed | 尚未人工檢查 |
| reviewed | 已人工檢查 |
| corrected | AI 分類後經人工修正 |
| uncertain | 資料不足，分類不確定 |

---

## 對外呈現名稱

對外頁面不一定顯示英文 code，建議轉成中文：

| code | display_name |
|---|---|
| traffic | 交通停車 |
| road | 道路路平 |
| pedestrian | 人行安全 |
| environment | 環境衛生 |
| drainage | 排水防汛 |
| safety | 公共安全 |
| market | 市場商圈 |
| park | 公園休憩 |
| school | 通學安全 |
| senior | 社福高齡 |
| culture | 文化觀光 |
| administration | 行政服務 |
| other | 其他議題 |

---

## 注意事項

本分類字典是城市治理分析工具，不是責任歸屬判定工具。分類結果只能表示資料中的議題類型，不代表單一局處或個人的責任結論。
