# 進度補充：官方資料人工審核執行工作台

更新時間：2026-05-23 台北時間

## 已完成

PR #165 已合併，官方資料人工審核執行工作台已進入 main。

已完成內容：

- `dashboard/open-data-review-sessions.html`
- `dashboard/data/open_data_review_session_planner.json`
- `config/open_data_review_session_planner_schema.yml`
- `scripts/build_open_data_review_session_planner.py`

## 目前資料狀態

- total_count：10。
- review_day：day_1 3、day_2 4、day_3 3。
- review_batch：batch_1_high_priority 3、batch_2_standard 4、batch_3_follow_up 3。
- total_estimated_minutes：285。
- engineering_review_allowed_count：0。
- crawler_execution_allowed：false。
- no_live_crawler：true。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。

## 使用邊界

人工審核執行工作台不是 crawler，不代表批准爬取。

目前仍然不啟動 live crawler，不對 source_url 發出網路請求，不抓私人陳情全文，不抓個資，不自動發布。

## 下一階段建議

建議下一包：

```text
feat/open-data-review-evidence-pack
```

任務方向：

- 從 10 筆人工審核 session task 產生 evidence pack 草稿。
- 每筆保留 required_evidence_items、evidence_file_placeholders、reviewer_summary_template、acceptance_criteria。
- 預設 engineering_review_allowed: false。
- 預設 crawler_execution_allowed: false。
- 仍然不啟動 live crawler。
