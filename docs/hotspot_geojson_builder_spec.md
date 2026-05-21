# Hotspot GeoJSON Builder Spec v1

本文件定義 `scripts/build_hotspots_geojson.py` 的預期行為，作為 Issue #3「城市故障熱點地圖系統」後續實作依據。

本規格承接：

```text
docs/hotspot_geojson_contract.md
```

---

## 一、目標

建立一支可重複執行的 builder script，把目前 dashboard 使用的熱點資料轉成 GeoJSON。

目標輸出：

```text
dashboard/data/hotspots.geojson
```

此檔未來供 Leaflet、heatmap、cluster、行政區 / 里別 / 路段圖層使用。

---

## 二、輸入檔案

第一階段必讀：

```text
dashboard/data/hotspots.json
```

建議可讀：

```text
dashboard/data/local_place_dictionary.json
```

未來可接：

```text
data/processed/issue_classified_sample.json
dashboard/data/issue_trends.json
```

---

## 三、輸出格式

輸出必須是 GeoJSON FeatureCollection：

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "updated_at": "2026-05-21",
    "source": "dashboard/data/hotspots.json",
    "status": "prototype"
  },
  "features": []
}
```

每個 feature 必須符合：

```text
docs/hotspot_geojson_contract.md
```

---

## 四、座標處理規則

### 1. 有正式座標

若 hotspot item 已含：

```text
lat
lng
```

且皆為有效數字，直接輸出：

```json
"coordinates": [lng, lat]
```

### 2. 沒有正式座標

若只有 prototype `x` / `y` 或完全沒有座標：

1. 使用嘉義市中心附近 prototype fallback 座標。
2. `geo_precision` 設為 `prototype`。
3. `review_status` 設為 `prototype`。
4. metadata 必須標示 `status: prototype`。
5. popup / summary 不可暗示為正式點位。

---

## 五、欄位對應

| hotspots.json | GeoJSON properties |
|---|---|
| name | name |
| district | district |
| category | category |
| department | department |
| score | score |
| action | action |
| place_id | place_id，可選 |

另外 builder 應補：

```text
issue_tags
source_count
geo_precision
review_status
```

---

## 六、issue_tags 推論

第一階段可用簡單 rule-based keyword mapping。

例：

| 關鍵字 | issue_tags |
|---|---|
| 停車 | traffic, parking |
| 人行 | pedestrian |
| 垃圾 | environment |
| 市場 | market |
| 商圈 | market |
| 通學 | school |
| 排水 | drainage |
| 公共安全 | safety |

資料不足時可輸出空陣列，但不可亂猜正式分類。

---

## 七、驗證規則

builder 產生後應檢查：

1. 輸出為 FeatureCollection。
2. `features` 為 list。
3. 每個 feature 有 `type: Feature`。
4. geometry type 第一階段為 `Point`。
5. coordinates 順序為 `[lng, lat]`。
6. score 介於 0–100。
7. geo_precision 為契約合法值。
8. review_status 為契約合法值。
9. 不包含個資欄位。
10. prototype 座標必須標示 prototype。

---

## 八、建議測試

未來實作時新增：

```text
tests/test_build_hotspots_geojson.py
```

測試案例：

1. builder 可產生 `dashboard/data/hotspots.geojson`。
2. GeoJSON 可 parse。
3. features 數量等於或大於 `hotspots.json` 熱點數。
4. coordinates 是 `[lng, lat]`。
5. prototype fallback 會標示 `geo_precision: prototype`。
6. score 範圍合法。
7. 不包含個資欄位。

---

## 九、建議命令

```bash
python scripts/build_hotspots_geojson.py
pytest -q tests/test_build_hotspots_geojson.py
pytest -q tests/test_dashboard_json_validation.py
pytest -q
```

---

## 十、下一步 UI 串接

產生 `hotspots.geojson` 後，`dashboard/leaflet-map.js` 可改為：

1. 優先讀取 `dashboard/data/hotspots.geojson`。
2. 若不存在或失敗，再 fallback 到 `dashboard/data/hotspots.json`。
3. popup 顯示 `properties`。
4. prototype feature 顯示資料限制標籤。

---

## 十一、安全與法遵

1. 不使用私人地址作為公開點位。
2. 不公開個人通報者資料。
3. 不把 geocoding API key 寫入 repo。
4. 不把 prototype 座標說成正式座標。
5. 不用地圖資料推論支持度、個人評價或民調結果。
