# Issue 進度矩陣

本文件整理目前 repo 內主要 issue 的完成狀態、已合併成果、後續可接工作與避免重複施工項目。

更新日期：2026-05-22

---

## 一、整體進度估算

| 範圍 | 估算完成度 | 說明 |
|---|---:|---|
| 可展示原型 | 70% - 75% | 已具備 dashboard、洞察頁、趨勢分析、Leaflet 地圖、GeoJSON、品質測試與 n8n 文件骨架。 |
| production 系統 | 40% - 45% | 仍缺正式 crawler 深度解析、transcript、真實 geocoding、n8n 實際啟用、1999 資料匯入與人工 review 流程。 |

---

## 二、Open issues

| Issue | 主題 | 目前狀態 | 已完成 | 下一步 | 注意事項 |
|---|---|---|---|---|---|
| #1 | 嘉義市議會會議紀錄 crawler | 第一階段未完成 | 已有 metadata crawler 基礎與資料管線相關文件 | 補 PDF / HTML 內容解析規格與測試資料 | 不要直接寫入 Google Sheet credential；不可把 token 寫入 repo。 |
| #2 | 議員質詢影音 metadata crawler | 第一階段未完成 | 已有 metadata crawler 方向與後續 transcript 規劃 | 補影音 metadata 欄位驗證、未來 transcript queue | 不要直接接 Whisper API key；先產生待轉錄清單。 |
| #3 | 城市故障熱點地圖系統 | 進行中，原型已可展示 | Leaflet map、hotspots.geojson、GeoJSON builder、GeoJSON validation、workflow rebuild、shared nav link | 建立 geocoding review queue、人工座標審核流程、未來 village / road layers | 目前座標仍是 prototype fallback，不可標示為 verified。 |
| #10 | n8n 每週資料更新與週報流程 | 文件與範本已完成，尚未實際啟用 | phase1 contract、workflow templates、README、manual acceptance checklist | 實際匯入 n8n 前先跑手動驗收；未來建立 execution log schema | 第一階段不得自動公開發文、不得自動寄出對外 email、不得公開分享 Drive。 |

---

## 三、Closed issues 與已完成成果

| Issue | 主題 | 完成狀態 | 代表成果 |
|---|---|---|---|
| #4 | 第一版 CYCC metadata crawler | 已完成第一階段 | metadata crawler 基礎、raw hash、CSV / JSON 管線。 |
| #6 | 第一版 Leaflet 熱點地圖 | 已完成 | `dashboard/map.html`、`dashboard/leaflet-map.js`，已支援 GeoJSON 優先讀取。 |
| #7 | issue trend analyzer | 已完成 | `src/analyzers/issue_trend_analyzer.py`、`scripts/build_issue_trends.py`、`dashboard/data/issue_trends.json`。 |
| #9 | sources.html | 已完成 | `dashboard/sources.html` 與資料來源呈現。 |
| #11 | 共用導覽列與 footer | 已完成 | `dashboard/shared-nav.js`，包含城市熱點地圖連結。 |
| #12 | AI 議題分類器 prototype | 已完成 | `src/classifiers/issue_classifier.py`、sample builder、classified sample。 |
| #13 | dashboard JSON validation | 已完成並持續擴充 | `tests/test_dashboard_json_validation.py`，已納入 `hotspots.geojson`。 |
| #14 | Dashboard Data GitHub Actions | 已完成並持續擴充 | `.github/workflows/dashboard-data.yml`，已重建 dashboard data 與 hotspot GeoJSON。 |
| #15 | 嘉義在地用語 validation test | 已完成 | `tests/test_local_terminology.py`。 |
| #16 / #21 | 在地用語與地名字典納入 CI | 已完成 | Dashboard Data workflow 已跑 local terminology / place dictionary tests。 |
| #17 | 品質門檻入口文件 | 已完成 | 品質文件與測試入口已整理。 |
| #18 | 地名審核 CSV 匯入流程 | 已完成 | 地名審核流程與相關測試。 |
| #20 | local_place_dictionary 接入 processor | 已完成 | fallback output 使用在地名稱，不再輸出禁用稱呼。 |
| #22 / #24 | Codex PR merge 前品質檢查清單 | 已完成 | merge 前不只看 Actions，也檢查 fallback source、用語與敏感欄位。 |

---

## 四、近期已合併 PR 摘要

| PR | 主題 | 結果 |
|---|---|---|
| #52 / #59 | insights 議題趨勢 UI | 7 / 30 / 90 天分區顯示，含 jump links、anchor、prototype disclosure 與測試。 |
| #54 | Leaflet map 讀取 GeoJSON | 地圖優先讀 `hotspots.geojson`，失敗才 fallback 到 `hotspots.json`。 |
| #55 | 驗證 hotspot GeoJSON | dashboard JSON validation 已納入 GeoJSON schema。 |
| #56 | Dashboard Data workflow 重建 GeoJSON | workflow 會自動執行 `scripts/build_hotspots_geojson.py`。 |
| #58 | shared navigation 加入地圖 | 共用導覽列加入「城市熱點地圖」。 |

---

## 五、不要重做的工作

以下任務已完成或已有穩定第一版，後續只做增量修改：

```text
issue classifier prototype
issue trend analyzer
insights 7 / 30 / 90 天分區 UI
Leaflet 第一版地圖
hotspots.json -> hotspots.geojson builder
Dashboard Data workflow 基礎
shared-nav.js 共用導覽
n8n phase 1 文件與 templates
n8n manual acceptance checklist
```

---

## 六、下一步建議

### 適合 Codex 做

| 優先級 | 任務 | 原因 |
|---:|---|---|
| 1 | 建立 `scripts/build_geocoding_review_queue.py` | 可推進 #3，且不需外部 API key。 |
| 2 | 建立 transcript review queue | 可推進 #2，先建立待轉錄清單，不接 API。 |
| 3 | 建立 council meeting content parser spec / fixture | 可推進 #1，先做測試資料與解析契約。 |

### 適合人工 / n8n 後台做

| 優先級 | 任務 | 原因 |
|---:|---|---|
| 1 | 依 `docs/n8n_manual_acceptance_checklist.md` 匯入 workflow template | 需要 n8n credential store 與手動檢查。 |
| 2 | 手動 review geocoding queue | 需人工確認地點，不宜自動 verified。 |
| 3 | 決定 1999 資料來源與授權方式 | 需確認公開資料、資料取得方式與去識別化策略。 |

---

## 七、用語與資料安全提醒

1. 不要把 prototype data 寫成正式結論。
2. 不要把 `geo_precision: prototype` 的座標標示為 verified。
3. 不要使用「民調」或「支持度調查」描述 dashboard 資料。
4. 不要在 public-facing output 使用不符合嘉義在地語感的稱呼。
5. 不要將 token、secret、credential、webhook secret 寫入 repo。
6. 不要輸出個資欄位，例如 phone、email、address、full_address、national_id。

---

## 八、目前最推薦下一個 PR

```text
Build geocoding review queue
```

目的：

```text
將目前 hotspots.geojson 中 geo_precision 為 prototype / unknown / uncertain 的熱點整理成人工座標審核清單。
```

這一步完成後，#3 會從「地圖原型」進入「正式地理資料校正流程」。
