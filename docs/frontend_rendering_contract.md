# 前端 Rendering Contract v1

本文件定義 dashboard HTML / JavaScript 與 JSON 資料之間的介面契約。

---

## 目的

避免資料 pipeline 改了 JSON 格式後，前端頁面無法顯示。

---

## 首頁 index.html

### JavaScript

```text
dashboard/app.js
```

### 讀取資料

```text
./data/dashboard_summary.json
./data/issue_ranking.json
./data/hotspots.json
```

### 必要 DOM selector

```text
[data-kpi="total_cases"]
[data-kpi="top_issue"]
[data-kpi="total_hotspots"]
[data-kpi="total_questions"]
[data-kpi="updated_at"]
[data-render="issue_ranking"]
[data-render="hotspot_map"]
[data-render="hotspot_table"]
```

### fallback 原則

若 JSON 讀取失敗：

1. 不應整頁空白。
2. KPI 可顯示 `--`。
3. 表格可顯示「資料整理中」。
4. console 可 warning，但不 throw fatal error。

---

## 洞察頁 insights.html

### JavaScript

```text
dashboard/insights.js
```

### 讀取資料

```text
./data/ai_issue_summary.json
./data/issue_trends.json
./data/urban_failure_scores.json
./data/department_performance.json
./data/councilor_issue_analysis.json
```

### 必要 DOM selector

```text
[data-ai="title"]
[data-ai="updated"]
[data-ai="summary"]
[data-ai="findings"]
[data-ai="actions"]
[data-render="trends"]
[data-render="scores"]
[data-render="departments"]
[data-render="councilors"]
```

---

## 資料來源頁 sources.html

### JavaScript

```text
dashboard/site-pages.js
```

### 讀取資料

```text
./data/data_sources.json
```

### 必要 DOM selector

```text
body[data-page="sources"]
[data-render="sources"]
```

---

## 城市週報頁 reports.html

### JavaScript

```text
dashboard/site-pages.js
```

### 讀取資料

```text
./data/reports_index.json
```

### 必要 DOM selector

```text
body[data-page="reports"]
[data-render="reports"]
```

---

## 共用導覽未來規格

若未來建立：

```text
dashboard/shared-nav.js
```

可讀取：

```text
./data/site_map.json
```

建議 DOM selector：

```text
[data-render="site_nav"]
[data-render="site_footer"]
```

---

## 前端不可依賴

前端不應依賴：

1. JSON array 固定排序。
2. 所有 optional 欄位都存在。
3. 所有數字都非 0。
4. 所有資料都有 lat / lng。
5. 所有 report_url 都已正式存在。

---

## 前端應具備

1. 空資料 fallback。
2. 缺欄位 fallback。
3. 手機版可讀。
4. 不因單一 JSON 失敗導致整頁失效。
5. 對外顯示避免使用內部 code，必要時轉中文 display_name。

---

## Pipeline 對前端的承諾

資料 processor 應盡量保證：

1. 產出合法 JSON。
2. 保留必要欄位。
3. 缺資料時產生 fallback data。
4. `updated_at` 或 `latest_update` 存在。
5. `data_status` 清楚標示 mock / processed / verified。

---

## 變更流程

若要修改 JSON 格式：

1. 先更新 `docs/data_dictionary.md`。
2. 再更新本文件。
3. 再修改 processor。
4. 再修改前端 JS。
5. 最後更新 tests。

不可只改 JSON 格式而不改前端。
