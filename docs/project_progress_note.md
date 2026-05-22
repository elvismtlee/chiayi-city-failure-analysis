# 專案進度快照

本文件記錄目前嘉義市城市故障分析資料庫的階段性進度，方便快速交接、檢查下一步與避免重複施工。

---

## 一、目前完成度估算

| 範圍 | 估算完成度 | 說明 |
|---|---:|---|
| 可展示原型 | 82% - 85% | 已具備 dashboard、趨勢、熱點地圖、審核 queue、SOP 與會議紀錄 parser prototype。 |
| 可長期運作系統 | 52% - 55% | 還需正式資料匯入、人工 review 後 processed data、n8n 實際啟用與 1999 資料流程。 |
| 競選與市政研究資料庫雛形 | 65% - 68% | 已可展示方法論與資料流，但公開引用仍需人工審核。 |

---

## 二、已完成基礎

| 類別 | 已完成 |
|---|---|
| Dashboard | 首頁、趨勢頁、熱點地圖、座標審核、影音審核。 |
| Data | hotspots JSON、GeoJSON、geocoding queue、transcript queue。 |
| Parser | CYCC minutes fixture-only parser prototype。 |
| Tests | dashboard JSON、shared nav、local terminology、GeoJSON、parser tests。 |
| Docs | metadata spec、parser spec、review SOP、daily runbook、docs index、acceptance checklist。 |
| Workflow | Dashboard Data workflow 與 Python Tests。 |

---

## 三、進行中任務

目前最重要的下一步是：

```text
CYCC minutes review queue + dashboard
```

目標是把會議紀錄 fixture parser output 轉成：

```text
dashboard/data/cycc_minutes_review_queue.json
dashboard/minutes-review.html
dashboard/minutes-review.js
```

並建立對應測試。

---

## 四、尚未完成的正式系統能力

| 能力 | 狀態 |
|---|---|
| 正式 CYCC PDF / HTML 內容 parser | 尚未接正式來源。 |
| Reviewed minutes processed data | 尚未建立。 |
| 1999 資料匯入 | 尚未確認正式來源與授權方式。 |
| 真實 geocoding 校正 | 仍需人工 review 與可信來源比對。 |
| n8n 實際執行 | 仍需在 n8n 後台匯入與驗收。 |
| 週報自動草稿 | 尚未建立完整資料流。 |

---

## 五、近期不要重做

以下功能已完成第一版，後續只做增量修改：

1. Leaflet 熱點地圖。
2. hotspots GeoJSON builder。
3. 座標審核 queue 與 dashboard。
4. 影音轉錄審核 queue 與 dashboard。
5. CYCC minutes fixture parser prototype。
6. docs index。
7. review workbench SOP。
8. daily ops runbook。
9. CYCC minutes review SOP。

---

## 六、下一步優先順序

| 優先 | 任務 | 目的 |
|---:|---|---|
| 1 | 會議紀錄 review queue dashboard | 推進 issue #1 進入人工審核流程。 |
| 2 | reviewed minutes data schema | 讓人工確認後資料可進入正式分析。 |
| 3 | issue classifier 接 reviewed minutes | 將會議紀錄轉成議題分類。 |
| 4 | weekly summary draft builder | 產出市政議題週報草稿。 |
| 5 | n8n 手動匯入與驗收 | 建立週更流程。 |

---

## 七、使用邊界

1. 未人工 review 的資料不可對外作為正式結論。
2. Prototype 座標不可標為 verified。
3. AI 摘要不可當正式逐字稿。
4. Dashboard 不可稱為民調或支持度調查。
5. 不得輸出私人個資。
6. 不得寫入 token、credential 或 API key。
7. 對外文案應使用中性語氣與可查證來源。

---

## 八、一句話狀態

```text
目前已完成可展示的城市故障分析資料庫原型，正在補齊會議紀錄人工審核流程；距離 production 還需要正式資料源、人工 review 後資料結構、n8n 實際啟用與 1999 資料匯入。
```
