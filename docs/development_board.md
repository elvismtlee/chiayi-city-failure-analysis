# 開發工作看板 v1

本文件整理目前嘉義城市故障分析資料庫的開發任務，方便 ChatGPT、Codex 與人工協作。

---

## A. 已完成

### 資料站基礎

- dashboard/index.html
- dashboard/app.js
- dashboard/insights.html
- dashboard/insights.js
- dashboard/sources.html
- dashboard/methodology.html
- dashboard/reports.html
- dashboard/404.html

### JSON mock data

- dashboard_summary.json
- issue_ranking.json
- hotspots.json
- ai_issue_summary.json
- issue_trends.json
- councilor_issue_analysis.json
- department_performance.json
- urban_failure_scores.json
- data_sources.json
- reports_index.json
- site_map.json

### 文件

- site_architecture.md
- data_governance.md
- public_disclaimer.md
- sources_page_spec.md
- methodology_page_spec.md
- reports_page_spec.md
- codex_resume_plan.md

---

## B. Codex 優先任務

### B1. Dashboard data pipeline

目標：

```text
raw CSV → dashboard JSON
```

狀態：待 Codex 晚上恢復後繼續。

---

### B2. GitHub Actions pipeline

目標：

```text
run crawler / processor / tests / Pages deploy
```

狀態：B1 完成後處理。

---

## C. 下一批功能

### C1. 全站共用導覽列

目標：

讓所有頁面讀取 site_map.json，或抽出共用 nav template。

原因：

避免每新增頁面都要手動改所有 HTML。

---

### C2. Leaflet 真地圖

目標：

把目前 prototype map 改為真 Leaflet / OpenStreetMap。

資料來源：

- hotspots.json
- hotspots.geojson

---

### C3. Issue trend analyzer

目標：

分析 7 / 30 / 90 天議題變化。

輸出：

```text
dashboard/data/issue_trends.json
```

---

### C4. Reports generator

目標：

自動產生：

- dashboard/reports/*.html
- reports/markdown/*.md
- reports/json/*.json

---

### C5. Data sources auto update

目標：

讓 crawler / processor 自動更新 data_sources.json 的筆數與時間。

---

## D. 人工 / ChatGPT 可先做

### D1. 文案優化

- 首頁 hero
- insights summary
- methodology copy
- data disclaimer

### D2. WordPress 整合

- 官網按鈕區塊
- iframe 模組
- data site 導流文案

### D3. n8n 工作流設計

- 每週週報
- Google Sheet 更新
- Gmail 草稿
- GitHub workflow dispatch

---

## E. 注意事項

1. 不要同時多人改同一個檔案。
2. Codex 做程式，ChatGPT 可先做文件與新增頁面。
3. 每個大功能開新 branch / PR。
4. PR merge 前先確認 GitHub Actions。
5. prototype data 必須標示清楚。
