# 地點標準化與熱點定位規格 v1

本文件定義 1999、陳情資料、議員質詢與城市故障回報中的地點文字如何轉成可分析的地理資料。

---

## 目標

將不同來源中的地點描述整理成可用於：

1. 熱點地圖
2. 里別統計
3. 路段統計
4. 城市故障分數
5. 週報與現場走訪清單

---

## 地點資料來源

常見輸入可能包含：

- 完整地址
- 路名
- 路口
- 地標
- 市場 / 學校 / 公園名稱
- 里名
- 模糊描述，例如「文化路附近」或「文化路商圈周邊」

---

## 標準化欄位

建議輸出：

```json
{
  "location_text_raw": "文化路附近",
  "location_text_normalized": "嘉義市文化路商圈周邊",
  "district": "西區",
  "village": null,
  "road": "文化路",
  "intersection": null,
  "landmark": "文化路商圈",
  "lat": 23.4800,
  "lng": 120.4490,
  "geo_precision": "landmark",
  "geo_method": "manual_seed",
  "geo_review_status": "unreviewed"
}
```

---

## geo_precision

| precision | 說明 |
|---|---|
| exact_address | 精確地址 |
| intersection | 路口 |
| road_segment | 路段 |
| landmark | 地標 |
| village | 里別 |
| district | 行政區 |
| city | 只知道嘉義市 |
| unknown | 無法判斷 |

---

## geo_method

| method | 說明 |
|---|---|
| source_coordinate | 原始資料已提供經緯度 |
| geocoding_api | 使用地理編碼 API |
| manual_seed | 人工建立常見地標座標 |
| keyword_match | 關鍵字對應 |
| fallback | 無法定位時使用 fallback |

---

## geo_review_status

| status | 說明 |
|---|---|
| unreviewed | 尚未人工檢查 |
| reviewed | 已人工檢查 |
| corrected | 已修正 |
| uncertain | 位置不確定 |

---

## 嘉義市常見地標 seed list

第一階段可先建立人工 seed：

| landmark | district | suggested_category |
|---|---|---|
| 文化路商圈 | 西區 / 東區交界 | market / traffic |
| 嘉義火車站 | 西區 | traffic |
| 北興市場 | 西區 | market |
| 嘉義市政府 | 東區 | administration |
| 中央廣場 | 西區 | culture / public_space |
| 蘭潭 | 東區 | park / tourism |
| 檜意森活村 | 東區 | culture / tourism |

---

## 地址隱私處理

若來源為使用者回報，不應公開完整住家地址。

公開資料建議降精度：

| 原始資料 | 對外呈現 |
|---|---|
| 完整住址 | 路段 / 里別 |
| 門牌號碼 | 移除 |
| 個人住家描述 | 去識別化 |
| 學校 / 公園 / 市場 | 可用地標 |

---

## 熱點聚合原則

1. 同一地標附近資料可聚合成熱點。
2. 同一路段多筆資料可聚合為 road_segment。
3. 位置不明資料不可強行放到地圖。
4. 若座標不確定，應標示 `geo_review_status: uncertain`。
5. 對外地圖可顯示模糊點位，不顯示個人精確地址。

---

## 後續輸出

可產生：

```text
dashboard/data/hotspots.geojson
dashboard/data/location_index.json
data/processed/location_normalized.csv
```
