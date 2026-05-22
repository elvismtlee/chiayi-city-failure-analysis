# 文件索引

本目錄整理嘉義市城市故障分析資料庫的規格、流程、SOP 與營運文件。此索引用來幫助一人團隊快速找到下一步應該看的文件。

---

## 一、專案進度與總覽

| 文件 | 用途 |
|---|---|
| `docs/issue_progress_matrix.md` | 總覽已完成、進行中、不要重做、下一步建議。 |
| `docs/daily_ops_runbook.md` | 每日資料審核與營運操作節奏。 |
| `docs/review_workbench_sop.md` | 人工審核工作台共同 SOP。 |

建議順序：

```text
issue_progress_matrix.md -> daily_ops_runbook.md -> review_workbench_sop.md
```

---

## 二、Crawler 與資料來源規格

| 文件 | 用途 |
|---|---|
| `docs/metadata_crawler_spec.md` | 嘉義市議會會議紀錄與質詢影音 metadata crawler 第一階段規格。 |
| `docs/cycc_minutes_parser_spec.md` | 嘉義市議會會議紀錄 PDF / HTML 解析規格與 fixture-only parser 基礎。 |

使用原則：

1. 第一階段先抓 metadata，不直接做完整正文解析。
2. 不放 API key、token、credential。
3. 不抓非公開資料。
4. 後續 parser 應先用 fixture 測試，再接正式 crawler。

---

## 三、人工審核與資料安全

| 文件 | 用途 |
|---|---|
| `docs/review_workbench_sop.md` | 統一座標審核、影音審核與未來會議紀錄解析審核流程。 |
| `docs/video_review_sop.md` | 影音轉錄審核與 metadata 補齊流程。 |
| `docs/daily_ops_runbook.md` | 每日與每週的實際操作清單。 |

核心規則：

```text
先留痕，再分析。
先審核，再發布。
先確認來源，再形成結論。
```

---

## 四、n8n 自動化文件

| 文件 | 用途 |
|---|---|
| `docs/n8n_workflow_blueprints.md` | n8n 工作流程藍圖。 |
| `docs/n8n_manual_acceptance_checklist.md` | n8n 第一階段手動驗收清單。 |

n8n 原則：

1. 不自動發文。
2. 不自動公開分享。
3. 只產生草稿、通知或審核清單。
4. 表單資料如需公開，必須先去識別化。

---

## 五、Dashboard 與資料檔

主要 dashboard 入口：

```text
dashboard/index.html
```

常用頁面：

| 頁面 | 用途 |
|---|---|
| `dashboard/map.html` | 城市熱點地圖。 |
| `dashboard/insights.html` | 議題趨勢與洞察。 |
| `dashboard/geocoding-review.html` | 座標人工審核清單。 |
| `dashboard/video-review.html` | 影音 metadata 與轉錄審核清單。 |
| `dashboard/minutes-review.html` | 會議紀錄 fixture parser 人工審核清單。 |
| `dashboard/minutes-issues.html` | 會議紀錄 reviewed sample 轉出的議題候選清單。 |
| `dashboard/weekly-summary.html` | 內部每週市政議題摘要草稿。 |
| `dashboard/policy-drafts.html` | 內部政策草稿候選清單。 |

常用資料檔：

| 資料檔 | 用途 |
|---|---|
| `dashboard/data/hotspots.json` | 熱點資料。 |
| `dashboard/data/hotspots.geojson` | Leaflet 地圖使用的 GeoJSON。 |
| `dashboard/data/geocoding_review_queue.json` | 待人工地理校正清單。 |
| `dashboard/data/transcript_review_queue.json` | 待轉錄與 metadata 審核清單。 |
| `dashboard/data/cycc_minutes_review_queue.json` | 會議紀錄 fixture parser 待人工審核清單。 |
| `data/processed/cycc_minutes_reviewed_sample.json` | 會議紀錄人工審核後的 sample data，不是正式結論。 |
| `dashboard/data/cycc_minutes_issue_candidates.json` | reviewed sample data 轉出的會議紀錄議題候選。 |
| `dashboard/data/weekly_summary_draft.json` | 從 issue candidates 產生的內部週報草稿。 |
| `dashboard/data/policy_draft_candidates.json` | 從 weekly summary draft 產生的政策草稿候選。 |
| `dashboard/data/site_map.json` | dashboard 導覽與頁面說明。 |

常用 scripts：

| Script | 用途 |
|---|---|
| `scripts/build_cycc_minutes_reviewed_sample.py` | 從會議紀錄 review queue 產生 reviewed sample data。 |
| `scripts/build_cycc_minutes_issue_candidates.py` | 從 reviewed sample data 產生議題候選 JSON。 |
| `scripts/build_weekly_summary_draft.py` | 從會議紀錄議題候選產生內部週報草稿。 |
| `scripts/build_policy_draft_candidates.py` | 從週報草稿或議題候選產生政策草稿候選。 |

---

## 六、測試與驗收

常用測試：

```bash
pytest -q
pytest -q tests/test_dashboard_json_validation.py
pytest -q tests/test_dashboard_shared_nav.py
pytest -q tests/test_geocoding_review_page.py
pytest -q tests/test_video_review_page.py
pytest -q tests/test_parse_cycc_minutes_sample.py
pytest -q tests/test_build_cycc_minutes_review_queue.py
pytest -q tests/test_minutes_review_page.py
pytest -q tests/test_build_cycc_minutes_reviewed_sample.py
pytest -q tests/test_build_cycc_minutes_issue_candidates.py
pytest -q tests/test_minutes_issues_page.py
pytest -q tests/test_build_weekly_summary_draft.py
pytest -q tests/test_build_policy_draft_candidates.py
pytest -q tests/test_weekly_summary_page.py
pytest -q tests/test_policy_drafts_page.py
```

新增 PR 前應檢查：

1. 是否新增或更新對應測試。
2. 是否避免重複已合併功能。
3. 是否通過 local terminology 檢查。
4. 是否避免輸出敏感欄位。
5. 是否避免把 prototype 或 AI 初稿標示為正式結論。
6. 是否沒有新增 credential、token、API key。

---

## 七、下一步工作選擇

若要推進 crawler：

```text
先看 metadata_crawler_spec.md
再看 cycc_minutes_parser_spec.md
再新增 fixture
再寫 parser prototype
最後才接正式來源
```

若要推進 dashboard：

```text
先看 site_map.json 與 shared-nav.js
再看對應資料檔
再補 renderer 與測試
```

若要推進人工審核：

```text
先看 review_workbench_sop.md
再看 daily_ops_runbook.md
再逐筆更新 queue 狀態
```

---

## 八、不可重做提醒

已完成的基礎功能不要重做，除非 issue 或 PR 明確要求改善：

1. 熱點 GeoJSON builder。
2. Leaflet 熱點地圖讀取 GeoJSON。
3. 座標審核 queue 與 dashboard。
4. 影音轉錄審核 queue 與 dashboard。
5. shared navigation。
6. n8n 第一階段文件與驗收清單。
7. 人工審核 SOP 與每日營運 runbook。
8. 會議紀錄 fixture-only parser spec 與 sample parser prototype。

---

## 九、資料使用邊界

這個專案是城市治理研究與市政故障分析資料庫，不是民調，也不是支持度調查。

資料對外使用前，應確認：

1. 有公開來源。
2. 有日期與上下文。
3. 已人工 review。
4. 無私人個資。
5. 結論沒有超出原始資料能支持的範圍。
6. 文案不做人身攻擊、不使用未查證指控。

城市有問題，就找出真因；資料要能查證，結論要能說明。
