# 嘉義在地地名字典 v1

本文件定義本專案使用的嘉義在地地名資料結構，作為 dashboard、AI 摘要、週報、現場行動與 sample data 的共同參考。

---

## 目的

避免地名在不同地方出現不同寫法，或使用不符合在地語感的稱呼。

資料流程應改成：

```text
原始地點文字
→ 對照在地地名字典
→ 產生標準顯示名稱
→ 套用 aliases / avoid_terms
→ dashboard / 週報 / 社群文案使用一致名稱
```

---

## 建議檔案位置

機器可讀版本：

```text
dashboard/data/local_place_dictionary.json
```

未來若要轉 CSV：

```text
data/reference/local_place_dictionary.csv
```

---

## 欄位定義

| 欄位 | 類型 | 說明 |
|---|---|---|
| place_id | string | 穩定 ID |
| display_name | string | 對外顯示名稱 |
| local_name | string | 嘉義人日常稱呼 |
| formal_name | string/null | 較正式或資料表名稱 |
| aliases | array | 可接受別名 |
| avoid_terms | array | 不建議或禁用稱呼 |
| district | string | 行政區或區域描述 |
| place_type | string | business_district / market / station / road_segment / school_area / park / public_space |
| issue_tags | array | 常見議題 |
| geo_precision | string | landmark / road_segment / district / unknown |
| public_note | string | 對外說明 |
| updated_at | string | 更新日期 |

---

## JSON 範例

```json
{
  "place_id": "place-wenhua-road-business-district",
  "display_name": "文化路商圈",
  "local_name": "文化路",
  "formal_name": "文化路商圈",
  "aliases": ["文化路周邊", "文化路商圈周邊"],
  "avoid_terms": ["文化路夜市", "嘉義市中心夜市區", "嘉義著名夜市觀光區"],
  "district": "西區 / 東區交界",
  "place_type": "business_district",
  "issue_tags": ["traffic", "parking", "pedestrian", "business_district"],
  "geo_precision": "landmark",
  "public_note": "嘉義人日常多稱文化路或文化路商圈，對外資料不使用文化路夜市。",
  "updated_at": "2026-05-21"
}
```

---

## 第一批地點建議

| display_name | local_name | place_type | 注意事項 |
|---|---|---|---|
| 文化路商圈 | 文化路 | business_district | 不用文化路夜市 |
| 嘉義火車站前站 | 火車站前站 | station | 可加前站 / 後站區分 |
| 北興市場周邊 | 北興市場 | market | 市場周邊動線與停車 |
| 中央廣場周邊 | 中央廣場 | public_space | 公共空間與活動動線 |
| 民生南路部分路段 | 民生南路 | road_segment | 需標示部分路段 |
| 新民路部分路段 | 新民路 | road_segment | 需標示部分路段 |
| 世賢路部分路段 | 世賢路 | road_segment | 需標示部分路段 |
| 學校周邊通學路線 | 學校周邊 | school_area | 不指涉單一學校時可用通稱 |
| 公園周邊 | 公園周邊 | park | 未指定公園時保留通稱 |

---

## 與 validation 的關係

本文件與以下文件配合：

```text
docs/local_terminology_style_guide.md
docs/local_terms_validation_rules.md
```

未來 pytest 應檢查：

1. public-facing 檔案不可出現 avoid_terms。
2. dashboard 熱點名稱應優先使用 display_name。
3. AI 摘要若輸入 aliases，輸出應轉為 display_name 或 local_name。

---

## AI 使用規則

AI 產生文案時：

- 對外標題使用 `display_name`
- 口語文案可使用 `local_name`
- 不使用 `avoid_terms`
- 若原始資料出現 avoid_terms，應轉換成建議名稱

範例：

```text
原始輸入：文化路夜市附近停車問題
建議輸出：文化路商圈周邊停車與人行動線議題
```

---

## 原則

```text
地名標準化不是為了官僚化，而是為了讓資料更像嘉義人整理的資料。
```
