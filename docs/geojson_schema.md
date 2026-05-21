# GeoJSON 與地理資料格式 v1

本文件定義嘉義城市故障分析平台的地理資料格式。

## 目的

讓熱點地圖、里別圖層、路段圖層與未來 1999 密度圖可以共用一致格式。

---

## 第一階段：hotspots.geojson

位置：

```text
dashboard/data/hotspots.geojson
```

用途：Leaflet 地圖顯示城市故障熱點。

### Feature 欄位

| 欄位 | 說明 |
|---|---|
| name | 熱點名稱 |
| district | 行政區 |
| category | 主要議題 |
| department | 對應局處 |
| score | 城市故障指數 |
| action | 建議行動 |
| source | 資料來源 |

---

## 範例

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "文化路商圈",
        "district": "西區 / 東區交界",
        "category": "停車 / 人行",
        "department": "交通處",
        "score": 92,
        "action": "商圈動線與停車熱點專案",
        "source": "prototype"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [120.449, 23.480]
      }
    }
  ]
}
```

---

## 第二階段：village layer

未來可加入：

```text
dashboard/data/chiayi_villages.geojson
```

用途：

- 里別案件數
- 里別城市故障指數
- 里別拜訪優先順序

---

## 第三階段：road segment layer

未來可加入：

```text
dashboard/data/road_segments.geojson
```

用途：

- 道路坑洞
- 路平問題
- 交通事故熱點
- 人行道斷點

---

## 坐標系統

採用：

```text
WGS84 EPSG:4326
```

Leaflet / OpenStreetMap 可直接使用。
