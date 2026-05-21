# Sprint Status｜2026-05-21

本文件記錄 2026-05-21 這輪資料平台建置進度，方便後續 ChatGPT / Codex / 人工維護者接續工作。

---

## 一、已完成主軸

### 1. 資料來源與 crawler 基礎

已建立嘉義市議會公開資料 metadata crawler 第一版，並產生 raw metadata：

```text
data/raw/cycc_minutes_metadata.csv
data/raw/cycc_question_video_metadata.csv
```

目前資料型態仍以 metadata 為主，尚未進入全文解析與語音轉文字。

---

### 2. Dashboard data pipeline 與品質門檻

已建立 dashboard JSON 產生與驗證基礎：

```text
dashboard/data/dashboard_summary.json
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
dashboard/data/data_sources.json
dashboard/data/site_map.json
```

已建立品質門檻：

```text
tests/test_build_dashboard_data.py
tests/test_dashboard_json_validation.py
tests/test_local_terminology.py
tests/test_local_place_dictionary.py
```

已建立 GitHub Actions：

```text
.github/workflows/python-tests.yml
.github/workflows/dashboard-data.yml
```

---

### 3. 嘉義在地用語防線

已建立 local place dictionary 與 validation tests。

重要規則：

```text
對外資料使用「文化路」「文化路商圈」「文化路商圈周邊」。
不在 public-facing output 使用「文化路夜市」。
```

「文化路夜市」只可作為 avoid_terms 或測試禁用詞使用。

---

### 4. Dashboard 前端頁面

已完成主要靜態頁面：

```text
dashboard/index.html
dashboard/insights.html
dashboard/sources.html
dashboard/methodology.html
dashboard/reports.html
dashboard/404.html
```

已新增共用導覽與 footer 基礎：

```text
dashboard/shared-nav.js
tests/test_dashboard_shared_nav.py
```

---

### 5. Leaflet 熱點地圖第一版

已完成第一版 Leaflet / OpenStreetMap 熱點地圖：

```text
dashboard/map.html
dashboard/leaflet-map.js
tests/test_leaflet_hotspot_map.py
```

目前地圖讀取：

```text
dashboard/data/hotspots.json
```

若資料尚無 lat/lng，會使用 prototype fallback 座標，並在 popup 標示 prototype。

---

### 6. AI issue classifier prototype

已完成 Issue #12：

```text
src/classifiers/issue_classifier.py
scripts/build_issue_classified_sample.py
data/processed/issue_classified_sample.json
tests/test_issue_classifier.py
tests/test_build_issue_classified_sample.py
```

目前為 rule-based prototype，不呼叫外部 AI API。

資料訊號不足時會產生：

```text
primary_issue: other
review_status: uncertain
```

---

### 7. n8n 第一階段文件與範本

已完成 n8n 第一階段契約、workflow templates 與 README：

```text
docs/n8n_phase1_implementation_contract.md
automation/n8n/phase1_workflow_templates.json
automation/n8n/README.md
tests/test_n8n_phase1_contract.py
tests/test_n8n_phase1_workflow_templates.py
tests/test_n8n_readme.py
```

安全底線：

```text
不自動發文。
不自動寄出對外 email。
不公開個人表單資料。
不把 GitHub token 寫入 repo。
不修改 Google Drive 分享權限。
```

---

## 二、已完成 / 關閉的重要 Issue

```text
#6  建立第一版 Leaflet 熱點地圖
#9  建立資料來源頁 sources.html
#11 重構全站共用導覽列與 footer
#12 建立 AI 議題分類器規格與 prototype
#13 建立 dashboard JSON validation tests
#14 建立 dashboard data GitHub Actions workflow
#15 建立嘉義在地用語 validation test
#16 將在地用語與地名字典測試納入 CI 品質門檻
#17 整理品質門檻入口文件
#18 建立地名審核 CSV 匯入 local_place_dictionary.json 流程
#20 將 local_place_dictionary.json 接入 dashboard data processor
```

---

## 三、仍開啟的重要 Issue

### #7｜建立 issue trend analyzer

目前已交由 Codex 接續。

前置條件已完成：

```text
data/processed/issue_classified_sample.json
src/classifiers/issue_classifier.py
```

下一步應產生：

```text
src/analyzers/issue_trend_analyzer.py
scripts/build_issue_trends.py
dashboard/data/issue_trends.json
tests/test_issue_trend_analyzer.py
tests/test_build_issue_trends.py
```

---

### #10｜建立 n8n 每週資料更新與週報流程

已完成文件、契約、workflow template 與 README。

尚未完成：

```text
實際 n8n 匯入檔
實際 credential 設定
實際 workflow 啟用
```

此 issue 暫不關閉。

---

### #3｜建立城市故障熱點地圖系統

#6 已完成第一版 Leaflet 地圖。

後續 #3 可拆成：

```text
GeoJSON schema
行政區 / 里別 layer
heatmap layer
cluster layer
geocoding pipeline
hotspot aggregation
```

---

### #1 / #2｜Crawler 後續強化

目前已有 metadata crawler 與 raw CSV。

後續仍可強化：

```text
更多欄位解析
PDF / HTML 內容解析
YouTube transcript / Whisper
局處與關鍵字抽取
寫入 Google Sheet
```

因此目前不建議直接關閉 #1 / #2。

---

## 四、已清理的舊 PR

已關閉多個被後續 PR 取代的舊分支 PR，避免 Codex 或人工誤 merge：

```text
#19
#26
#30
#32
#34
#36
#37
```

這些 PR 均非必要，不應再接續開發。

---

## 五、下一步建議

### 最高優先

等待 Codex 完成 Issue #7 PR，檢查：

```text
pytest -q
python scripts/build_issue_trends.py
cat dashboard/data/issue_trends.json
```

### 第二優先

把 `issue_trends.json` 接入：

```text
dashboard/insights.html
```

### 第三優先

讓 `dashboard/index.html` 從 prototype 假地圖逐步切換到：

```text
dashboard/map.html
或 Leaflet map component
```

### 第四優先

繼續 #10，把 n8n template 轉成實際可匯入 n8n 的 workflow JSON，但仍不得包含 credentials。

---

## 六、工作原則

```text
不要只看 Actions 綠燈。
workflow 綠燈是必要條件，不是充分條件。
```

每個 PR 合併前仍需確認：

1. 沒有不當在地用語。
2. 沒有敏感個資欄位。
3. 沒有 token / secret / credential。
4. 沒有把 prototype 資料說成正式結論。
5. 不使用民調、支持度調查等不當說法。
6. 對外資料需標示來源、限制與更新時間。
