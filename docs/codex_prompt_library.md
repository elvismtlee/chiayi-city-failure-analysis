# Codex 指令庫 v1

本文件整理可直接貼給 Codex 的任務指令。

---

## 1. 狀態檢查指令

```text
請先不要修改任何檔案。
請檢查目前 repo 狀態，回報：
1. 目前 branch
2. main 是否最新
3. 是否有 uncommitted changes
4. open PR 狀態
5. GitHub Actions 狀態
6. 下一步建議
```

---

## 2. Dashboard data pipeline 指令

```text
請依照 docs/codex_resume_plan.md，從最新 main 開新 branch：

codex/build-dashboard-data-pipeline

目標：建立 dashboard data pipeline。

請讓 src/processors/build_dashboard_data.py 可以讀取：
- data/raw/cycc_minutes_metadata.csv
- data/raw/cycc_question_video_metadata.csv

並產生或更新：
- dashboard/data/dashboard_summary.json
- dashboard/data/issue_ranking.json
- dashboard/data/hotspots.json
- dashboard/data/ai_issue_summary.json

要求：
1. raw CSV 不存在時使用 fallback mock data，不要失敗。
2. 加入 pytest。
3. 執行 pytest。
4. 不要大幅改 UI。
5. 不要修改無關檔案。
6. 完成後開 PR，標題：Build dashboard data pipeline。
```

---

## 3. 全站導覽指令

```text
請處理 Issue #11：重構全站共用導覽列與 footer。

要求：
1. 參考 dashboard/data/site_map.json。
2. 讓 index.html、insights.html、sources.html、methodology.html、reports.html、404.html 導覽一致。
3. 每頁需有 active 狀態。
4. footer 放資料聲明短版。
5. 不破壞既有 JSON rendering。
6. 手機版可用。
7. 完成後開 PR。
```

---

## 4. Leaflet 地圖指令

```text
請處理 Issue #6：建立第一版 Leaflet 熱點地圖。

目標：把 prototype 假地圖升級為 Leaflet.js / OpenStreetMap。

要求：
1. 讀取 dashboard/data/hotspots.json。
2. 若有 lat/lng，顯示 marker。
3. 若沒有 lat/lng，保留 prototype fallback。
4. marker popup 顯示 name、category、score、department、action。
5. 不破壞首頁其他區塊。
6. 完成後開 PR。
```

---

## 5. Issue trend analyzer 指令

```text
請處理 Issue #7：建立 issue trend analyzer。

目標：產生 dashboard/data/issue_trends.json。

要求：
1. 支援 7 / 30 / 90 天。
2. 計算 change_percent。
3. 判斷 up / down / stable / spike。
4. raw data 不足時輸出 fallback prototype data。
5. 加入 pytest。
6. 完成後開 PR。
```

---

## 6. 資料來源頁指令

```text
請處理 Issue #9：建立資料來源頁 sources.html。

若頁面已存在，請檢查並改善：
1. data_sources.json 格式是否正確。
2. sources.html 是否可讀取 JSON。
3. 是否顯示 status / latest_update / record_count。
4. 是否有資料聲明。
5. 導覽是否一致。
6. 不要稱為民調。
```

---

## 7. PR review 修正指令

```text
請依照 PR review comments 修正。

注意：
1. 只修 review 提到的範圍。
2. 不要順手重構無關檔案。
3. 修完後執行測試。
4. 回報修正摘要與測試結果。
```

---

## 8. 緊急 hotfix 指令

```text
GitHub Pages 目前顯示異常。請從最新 main 開 hotfix branch，檢查：
1. dashboard/index.html
2. dashboard/app.js
3. dashboard/data/*.json
4. GitHub Pages workflow

只修造成頁面壞掉的最小範圍。
完成後開 PR，標題：Hotfix GitHub Pages dashboard。
```
