# 城市故障熱點 GeoJSON 契約 v1

本文件定義嘉義城市故障熱點地圖系統的 GeoJSON 資料契約，供後續 Leaflet、heatmap、cluster、行政區圖層、里別圖層與路段圖層使用。

本契約屬於 Issue #3 的第一階段資料規格，不涉及真實個資，也不包含 geocoding API key。

---

## 一、核心原則

1. 對外地圖資料只呈現統計、分類與摘要，不呈現個人姓名、電話、email、完整住址。
2. 地點精度依資料來源分級，資料不足時不得假裝精準。
3. 熱點資料必須能回溯資料來源與更新時間。
4. GeoJSON 只作為視覺化資料，不等於完整民意調查。
5. 地圖 popup 不做人身攻擊、不做無來源指控、不做支持度推論。

---

## 二、檔案建議位置

```text
dashboard/data/hotspots.geojson
dashboard/data/village_layers.geojson
dashboard/data/road_segments.geojson
dashboard/data/heatmap_points.geojson
```

第一階段優先建立：

```text
dashboard/data/hotspots.geojson
```

---

## 三、hotspots.geojson 結構

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "updated_at": "2026-05-21",
    "source": "dashboard/data/hotspots.json",
    "status": "prototype",
    "geo_precision_note": "部分座標為 prototype fallback，待正式 geocoding 更新。"
  },
  "features": [
    {
      "type": "Feature",
      "id": "hotspot-wenhua-road-business-district",
      "geometry": {
        "type": "Point",
        "coordinates": [120.4497, 23.4808]
      },
      "properties": {
        "name": "文化路商圈",
        "district": "西區 / 東區交界",
        "category": "停車 / 人行",
        "department": "交通處",
        "score": 92,
        "action": "商圈動線與停車熱點專案",
        "issue_tags": ["traffic", "parking", "pedestrian"],
        "source_count": 0,
        "geo_precision": "prototype",
        "review_status": "prototype"
      }
    }
  ]
}
```

GeoJSON coordinates 順序必須是：

```text
[lng, lat]
```

---

## 四、Feature 必填欄位

### geometry

| 欄位 | 型別 | 說明 |
|---|---|---|
| type | string | 第一階段使用 Point |
| coordinates | array | `[lng, lat]` |

### properties

| 欄位 | 型別 | 說明 |
|---|---|---|
| name | string | 對外顯示熱點名稱 |
| district | string | 行政區或交界說明 |
| category | string | 主要議題分類 |
| department | string | 可能相關局處 |
| score | number | 城市故障指數，0–100 |
| action | string | 建議行動 |
| issue_tags | array | 機器可讀議題標籤 |
| source_count | number | 來源資料筆數 |
| geo_precision | string | 地理精度 |
| review_status | string | 審核狀態 |

---

## 五、geo_precision 合法值

```text
exact
road_segment
landmark
village
district
prototype
unknown
```

說明：

| 值 | 說明 |
|---|---|
| exact | 已確認精準點位 |
| road_segment | 僅能定位到路段 |
| landmark | 僅能定位到地標或商圈 |
| village | 僅能定位到里別 |
| district | 僅能定位到行政區 |
| prototype | 原型座標，不可視為正式點位 |
| unknown | 無法定位 |

---

## 六、review_status 合法值

```text
verified
reviewed
prototype
uncertain
rejected
```

第一階段 prototype 資料應使用：

```text
prototype
```

資料不足但仍需暫時呈現時使用：

```text
uncertain
```

---

## 七、禁止欄位

GeoJSON 對外檔案不得包含：

```text
phone
mobile
email
national_id
id_number
full_address
address
name_of_reporter
```

若來源資料含個資，必須先在 processor 階段去識別化。

---

## 八、地圖 popup 顯示欄位

建議顯示：

```text
熱點名稱
行政區 / 區域
主要議題
城市故障指數
可能相關局處
建議行動
資料狀態
```

不顯示：

```text
個人姓名
電話
email
完整住址
未查證指控
支持度推論
```

---

## 九、與現有檔案關係

目前 `dashboard/data/hotspots.json` 是 dashboard table 與 prototype 地圖使用的資料。

未來可以新增 converter：

```text
scripts/build_hotspots_geojson.py
```

輸入：

```text
dashboard/data/hotspots.json
dashboard/data/local_place_dictionary.json
```

輸出：

```text
dashboard/data/hotspots.geojson
```

---

## 十、驗收標準

1. GeoJSON 可被 Leaflet 讀取。
2. coordinates 使用 `[lng, lat]`。
3. score 介於 0–100。
4. geo_precision 使用合法值。
5. review_status 使用合法值。
6. 不含個資欄位。
7. 不含未查證指控與支持度推論。
8. prototype 座標必須明確標示 prototype。
