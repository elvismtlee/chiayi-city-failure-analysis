# 地名人工確認工作表規格 v1

本文件定義用 Google Sheet 或 CSV 收集、審核、確認嘉義在地地名的欄位格式。

目的不是直接取代 `local_place_dictionary.json`，而是建立一個「待確認 → 已確認 → 匯入正式字典」的流程。

---

## 建議工作表名稱

```text
place_name_review
```

---

## 欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| review_id | Y | review-0001 |
| raw_name | Y | 原始地名或來源文字 |
| suggested_display_name | Y | 建議對外顯示名稱 |
| local_name | N | 嘉義人日常說法 |
| formal_name | N | 正式名稱 |
| district | Y | 西區 / 東區 / 全市 / unknown |
| place_type | Y | business_district / market / station / road_segment / school_area / park / public_space / other |
| aliases | N | 可接受別名，逗號分隔 |
| avoid_terms | N | 不建議用語，逗號分隔 |
| issue_tags | N | 常見議題標籤，逗號分隔 |
| geo_precision | Y | landmark / road_segment / district / unknown |
| source | N | 來源，例如人工、公開資料、表單、週報 |
| review_status | Y | pending / reviewed / approved / rejected |
| reviewer | N | 確認人 |
| reviewed_at | N | 確認日期 |
| notes | N | 備註 |

---

## review_status

| 狀態 | 說明 |
|---|---|
| pending | 尚未確認 |
| reviewed | 已看過但尚未決定 |
| approved | 可加入正式地名字典 |
| rejected | 不建議使用 |

---

## 範例

```csv
review_id,raw_name,suggested_display_name,local_name,formal_name,district,place_type,aliases,avoid_terms,issue_tags,geo_precision,source,review_status,reviewer,reviewed_at,notes
review-0001,文化路附近,文化路商圈,文化路,文化路商圈,西區 / 東區交界,business_district,"文化路周邊,文化路商圈周邊",文化路夜市,"traffic,parking,pedestrian,business_district",landmark,人工,approved,在地確認,2026-05-21,嘉義人日常多稱文化路或文化路商圈
```

---

## 匯入正式字典前檢查

加入 `dashboard/data/local_place_dictionary.json` 前，必須確認：

- [ ] review_status 為 approved
- [ ] suggested_display_name 不含禁用詞
- [ ] local_name 符合嘉義在地說法
- [ ] aliases 是可接受別名
- [ ] avoid_terms 已列出容易誤用名稱
- [ ] geo_precision 合法
- [ ] place_type 合法
- [ ] issue_tags 不亂填

---

## 使用流程

```text
收集原始地名
→ 填入 place_name_review
→ 人工確認
→ review_status 改為 approved
→ 匯入 local_place_dictionary.json
→ 執行 pytest
→ dashboard / 週報 / AI 摘要使用
```

---

## 原則

```text
沒有確認過的地名，不直接進正式字典。
```
