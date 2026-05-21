# Codex 晚上接續計畫

本文件供 Codex 在用量恢復後接續使用。

---

## 目前狀態

Codex 已完成或正在處理：

1. Issue #4：CYCC metadata crawler
2. PR #8：已產生 metadata crawler 結果
3. 抓到資料：
   - data/raw/cycc_minutes_metadata.csv：10 筆
   - data/raw/cycc_question_video_metadata.csv：131 筆
4. pytest：17 passed
5. GitHub Actions：Python Tests passed

---

## 晚上恢復後第一步

請先不要直接繼續寫 code。

請先執行：

```text
檢查目前 main 與 PR branch 狀態，確認是否有 merge conflict。
```

需要回報：

1. PR #8 是否已 merge。
2. main 是否包含最新 dashboard / docs 檔案。
3. 目前工作目錄是否乾淨。
4. 是否需要 rebase / pull 最新 main。
5. 下一個 branch 建議名稱。

---

## 安全接續順序

### Step 1：同步 main

```bash
git checkout main
git pull origin main
```

### Step 2：確認 PR #8 狀態

若 PR #8 尚未 merge，先不要基於舊 main 開新任務。

### Step 3：建立新 branch

建議 branch：

```bash
git checkout -b codex/build-dashboard-data-pipeline
```

---

## 下一個 Codex 任務

任務名稱：

```text
Build dashboard data pipeline
```

目標：

讓 crawler 輸出的 raw CSV 可以轉成 dashboard 使用的 JSON。

需要處理：

1. src/processors/build_dashboard_data.py
2. dashboard/data/dashboard_summary.json
3. dashboard/data/issue_ranking.json
4. dashboard/data/hotspots.json
5. dashboard/data/ai_issue_summary.json
6. pytest
7. GitHub Actions

---

## 避免衝突規則

請避免一次大幅重寫：

- dashboard/index.html
- dashboard/insights.html
- dashboard/app.js
- dashboard/insights.js

除非有明確 bug。

若要改 UI，應另開 branch。

---

## 測試要求

至少執行：

```bash
python src/processors/build_dashboard_data.py
pytest
```

若 GitHub Actions 有更新，也需確認 workflow 可以通過。

---

## PR 要求

PR 標題：

```text
Build dashboard data pipeline
```

PR 描述需包含：

1. 修改哪些檔案
2. 讀取哪些 CSV
3. 產生哪些 JSON
4. fallback mock data 如何運作
5. 測試結果
6. 是否影響 GitHub Pages

---

## 下一階段任務候選

完成 dashboard data pipeline 後，下一批任務：

1. 全站共用導覽列
2. Leaflet 真地圖
3. issue trend analyzer
4. reports generator
5. data source status auto update
6. method / disclaimer footer integration
