# 進度補充：官方資料 Crawler Spec 草稿

更新時間：2026-05-23 台北時間

## 已完成

PR #159 已合併，官方資料 crawler spec 草稿已進入 main。

已完成內容：

- `dashboard/open-data-crawler-specs.html`
- `dashboard/data/open_data_crawler_spec_drafts.json`
- `config/open_data_crawler_spec_draft_schema.yml`
- `scripts/build_open_data_crawler_spec_drafts.py`

## 目前資料狀態

- total_count：10。
- source_task_count：10。
- proposed_fetch_method：csv_download_later 10。
- parser_type：csv 10。
- social_welfare：5。
- public_works_environment：3。
- traffic_parking：1。
- culture_events：1。
- public_use_status：internal_crawler_spec_drafts。
- crawler_execution_allowed：false。
- no_live_crawler：true。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。

## 使用邊界

Crawler spec draft 只是工程規格草稿，不代表批准爬取。

目前仍然不啟動 live crawler，不對 source_url 發出網路請求，不抓私人陳情全文，不抓個資，不自動發布。

## 下一階段建議

建議下一包：

```text
feat/open-data-human-review-workbook
```

任務方向：

- 從 10 筆 crawler spec 草稿產生人工審核工作簿。
- 追蹤 source_opened、official_source_verified、license_reviewed、format_checked、personal_data_checked、private_complaint_checked。
- 預設 engineering_review_allowed: false。
- 預設 crawler_execution_allowed: false。
- 仍然不啟動 live crawler。
