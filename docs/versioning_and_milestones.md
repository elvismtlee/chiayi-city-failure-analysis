# 版本路線圖與里程碑 v1

本文件定義「嘉義城市故障分析資料庫」從 prototype 到正式資料平台的版本規劃。

---

## v0.1｜靜態原型資料站

### 目標

建立可公開瀏覽的 GitHub Pages 原型站。

### 已完成項目

- 城市儀表板首頁
- 城市洞察分析頁
- 資料來源頁
- 方法論頁
- 城市週報頁
- 404 頁
- mock JSON data
- 基礎文件與規格

### 狀態

```text
已完成主要架構，仍需統一導覽與品質檢查。
```

---

## v0.2｜Crawler 與資料處理 pipeline

### 目標

讓官方公開資料可以進入 dashboard。

### 主要工作

1. CYCC metadata crawler
2. raw CSV 輸出
3. dashboard data processor
4. JSON 自動產生
5. GitHub Actions 測試
6. Pages 自動部署

### 驗收標準

- crawler 可產生 raw CSV
- processor 可產生 dashboard JSON
- pytest 通過
- GitHub Actions 通過
- GitHub Pages 不壞掉

---

## v0.3｜全站導覽與資料透明化

### 目標

讓資料站變成完整小型網站，而不是多個分散 HTML。

### 主要工作

1. 共用導覽列
2. 共用 footer
3. 資料聲明
4. 資料來源狀態自動更新
5. release checklist / QA checklist 套用

---

## v0.4｜真地圖與 GeoJSON

### 目標

把 prototype 假地圖改為真地理資料平台。

### 主要工作

1. Leaflet.js
2. OpenStreetMap
3. hotspots.geojson
4. popup / score / category
5. 未來支援里別與路段 layer

---

## v0.5｜AI 洞察與城市週報

### 目標

把資料轉成可閱讀、可分享、可行動的城市觀察。

### 主要工作

1. AI issue summary
2. issue trend analyzer
3. reports generator
4. 週報 HTML / Markdown / JSON
5. 社群文案草稿

---

## v1.0｜嘉義城市治理 AI 資料中心

### 目標

建立一個可長期維護、公開透明、可週期更新的城市資料平台。

### v1.0 應具備

- 官方資料 crawler
- 自動資料處理 pipeline
- 資料來源透明頁
- 城市儀表板
- 城市洞察分析
- 真地圖熱點
- 週報系統
- WordPress 官網導流
- n8n 自動化流程
- 清楚的資料治理規範

---

## 優先順序

```text
PR #8 crawler
→ dashboard data pipeline
→ 全站共用導覽
→ Leaflet 地圖
→ reports generator
→ n8n 自動化
```

---

## 原則

1. 每個 PR 只做一個明確任務。
2. Codex 做程式任務，ChatGPT 可先做規格、文件、頁面文案。
3. 不把 prototype data 說成正式資料。
4. 所有分析結果要能回到資料來源。
5. 不公開個資，不做無來源指控。
